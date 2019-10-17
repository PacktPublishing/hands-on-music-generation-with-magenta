import os
from typing import List, Tuple

import numpy as np
import tensorflow as tf
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen

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


def app(unused_argv):
  # TODO get checkpoint http://download.magenta.tensorflow.org/models/nsynth/wavenet-ckpt.tar
  pass

  # TODO this returns 4 encodings
  encodings = encode(WAV_FILENAMES)

  # TODO check sample length
  encodings_mix, encodings_mix_name = mix(encodings, WAV_FILENAMES)

  # TODO synth
  synth(encodings_mix, encodings_mix_name)


def encode(wav_filenames: List[str],
           checkpoint: str = "checkpoints/wavenet-ckpt/model.ckpt-200000",
           sample_length: int = 16000,
           sample_rate: int = 16000) -> List[np.ndarray]:
  """
  TODO
  """
  # TODO utilities
  os.makedirs("encodings", exist_ok=True)

  def get_npy_path(wav_filename):
    return os.path.join("encodings", wav_filename.replace(".wav", ".npy"))

  # TODO convert to audio
  audios_new = []
  for wav_filename in wav_filenames:
    if os.path.exists(get_npy_path(wav_filename)):
      continue
    audio = utils.load_audio(os.path.join("sounds", wav_filename),
                             sample_length=sample_length,
                             sr=sample_rate)
    audios_new.append(audio)

  # TODO encoding
  encodings_new = []
  if audios_new:
    audios_new = np.array(audios_new)
    encodings_new = fastgen.encode(audios_new, checkpoint, sample_length)

  # TODO saving
  index = 0
  encodings = []
  for wav_filename in wav_filenames:
    if os.path.exists(get_npy_path(wav_filename)):
      encoding = np.load(get_npy_path(wav_filename))
    else:
      encoding = encodings_new[index]
      np.save(get_npy_path(wav_filename), encoding)
    encodings.append(encoding)
    index = index + 1

  # TODO returning all encodings
  assert len(encodings) == len(wav_filenames)
  return encodings


def mix(encodings: List[np.ndarray],
        encodings_name: List[str]) -> Tuple[np.ndarray, List[str]]:
  """
  TODO
  """
  encodings_mix = []
  encodings_mix_name = []
  for encoding1, encoding1_name in zip(encodings, encodings_name):
    for encoding2, encoding2_name in zip(encodings, encodings_name):
      if encoding1 is encoding2:
        continue
      # TODO encodings
      encoding_mix = encoding1 + encoding2 / 2.0
      encodings_mix.append(encoding_mix)
      # TODO encoding name
      encoding_name = (f"{encoding1_name.split('_', 1)[0]}_"
                       f"{encoding2_name.split('_', 1)[0]}"
                       f".wav")
      encodings_mix_name.append(encoding_name)
  # TODO add figures show
  return np.array(encodings_mix), encodings_mix_name


def synth(encodings_mix: np.ndarray,
          encodings_mix_name: List[str],
          checkpoint: str = "checkpoints/wavenet-ckpt/model.ckpt-200000"):
  """
  TODO
  """
  os.makedirs(os.path.join("output", "nsynth"), exist_ok=True)
  encodings_mix_name = [os.path.join("output", "nsynth", encoding_mix_name)
                        for encoding_mix_name in encodings_mix_name]
  fastgen.synthesize(encodings_mix,
                     checkpoint_path=checkpoint,
                     save_paths=encodings_mix_name)


if __name__ == "__main__":
  tf.logging.set_verbosity(FLAGS.log)
  tf.app.run(app)
