import glob
import os
import time

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


def save_spectogram_plot(audio,
                         sample_rate: int = 16000,
                         filename: str = None,
                         output_dir: str = "output") -> None:
  """
  TODO
  :param audio: TODO
  :param sample_rate: TODO
  :param filename: TODO
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
  hop_length = 2048
  constant_q_transform = librosa.cqt(
    audio,
    sr=sample_rate,
    hop_length=hop_length,
    fmin=frequency_min,
    n_bins=num_bins,
    bins_per_octave=bins_per_octave)
  plt.figure()
  librosa.display.specshow(
    librosa.amplitude_to_db(constant_q_transform, ref=np.max),
    sr=sample_rate,
    x_axis="time")

  if not filename:
    date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
    filename = f"{date_and_time}.png"
  path = os.path.join(output_dir, filename)
  plt.savefig(fname=path, dpi=600)
  plt.clf()


def save_rainbowgram_plot(audio,
                          sample_rate: int = 16000,
                          filename: str = None,
                          output_dir: str = "output") -> None:
  """
  TODO
  :param audio:
  :param sample_rate:
  :param filename:
  :param output_dir:
  :return:
  """
  os.makedirs(output_dir, exist_ok=True)

  # Configuration from https://arxiv.org/abs/1704.01279
  # and https://gist.github.com/jesseengel/e223622e255bd5b8c9130407397a0494
  peak = 70
  hop_length = 256
  over_sample = 4
  res_factor = 0.8
  octaves = 6
  notes_per_octave = 10
  color_dict = {
    "red": ((0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0)),
    "green": ((0.0, 0.0, 0.0),
              (1.0, 0.0, 0.0)),
    "blue": ((0.0, 0.0, 0.0),
             (1.0, 0.0, 0.0)),
    "alpha": ((0.0, 1.0, 1.0),
              (1.0, 0.0, 0.0))
  }
  color_mask = LinearSegmentedColormap("ColorMask", color_dict)
  plt.register_cmap(cmap=color_mask)

  # Init subplots, there is only one plot but we have to use 2 cmap,
  # which means 2 call to ax.matshow that wouldn"t work with a single plot.
  fig, ax = plt.subplots()
  plt.axis("off")

  bins_per_octave = int(notes_per_octave * over_sample)
  num_bins = int(octaves * notes_per_octave * over_sample)
  constant_q_transform = librosa.cqt(audio,
                                     sr=sample_rate,
                                     hop_length=hop_length,
                                     bins_per_octave=bins_per_octave,
                                     n_bins=num_bins,
                                     filter_scale=res_factor,
                                     fmin=librosa.note_to_hz("C2"))
  mag, phase = librosa.core.magphase(constant_q_transform)
  phase_angle = np.angle(phase)
  phase_unwrapped = np.unwrap(phase_angle)
  dphase = phase_unwrapped[:, 1:] - phase_unwrapped[:, :-1]
  dphase = np.concatenate([phase_unwrapped[:, 0:1], dphase], axis=1) / np.pi
  mag = (librosa.power_to_db(mag ** 2,
                             amin=1e-13,
                             top_db=peak,
                             ref=np.max) / peak) + 1
  ax.matshow(dphase[::-1, :], cmap=plt.cm.rainbow)
  ax.matshow(mag[::-1, :], cmap=color_mask)

  if not filename:
    date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
    filename = f"{date_and_time}.png"
  path = os.path.join(output_dir, filename)
  plt.savefig(fname=path, dpi=600)
  plt.clf()


if __name__ == "__main__":
  for path in glob.glob("output/nsynth/*.wav"):
    audio, _ = librosa.load(path, 16000)
    filename = os.path.basename(path)
    output_dir = os.path.join("output", "nsynth", "plots")
    print(f"Writing rainbowgram for {path}  in {output_dir}")
    save_rainbowgram_plot(audio,
                          filename=filename.replace(".wav", "_rainbowgram.png"),
                          output_dir=output_dir)
