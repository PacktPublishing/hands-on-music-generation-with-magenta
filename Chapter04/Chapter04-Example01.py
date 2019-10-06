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
      "https://storage.googleapis.com/magentadata/models/"
      "%s/checkpoints/%s" % (model_name, checkpoint_name))
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
  download_checkpoint("music_vae", checkpoint, "bundles")
  return TrainedModel(
    # Removes the .lohl in some training checkpoint which shares the same config
    configs.CONFIG_MAP[name.split(".")[0] if "." in name else name],
    # The batch size will affect the z size for a sequence
    batch_size=8,
    checkpoint_dir_or_path=os.path.join("bundles", checkpoint))


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
  if not os.path.exists(output_dir):
    os.mkdir(output_dir)
  if not isinstance(sequences, list):
    sequences = [sequences]
  for (index, sequence) in enumerate(sequences):
    date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
    filename = "%s_%02d_%s.mid" % (prefix, index, date_and_time)
    path = os.path.join(output_dir, filename)
    mm.midi_io.note_sequence_to_midi_file(sequence, path)
    print("Generated midi file: " + str(os.path.abspath(path)))


# TODO sift to chapter 03
def save_plot(sequences: Union[NoteSequence, List[NoteSequence]],
              output_dir: Optional[str] = None,
              prefix: str = "sequence",
              total_bar: int = 2):
  """
  Writes the sequences as HTML plot files to the "output" directory, with the
  filename pattern "<prefix>_<index>_<date_time>" and "html" as extension.

      :param sequences: a NoteSequence or list of NoteSequence to be saved
      :param output_dir: an optional subdirectory in the output directory
      :param prefix: an optional prefix for each file
      :param total_bar: an int for the number of bars to show in the plot
  """
  output_dir = os.path.join("output", output_dir) if output_dir else "output"
  if not os.path.exists(output_dir):
    os.mkdir(output_dir)
  if not isinstance(sequences, list):
    sequences = [sequences]
  for (index, sequence) in enumerate(sequences):
    date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
    filename = "%s_%02d_%s.html" % (prefix, index, date_and_time)
    path = os.path.join(output_dir, filename)
    midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
    if total_bar <= 2:
      # For small sequences, alternate bar fill each 2 bars instead of 1 bar
      bar_fill_alphas = [0.25, 0.25, 0.05, 0.05]
    else:
      # For long sequences, mark the first and last 2 bars in a darker fill
      # and alternate fills in between (each 2 bars)
      bar_fill_alphas = [0.5, 0.5] \
                        + [0.20, 0.20, 0.00, 0.00] * int((total_bar - 4) / 4) \
                        + [0.5, 0.5]
    plotter = Plotter(plot_max_length_bar=total_bar,
                      bar_fill_alphas=bar_fill_alphas,
                      show_velocity=True)
    plotter.save(midi, path)
    print("Generated plot file: " + str(os.path.abspath(path)))


def sample(num_steps_per_sample: int) -> List[NoteSequence]:
  """
  Samples 2 sequences using the 'cat-drums_2bar_small.lokl' model, which
  is optimized for sampling.
  """
  model = get_model("cat-drums_2bar_small.lokl")

  # Uses the model to sample 2 sequences,
  # with the number of steps and default temperature
  sample_sequences = model.sample(2, num_steps_per_sample)

  # Saves the midi and the plot in the sample folder
  save_midi(sample_sequences, "sample", "music_vae")
  save_plot(sample_sequences, "sample", "music_vae")

  return sample_sequences


