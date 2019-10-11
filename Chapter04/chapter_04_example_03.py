"""
TODO 01 example
"""

import os
import time
from typing import List, Union, Optional

import magenta.music as mm
import tensorflow as tf
from magenta.models.music_vae import TrainedModel, configs
from magenta.music import DEFAULT_STEPS_PER_BAR
from magenta.protobuf.music_pb2 import NoteSequence
from six.moves import urllib
from visual_midi import Plotter


def download_checkpoint(model_name: str,
                        checkpoint_name: str,
                        target_dir: str):
  """
  Downloads a Magenta checkpoint to target directory.

  Target directory target_dir will be created if it does not already exist.

      :param model_name: magenta model name to download
      :param checkpoint_name: magenta checkpoint name to download
      :param target_dir: local directory in which to write the checkpoint
  """
  tf.gfile.MakeDirs(target_dir)
  checkpoint_target = os.path.join(target_dir, checkpoint_name)
  if not os.path.exists(checkpoint_target):
    response = urllib.request.urlopen(
      f"https://storage.googleapis.com/magentadata/models/"
      f"{model_name}/checkpoints/{checkpoint_name}")
    data = response.read()
    local_file = open(checkpoint_target, 'wb')
    local_file.write(data)
    local_file.close()


def get_model(name: str):
  """
  Returns the model instance from its name.

      :param name: the model name
  """
  checkpoint = name + ".tar"
  download_checkpoint("music_vae", checkpoint, "checkpoints")
  return TrainedModel(
    # Removes the .lohl in some training checkpoint which shares the same config
    configs.CONFIG_MAP[name.split(".")[0] if "." in name else name],
    # The batch size changes the number of sequences to be processed together
    batch_size=8,
    checkpoint_dir_or_path=os.path.join("checkpoints", checkpoint))


# TODO sift to chapter 03
def save_midi(sequences: Union[NoteSequence, List[NoteSequence]],
              output_dir: Optional[str] = None,
              prefix: str = "sequence"):
  """
  Writes the sequences as MIDI files to the "output" directory, with the
  filename pattern "<prefix>_<index>_<date_time>" and "mid" as extension.

      :param sequences: a NoteSequence or list of NoteSequence to be saved
      :param output_dir: an optional subdirectory in the output directory
      :param prefix: an optional prefix for each file
  """
  output_dir = os.path.join("output", output_dir) if output_dir else "output"
  os.makedirs(output_dir, exist_ok=True)
  if not isinstance(sequences, list):
    sequences = [sequences]
  for (index, sequence) in enumerate(sequences):
    date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
    filename = f"{prefix}_{index:02}_{date_and_time}.mid"
    path = os.path.join(output_dir, filename)
    mm.midi_io.note_sequence_to_midi_file(sequence, path)
    print(f"Generated midi file: {os.path.abspath(path)}")


# TODO sift to chapter 03
def save_plot(sequences: Union[NoteSequence, List[NoteSequence]],
              output_dir: Optional[str] = None,
              prefix: str = "sequence",
              plot_max_length_bar: int = 8):
  """
  Writes the sequences as HTML plot files to the "output" directory, with the
  filename pattern "<prefix>_<index>_<date_time>" and "html" as extension.

      :param sequences: a NoteSequence or list of NoteSequence to be saved
      :param output_dir: an optional subdirectory in the output directory
      :param prefix: an optional prefix for each file
      :param plot_max_length_bar: an int for the number of bars to show in the plot
  """
  output_dir = os.path.join("output", output_dir) if output_dir else "output"
  os.makedirs(output_dir, exist_ok=True)
  if not isinstance(sequences, list):
    sequences = [sequences]
  for (index, sequence) in enumerate(sequences):
    date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
    filename = f"{prefix}_{index:02}_{date_and_time}.html"
    path = os.path.join(output_dir, filename)
    midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
    plotter = Plotter(plot_max_length_bar=plot_max_length_bar,
                      show_velocity=True)
    plotter.save(midi, path)
    print(f"Generated plot file: {os.path.abspath(path)}")


def sample(model_name: str,
           num_steps_per_sample: int) -> List[NoteSequence]:
  """
  Samples 2 sequences using the given model.
  """
  model = get_model(model_name)

  # Uses the model to sample 2 sequences,
  # with the number of steps and default temperature
  sample_sequences = model.sample(2, num_steps_per_sample)

  # Saves the midi and the plot in the sample folder
  save_midi(sample_sequences, "sample", model_name)
  save_plot(sample_sequences, "sample", model_name, 16)

  return sample_sequences


def app(unused_argv):
  # Number of bar per sample, also giving the size of the interpolation splits
  num_bar_per_sample = 16

  # Number of steps per sample and interpolation splits
  num_steps_per_sample = num_bar_per_sample * DEFAULT_STEPS_PER_BAR

  # Samples 2 new sequences
  generated_sample_sequences = sample("hierdec-trio_16bar",
                                      num_steps_per_sample)

  print(f"Generated sample sequence total time: "
        f"{generated_sample_sequences[0].total_time}")

  return 0


if __name__ == "__main__":
  tf.app.run(app)
