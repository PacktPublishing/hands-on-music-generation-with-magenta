"""TODO all examples

- TODO talk about the size in the output
- TODO talk about the sample and interpolate code
"""

import os
import time
from typing import List

import magenta.music as mm
import pretty_midi
import tensorflow as tf
from magenta.models.music_vae import TrainedModel, configs
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


def write_midis(dir: str, prefix: str, sequences: List[NoteSequence]):
  # TODO Writes the resulting midi file to the output directory
  if not os.path.exists(os.path.join("output", dir)):
    os.mkdir(os.path.join("output", dir), )
  for (index, sequence) in enumerate(sequences):
    date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
    midi_filename = "%s_%s_%s.mid" % (prefix, index, date_and_time)
    midi_path = os.path.join("output", dir, midi_filename)
    mm.midi_io.note_sequence_to_midi_file(sequence, midi_path)
    print("Generated midi file: " + str(os.path.abspath(midi_path)))


def write_plots(dir: str, prefix: str, sequences: List[NoteSequence]):
  # TODO Writes the resulting plot file to the output directory
  if not os.path.exists(os.path.join("output", dir)):
    os.mkdir(os.path.join("output", dir), )
  for (index, sequence) in enumerate(sequences):
    date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
    plot_filename = "%s_%s_%s.html" % (prefix, index, date_and_time)
    plot_path = os.path.join("output", dir, plot_filename)
    pretty_midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
    plotter = Plotter(plot_max_length_time=64)
    plotter.save(pretty_midi, plot_path)
    print("Generated plot file: " + str(os.path.abspath(plot_path)))


def app(unused_argv):
  def sample() -> List[NoteSequence]:
    """
    TODO maybe use a primer to set the ending sample
    - use cat-drums_2bar_small.lokl to sample 2 drums sequences
    """
    model = get_model("cat-drums_2bar_small.lokl")

    # TODO explain steps and temperature, 32 is 2 bars
    sample_sequences = model.sample(2, 32, 1)

    # TODO output in folder
    write_midis("sample", "music_vae-" + "cat-drums_2bar_small",
                sample_sequences)
    write_plots("sample", "music_vae-" + "cat-drums_2bar_small",
                sample_sequences)

    return sample_sequences

  def interpolate(sample_sequences: List[NoteSequence]) -> NoteSequence:
    """
    - use cat-drums_2bar_small.hikl to interpolate between the 2 drum seq
    """
    if len(sample_sequences) != 2:
      raise Exception("Wrong number of sequences, expected: 2, actual: "
                      + str(len(sample_sequences)))

    model = get_model("cat-drums_2bar_small.hikl")

    # TODO magenta.models.music_vae.trained_model.NoExtractedExamplesError:
    #  No examples extracted from NoteSequence
    # /home/alex/miniconda3/envs/magenta/lib/python3.5/site-packages/magenta/models/music_vae/trained_model.py:220
    # !!! Needs to be quant
    # TODO explain num_outputs, length, temperature, 32 is 2 bars
    # TODO use empty sequence : check error and add to book
    interpolate_sequences = model.interpolate(
      sample_sequences[0], sample_sequences[1], 10, 32, 1)

    # TODO output in folder
    write_midis("interpolate", "music_vae-" + "cat-drums_2bar_small",
                interpolate_sequences)
    write_plots("interpolate", "music_vae-" + "cat-drums_2bar_small",
                interpolate_sequences)

    # TODO merge with mm libs
    interpolate_sequence = mm.sequences_lib.concatenate_sequences(
      interpolate_sequences)

    write_midis("merge", "music_vae-" + "cat-drums_2bar_small",
                [interpolate_sequence])
    write_plots("merge", "music_vae-" + "cat-drums_2bar_small",
                [interpolate_sequence])

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
    model = get_model("groovae_2bar_humanize")

    # TODO 4 = 120 bpm 2 seconds is 1 bar we need 2 bars
    split_interpolate_sequences = mm.sequences_lib.split_note_sequence(
      interpolate_sequence, 4)

    # groove_sequences = []
    # for split_interpolate_sequence in split_interpolate_sequences:
    #   # TODO magenta.models.music_vae.trained_model.NoExtractedExamplesError:
    #   #  No examples extracted from NoteSequence
    #   # /home/alex/miniconda3/envs/magenta/lib/python3.5/site-packages/magenta/models/music_vae/trained_model.py:220
    #   # !!! Needs to be 2 bars
    #   # TODO encode decode, mu, sigma not necessary but clearer
    #   encoding, mu, sigma = model.encode([split_interpolate_sequence])
    #   # TODO 32 is 2 bars
    #   groove_sequence = model.decode(encoding, 32)[0]
    #   groove_sequences.append(groove_sequence)

    # TODO encode decode, mu, sigma not necessary but clearer
    encoding, mu, sigma = model.encode(split_interpolate_sequences)
    # TODO 32 is 2 bars
    groove_sequences = model.decode(encoding, 32)

    # TODO merge with mm libs
    groove_sequence = mm.sequences_lib.concatenate_sequences(
      groove_sequences, [2] * 10)

    write_midis("groove", "music_vae-" + "groove",
                [groove_sequence])
    write_plots("groove", "music_vae-" + "groove",
                [groove_sequence])

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
