import os
import time

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


# TODO better plot https://strikingmoose.com/2017/07/31/exploring-librosa-and-its-visualizations/
# TODO https://en.wikipedia.org/wiki/Constant-Q_transform
# We display CQTs witha pitch range of 24-96 (C2-C8), hop size of 256, 40 binsper octave, and a filter scale of 0.8.


def save_spectogram_plot(audio,
                         sample_rate: int = 16000,
                         filename: str = None,
                         output_dir: str = "output") -> None:
  """
  TODO
  :param audio: TODO
  :param sample_rate: TODO
  :param output_dir: TODO
  """
  os.makedirs(output_dir, exist_ok=True)
  pitch_min = np.min(36)
  pitch_max = np.max(84)
  frequency_min = librosa.midi_to_hz(pitch_min)
  frequency_max = 2 * librosa.midi_to_hz(pitch_max)
  octaves = int(np.ceil(np.log2(frequency_max) - np.log2(frequency_min)))
  bins_per_octave = 32
  num_bins = int(bins_per_octave * octaves)
  constant_q_transform = librosa.cqt(
    audio,
    sr=sample_rate,
    hop_length=2048,
    fmin=frequency_min,
    n_bins=num_bins,
    bins_per_octave=bins_per_octave)
  plt.figure()
  librosa.display.specshow(
    librosa.amplitude_to_db(constant_q_transform, ref=np.max),
    sr=sample_rate,
    x_axis='time')
  if not filename:
    date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
    filename = f"{date_and_time}.png"
  path = os.path.join(output_dir, filename)
  plt.savefig(fname=path, dpi=600)


if __name__ == "__main__":
  y, sr = librosa.load(
    os.path.join("output", "gansynth", "generated_clip.wav"), )
  save_spectogram_plot(y, output_dir=os.path.join("output", "gansynth"))