def interpolate(sample_sequences: List[NoteSequence],
                num_steps_per_sample: int,
                num_output: int,
                total_bars: int) -> NoteSequence:
  """
  Interpolates between 2 sequences using the 'cat-drums_2bar_small.hikl'
  model, which is optimized for interpolating.
  """
  if len(sample_sequences) != 2:
    raise Exception("Wrong number of sequences, expected: 2, actual: "
                    + str(len(sample_sequences)))
  if not sample_sequences[0].notes or not sample_sequences[1].notes:
    raise Exception("Empty note sequences, sequence 1 length: "
                    + str(len(sample_sequences[0].notes))
                    + ", sequence 2 length: "
                    + str(len(sample_sequences[1].notes)))

  model = get_model("cat-drums_2bar_small.hikl")

  # Use the model to interpolate between the 2 input sequences,
  # with the number of output (counting the start and end sequence),
  # number of steps per sample and default temperature
  #
  # This might throw a NoExtractedExamplesError exception if the
  # sequences are not properly formed (for example if the sequences
  # are not quantized, a sequence is empty or not of the proper length).
  interpolate_sequences = model.interpolate(
    sample_sequences[0],
    sample_sequences[1],
    num_output,
    num_steps_per_sample)

  # Saves the midi and the plot in the interpolate folder
  save_midi(interpolate_sequences, "interpolate", "music_vae")
  save_plot(interpolate_sequences, "interpolate", "music_vae")

  # Concatenates the resulting sequences (of length num_output) into one
  # single sequence.
  # The second parameter is a list containing the number of seconds
  # for each input sequence. This is useful if some of the input
  # sequences do not have notes at the end (for example the last
  # note ends at 3.5 seconds instead of 4)
  interpolate_sequence = mm.sequences_lib.concatenate_sequences(
    interpolate_sequences, [4] * num_output)

  # Saves the midi and the plot in the merge folder,
  # with the plot having total_bars size
  save_midi(interpolate_sequence, "merge", "music_vae")
  save_plot(interpolate_sequence, "merge", "music_vae", total_bars)

  return interpolate_sequence


def groove(interpolate_sequence: NoteSequence,
           num_steps_per_sample: int,
           num_output: int,
           total_bars: int) -> NoteSequence:
  """
  Adds groove to the given sequence by splitting it in manageable sequences
  and using the 'groovae_2bar_humanize' model to humanize it.
  """
  model = get_model("groovae_2bar_humanize")

  # Split the sequences in chunks of 4 seconds (which is 2 bars at 120 qpm),
  # which is necessary since the model is trained for 2 bars
  split_interpolate_sequences = mm.sequences_lib.split_note_sequence(
    interpolate_sequence, 4)

  if len(split_interpolate_sequences) != num_output:
    raise Exception("Wrong number of interpolate size, expected: 10, actual: "
                    + str(split_interpolate_sequences))

  # Uses the model to encode the list of sequences, returning the encoding
  # (also called z or latent vector) which will the used in the decoding,
  # The other values mu and sigma are not used, but kept in the code for
  # clarity.
  #
  # The resulting array shape is (a, b), where a is the number of
  # split sequences (should correspond to num_output), and b is the encoding
  # size (should correspond to num_steps_per_sample * model.batch_size).
  #
  # This might throw a NoExtractedExamplesError exception if the
  # sequences are not properly formed (for example if the sequences
  # are not quantized, a sequence is empty or not of the proper length).
  encoding, mu, sigma = model.encode(split_interpolate_sequences)

  # Uses the model to decode the encoding (also called z or latent vector),
  # returning a list of humanized sequence with one element per encoded
  # sequences (each of length num_steps_per_sample).
  groove_sequences = model.decode(encoding, num_steps_per_sample)

  # Concatenates the resulting sequences (of length num_output) into one
  # single sequence.
  groove_sequence = mm.sequences_lib.concatenate_sequences(
    groove_sequences, [4] * num_output)

  # Saves the midi and the plot in the groove folder,
  # with the plot having total_bars size
  save_midi(groove_sequence, "groove", "music_vae")
  save_plot(groove_sequence, "groove", "music_vae", total_bars)

  return groove_sequence


def app(unused_argv):
  # Number of interpolated sequences (counting the start and end sequences)
  num_output = 6

  # Number of bar per sample, also giving the size of the interpolation splits
  num_bar_per_sample = 3

  # Number of steps per sample and interpolation splits
  num_steps_per_sample = num_bar_per_sample * DEFAULT_STEPS_PER_BAR

  # The total number of bars
  total_bars = num_output * num_bar_per_sample

  # Samples 2 new sequences
  generated_sample_sequences = sample(num_steps_per_sample)

  # Interpolates between the 2 sequences, return 1 sequence
  generated_interpolate_sequence = interpolate(generated_sample_sequences,
                                               num_steps_per_sample,
                                               num_output,
                                               total_bars)

  # Adds groove to the whole sequence
  generated_groove_sequence = groove(generated_interpolate_sequence,
                                     num_steps_per_sample,
                                     num_output,
                                     total_bars)

  print("Generated groove sequence total time: ",
        str(generated_groove_sequence.total_time))

  return 0


if __name__ == "__main__":
  tf.app.run(app)
