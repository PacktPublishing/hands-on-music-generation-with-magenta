from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen


def mix(wav1: str,
        wav2: str,
        sample_length: int = None,
        sample_rate: int = 16000,
        checkpoint=None):
  encoding1 = encode(wav1, sample_length, sample_rate, checkpoint)
  encoding2 = encode(wav2, sample_length, sample_rate, checkpoint)
  encoding_mix = (encoding1 + encoding2) / 2.0
  # TODO add figures show
  return encoding_mix


def encode(wav: str,
           sample_length: int = None,
           sample_rate: int = 16000,
           checkpoint=None):
  audio = utils.load_audio(wav,
                           sample_length=sample_length,
                           sr=sample_rate)
  encoding = fastgen.encode(audio, checkpoint, sample_length)
  return encoding
