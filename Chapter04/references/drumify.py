"""
TODO 01 example
"""

import os

import tensorflow as tf
from magenta.models.music_vae import TrainedModel, configs, Config
from magenta.music import midi_file_to_note_sequence
from magenta.protobuf.music_pb2 import NoteSequence
from six.moves import urllib


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


def get_config(name: str) -> Config:
  return configs.CONFIG_MAP[name.split(".")[0] if "." in name else name]


def get_model(name: str) -> TrainedModel:
  """
  Returns the model instance from its name.

      :param name: the model name
  """
  checkpoint = name + ".tar"
  download_checkpoint("music_vae", checkpoint, "checkpoints")
  return TrainedModel(
    # Removes the .lohl in some training checkpoint which shares the same config
    get_config(name),
    # The batch size changes the number of sequences to be processed together
    batch_size=8,
    checkpoint_dir_or_path=os.path.join("checkpoints", checkpoint))


# TODO quick method for turning a drumbeat into a tapped rhythm
def get_tapped_2bar(sequence):
  model_tap = get_config("groovae_2bar_tap_fixed_velocity")
  data_converter_tap = model_tap.data_converter
  sequence_tap = data_converter_tap.to_notesequences(
    data_converter_tap.to_tensors(sequence).inputs)[0]
  # new_s = change_tempo(new_s, sequence.tempos[0].qpm)
  for note in sequence_tap.notes:
    note.velocity = 100
    note.pitch = 42
  return sequence_tap


def drumify(model_name: str, sequence: NoteSequence) -> NoteSequence:
  """
  Adds groove to the given sequence by splitting it in manageable sequences
  and using the given model to humanize it.
  """
  model = get_model(model_name)

  # TODO make that a tapped sequence
  pass


def app(unused_argv):
  sequence = midi_file_to_note_sequence(
    os.path.join("primers", "52_jazz_125_beat_4-4.mid"))

  tapped_sequence = get_tapped_2bar(sequence)

  return 0


if __name__ == "__main__":
  tf.app.run(app)
