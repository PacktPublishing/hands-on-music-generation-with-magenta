"""TODO all examples

- TODO talk about the size in the output
- TODO talk about the sample and interpolate code
"""

import os
import time
from typing import Tuple, List

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
  """TODO split melody and drums"""

  num_outputs = 10

  def sample() -> Tuple[List[NoteSequence], List[NoteSequence]]:
    """
    TODO maybe use a primer to set the ending sample
    - use cat-mel_2bar_big to sample 2 melodies
    - use cat-drums_2bar_small.lokl to sample 2 drums sequences
    """
    model_melody = get_model("cat-mel_2bar_big")
    model_drums = get_model("cat-drums_2bar_small.lokl")

    # TODO explain steps and temperature
    sample_melody_sequences = model_melody.sample(2, 32, 1)
    sample_drums_sequences = model_drums.sample(2, 32, 1)

    # TODO output in folder
    write_midis("sample", "music_vae-" + "cat-mel_2bar_big",
                sample_melody_sequences)
    write_plots("sample", "music_vae-" + "cat-mel_2bar_big",
                sample_melody_sequences)
    write_midis("sample", "music_vae-" + "cat-drums_2bar_small",
                sample_drums_sequences)
    write_plots("sample", "music_vae-" + "cat-drums_2bar_small",
                sample_drums_sequences)

    return sample_drums_sequences, sample_melody_sequences

  def interpolate(sample_drums_sequences: List[NoteSequence],
                  sample_melody_sequences: List[NoteSequence]) \
      -> Tuple[NoteSequence, NoteSequence]:
    """
    - use cat-mel_2bar_big to interpolate between the 2 melodies
    - use cat-drums_2bar_small.hikl to interpolate between the 2 drum seq
    """
    model_melody = get_model("cat-mel_2bar_big")
    model_drums = get_model("cat-drums_2bar_small.hikl")

    # TODO explain num_outputs, length, temperature
    sample_melody_sequences = model_melody.interpolate(
      sample_melody_sequences[0], sample_melody_sequences[1], 10, 32, 1)
    sample_drums_sequences = model_drums.interpolate(
      sample_drums_sequences[0], sample_drums_sequences[1], 10, 32, 1)

    # TODO output in folder
    write_midis("interpolate", "music_vae-" + "cat-mel_2bar_big",
                sample_melody_sequences)
    write_plots("interpolate", "music_vae-" + "cat-mel_2bar_big",
                sample_melody_sequences)
    write_midis("interpolate", "music_vae-" + "cat-drums_2bar_small",
                sample_drums_sequences)
    write_plots("interpolate", "music_vae-" + "cat-drums_2bar_small",
                sample_drums_sequences)

    # TODO merge with mm libs
    sample_melody_sequence = mm.sequences_lib.concatenate_sequences(
      sample_melody_sequences)
    sample_drums_sequence = mm.sequences_lib.concatenate_sequences(
      sample_drums_sequences)

    write_midis("merge", "music_vae-" + "cat-mel_2bar_big",
                [sample_melody_sequence])
    write_plots("merge", "music_vae-" + "cat-mel_2bar_big",
                [sample_melody_sequence])
    write_midis("merge", "music_vae-" + "cat-drums_2bar_small",
                [sample_drums_sequence])
    write_plots("merge", "music_vae-" + "cat-drums_2bar_small",
                [sample_drums_sequence])

    # TODO merge in two instruments
    sample_sequence = merge([sample_melody_sequence, sample_drums_sequence])

    write_midis("merge", "music_vae-" + "cat-mel_2bar_big" + "-merged",
                [sample_sequence])
    write_plots("merge", "music_vae-" + "cat-mel_2bar_big" + "-merged",
                [sample_sequence])

    return sample_melody_sequence, sample_drums_sequence

  def groove(sample_drums_sequences: List[NoteSequence],
             sample_melody_sequences: List[NoteSequence]):
    """
    - use groovae_2bar_humanize to add groove to the 2 drums seq
    - use groovae_2bar_add_closed_hh to add some high hats to the last seq
    """
    pass

  sample_drums_sequences, sample_melody_sequences = sample()
  interpolate(sample_drums_sequences, sample_melody_sequences)
  groove(sample_drums_sequences, sample_melody_sequences)

  return 0


if __name__ == "__main__":
  tf.app.run(app)
