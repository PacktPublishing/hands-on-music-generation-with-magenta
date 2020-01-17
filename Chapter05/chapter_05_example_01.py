"""
This example shows how to use NSynth to interpolate between pairs of sounds.
"""

import os
import tarfile
from typing import List, Tuple

import numpy as np
import tensorflow as tf
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen
from six.moves import urllib

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string(
  "log", "WARN",
  "The threshold for what messages will be logged. DEBUG, INFO, WARN, ERROR, "
  "or FATAL.")

WAV_FILENAMES = ["83249__zgump__bass-0205__crop.wav",
                 "160045__jorickhoofd__metal-hit-with-metal-bar-resonance"
                 "__crop.wav",
                 "412017__skymary__cat-meow-short__crop.wav",
                 "427567__maria-mannone__flute__crop.wav"]


def download_checkpoint(checkpoint_name: str,
                        target_dir: str = "checkpoints") -> None:
  """
  Downloads a Magenta checkpoint to target directory and extracts it.

  Target directory target_dir will be created if it does not already exist.

      :param checkpoint_name: magenta checkpoint name to download,
      one of "baseline-ckpt" or "wavenet-ckpt"
      :param target_dir: local directory in which to write the checkpoint
  """
  tf.gfile.MakeDirs(target_dir)
  checkpoint_target = os.path.join(target_dir, f"{checkpoint_name}.tar")
  if not os.path.exists(checkpoint_target):
    response = urllib.request.urlopen(
      f"http://download.magenta.tensorflow.org/"
      f"models/nsynth/{checkpoint_name}.tar")
    data = response.read()
    local_file = open(checkpoint_target, 'wb')
    local_file.write(data)
    local_file.close()
    tar = tarfile.open(checkpoint_target)
    tar.extractall(target_dir)
    tar.close()


def encode(wav_filenames: List[str],
           checkpoint: str = "checkpoints/wavenet-ckpt/model.ckpt-200000",
           sample_length: int = 16000,
           sample_rate: int = 16000) -> List[np.ndarray]:
  """
  Encodes the list of filename to encodings by loading the wav files,
  encoding them using fastgen, and returning the result.

  :param wav_filenames: the list of filenames to encode, they need to be
  present in the "sound" folder
  :param checkpoint: the checkpoint folder
  :param sample_length: the sample length, can be calculated by multiplying
  the desired number of seconds by 16000
  :param sample_rate: the sample rate, should be 16000
  """
  if not wav_filenames:
    return []

  # Loads the audio for each filenames
  audios = []
  for wav_filename in wav_filenames:
    audio = utils.load_audio(os.path.join("sounds", wav_filename),
                             sample_length=sample_length,
                             sr=sample_rate)
    audios.append(audio)

  # Encodes the audio for each new wav
  audios = np.array(audios)
  encodings = fastgen.encode(audios, checkpoint, sample_length)

  return encodings


def mix_encoding_pairs(encodings: List[np.ndarray],
                       encodings_name: List[str]) \
    -> Tuple[np.ndarray, List[str]]:
  """
  Mixes each elements of the encodings two by two, by adding the encodings
  together and returning them, with their resulting mixed filename.

  :param encodings: the list of encodings
  :param encodings_name: the list of encodings names
  """
  encodings_mix = []
  encodings_mix_name = []
  # Takes the pair of encodings two by two
  for encoding1, encoding1_name in zip(encodings, encodings_name):
    for encoding2, encoding2_name in zip(encodings, encodings_name):
      if encoding1_name == encoding2_name:
        continue
      # Adds the encodings together
      encoding_mix = encoding1 + encoding2 / 2.0
      encodings_mix.append(encoding_mix)
      # Merges the beginning of the track names
      if "_" in encoding1_name and "_" in encoding2_name:
        encoding_name = (f"{encoding1_name.split('_', 1)[0]}_"
                         f"{encoding2_name.split('_', 1)[0]}")
      else:
        encoding_name = f"{encoding1_name}_{encoding2_name}"
      encodings_mix_name.append(encoding_name)
  return np.array(encodings_mix), encodings_mix_name


def synthesize(encodings_mix: np.ndarray,
               encodings_mix_name: List[str],
               checkpoint: str = "checkpoints/wavenet-ckpt/model.ckpt-200000") \
    -> None:
  """
  Synthetizes the list of encodings and saves them under the list of names.
  This might take a long time on commodity hardware (~15 minutes)

  :param encodings_mix: the list of encodings to synth
  :param encodings_mix_name: the list of encodings names for the files
  :param checkpoint: the checkpoint folder
  """
  os.makedirs(os.path.join("output", "nsynth"), exist_ok=True)
  encodings_mix_name = [os.path.join("output", "nsynth",
                                     encoding_mix_name + ".wav")
                        for encoding_mix_name in encodings_mix_name]
  fastgen.synthesize(encodings_mix,
                     checkpoint_path=checkpoint,
                     save_paths=encodings_mix_name)


def app(unused_argv):
  # Downloads and extracts the checkpoint to "checkpoints/wavenet-ckpt"
  download_checkpoint("wavenet-ckpt")

  # Encodes the wav files into 4 encodings (and saves them for later use)
  encodings = encode(WAV_FILENAMES)

  # Mix the 4 encodings pairs into 12 encodings
  encodings_mix, encodings_mix_name = mix_encoding_pairs(encodings,
                                                         WAV_FILENAMES)

  # Synthesize the 12 encodings into wavs
  synthesize(encodings_mix, encodings_mix_name)


if __name__ == "__main__":
  tf.logging.set_verbosity(FLAGS.log)
  tf.app.run(app)
