"""TODO all examples

- TODO talk about the size in the output
- TODO talk about the sample and interpolate code
"""

import os
import time
from typing import List, Union, Optional

import magenta.music as mm
import pretty_midi
import tensorflow as tf
from magenta.models.music_vae import TrainedModel, configs
from magenta.music import DEFAULT_STEPS_PER_BAR
from magenta.protobuf.music_pb2 import NoteSequence
from six.moves import urllib
from visual_midi import Plotter


def download_checkpoint(model_name: str,
                        checkpoint_name: str,
                        target_dir: str):
  """Downloads a Magenta checkpoint to target directory.

  Target directory target_dir will be created if it does not already exist.

  TODO extract?

  Args:
     model_name: magenta model name to download
     checkpoint_name: magenta checkpoint name to download.
     target_dir: local directory in which to write the checkpoint.
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


def get_model(name):
  """TODO"""
  checkpoint = name + ".tar"
  download_checkpoint("music_vae", checkpoint, "bundles")
  return TrainedModel(
    # Removes the .lohl in some training checkpoint which shares the same config
    configs.CONFIG_MAP[name.split(".")[0] if "." in name else name],
    batch_size=8,
    checkpoint_dir_or_path=os.path.join("bundles", checkpoint))


def merge(sequences: List[NoteSequence]) -> NoteSequence:
  merged = pretty_midi.PrettyMIDI()
  for sequence in sequences:
    sequence_midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
    for instrument in sequence_midi.instruments:
      if instrument.notes:
        merged.instruments.append(instrument)
  return mm.midi_io.midi_to_note_sequence(merged)


# TODO sift to chapter 03
def save_midi(sequences: Union[NoteSequence, List[NoteSequence]],
              output_dir: Optional[str] = None,
              prefix: str = "sequence"):
  """Writes the sequences as MIDI files to the "output" directory, with the
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
  """Writes the sequences as HTML plot files to the "output" directory, with the
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
    if total_bar > 2:
      # TODO
      bar_fill_alphas = [0.5, 0.5] \
                        + [0.20, 0.20, 0.00, 0.00] * int((total_bar - 4) / 4) \
                        + [0.5, 0.5]
    else:
      # TODO
      bar_fill_alphas = [0.25, 0.25, 0.05, 0.05]
    # TODO arg
    plotter = Plotter(plot_max_length_bar=total_bar,
                      bar_fill_alphas=bar_fill_alphas,
                      show_velocity=True)
    plotter.save(midi, path)
    print("Generated plot file: " + str(os.path.abspath(path)))


def app(unused_argv):
  # TODO doesn't work
  tf.logging.set_verbosity("INFO")

  num_output = 6
  num_bar_per_sample = 2
  num_steps_per_sample = num_bar_per_sample * DEFAULT_STEPS_PER_BAR
  total_bars = num_output * num_bar_per_sample

  def sample() -> List[NoteSequence]:
    """
    TODO maybe use a primer to set the ending sample
    - use cat-drums_2bar_small.lokl to sample 2 drums sequences
    """
    model = get_model("cat-drums_2bar_small.lokl")

    # TODO explain steps and temperature, 32 is 2 bars
    sample_sequences = model.sample(2, num_steps_per_sample)

    # TODO output in folder
    save_midi(sample_sequences, "sample", "music_vae")
    save_plot(sample_sequences, "sample", "music_vae")

    return sample_sequences

  def interpolate(sample_sequences: List[NoteSequence]) -> NoteSequence:
    """
    - use cat-drums_2bar_small.hikl to interpolate between the 2 drum seq
    """
    if len(sample_sequences) != 2:
      raise Exception("Wrong number of sequences, expected: 2, actual: "
                      + str(len(sample_sequences)))
    if not sample_sequences[0].notes or not sample_sequences[1].notes:
      raise Exception("Empty note sequences, sequence 1: "
                      + str(len(sample_sequences[0].notes))
                      + ", sequence 2: "
                      + str(len(sample_sequences[1].notes)))

    model = get_model("cat-drums_2bar_small.hikl")

    # TODO magenta.models.music_vae.trained_model.NoExtractedExamplesError:
    #  No examples extracted from NoteSequence
    # /home/alex/miniconda3/envs/magenta/lib/python3.5/site-packages/magenta/models/music_vae/trained_model.py:220
    # !!! Needs to be quant
    # TODO explain num_outputs, length, temperature, num_steps is 2 bars
    # TODO use empty sequence : check error and add to book
    interpolate_sequences = model.interpolate(
      sample_sequences[0],
      sample_sequences[1],
      num_output,
      num_steps_per_sample)

    # TODO output in folder
    save_midi(interpolate_sequences, "interpolate", "music_vae")
    save_plot(interpolate_sequences, "interpolate", "music_vae")

    # TODO merge with mm libs
    interpolate_sequence = mm.sequences_lib.concatenate_sequences(
      interpolate_sequences, [4] * num_output)

    save_midi(interpolate_sequence, "merge", "music_vae")
    save_plot(interpolate_sequence, "merge", "music_vae", total_bars)

    # TODO merge in two instruments
    # groove_sequence = merge([sample_melody_sequence, groove_sequence])
    #
    # write_midis("merge", "music_vae-" + "cat-mel_2bar_big" + "-merged",
    #             [groove_sequence])
    # write_plots("merge", "music_vae-" + "cat-mel_2bar_big" + "-merged",
    #             [groove_sequence])

    return interpolate_sequence

  def groove(interpolate_sequence: NoteSequence) -> NoteSequence:
    """
    - use groovae_2bar_humanize to add groove to the drums seq
    - use groovae_2bar_add_closed_hh to add some high hats to the last seq
    """
    # if interpolate_sequence.total_time != 40:
    #   raise Exception("Wrong sequence size, expected: 40, actual: "
    #                   + str(interpolate_sequence.total_time))
    model = get_model("groovae_2bar_humanize")

    # TODO 4 = 120 bpm 2 seconds is 1 bar we need 2 bars
    split_interpolate_sequences = mm.sequences_lib.split_note_sequence(
      interpolate_sequence, 4)

    # TODO why ?
    if len(split_interpolate_sequences) != num_output:
      raise Exception("Wrong number of interpolate size, expected: 10, actual: "
                      + str(split_interpolate_sequences))

    # groove_sequences = []
    # for split_interpolate_sequence in split_interpolate_sequences:
    #   # TODO magenta.models.music_vae.trained_model.NoExtractedExamplesError:
    #   #  No examples extracted from NoteSequence
    #   # /home/alex/miniconda3/envs/magenta/lib/python3.5/site-packages/magenta/models/music_vae/trained_model.py:220
    #   # !!! Needs to be 2 bars
    #   # TODO encode decode, mu, sigma not necessary but clearer
    #   encoding, mu, sigma = model.encode([split_interpolate_sequence])
    #   # TODO num_steps is 2 bars
    #   groove_sequence = model.decode(encoding, num_steps)[0]
    #   groove_sequences.append(groove_sequence)

    # TODO encode decode, mu, sigma not necessary but clearer
    # <class 'tuple'>: (<class 'magenta.models.music_vae.trained_model.NoExtractedExamplesError'>, NoExtractedExamplesError('No examples extracted from NoteSequence: ticks_per_quarter: 220\ntempos
    encoding, mu, sigma = model.encode(split_interpolate_sequences)
    # TODO num_steps is 2 bars
    groove_sequences = model.decode(encoding, num_steps_per_sample)

    # TODO merge with mm libs
    groove_sequence = mm.sequences_lib.concatenate_sequences(
      groove_sequences, [4] * num_output)

    save_midi(groove_sequence, "groove", "music_vae")
    save_plot(groove_sequence, "groove", "music_vae", total_bars)

    # TODO add hi hats
    pass

    return groove_sequence

  # TODO add to book : interpolate works on quantitized stuff
  # TODO add to book : groove works 2 bars at a time
  generated_sample_sequences = sample()
  generated_interpolate_sequence = interpolate(generated_sample_sequences)
  generated_groove_sequence = groove(generated_interpolate_sequence)

  print("Generated groove sequence total time: ",
        str(generated_groove_sequence.total_time))

  return 0


if __name__ == "__main__":
  tf.app.run(app)
