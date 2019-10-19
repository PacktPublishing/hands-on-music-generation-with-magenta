import glob
import os

import librosa
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read as readwav

# Configuration from https://arxiv.org/abs/1704.01279
# and https://gist.github.com/jesseengel/e223622e255bd5b8c9130407397a0494
peak = 70
n_fft = 512
hop_length = 256
sample_rate = 16000
over_sample = 4
res_factor = 0.8
octaves = 6
notes_per_octave = 10
color_dict = {
  'red': ((0.0, 0.0, 0.0),
          (1.0, 0.0, 0.0)),
  'green': ((0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0)),
  'blue': ((0.0, 0.0, 0.0),
           (1.0, 0.0, 0.0)),
  'alpha': ((0.0, 1.0, 1.0),
            (1.0, 0.0, 0.0))
}
color_mask = matplotlib.colors.LinearSegmentedColormap('ColorMask', color_dict)
plt.register_cmap(cmap=color_mask)


def save_rainbowgram(path: str,
                     output_dir: str):
  os.makedirs(output_dir, exist_ok=True)
  print(f"Plotting {path} to {output_dir}")

  # Init subplots, there is only one plot but we have to use 2 cmap,
  # which means 2 call to ax.matshow that wouldn't work with a single plot.
  fig, ax = plt.subplots()
  plt.axis('off')

  # Generates the plot
  _, audio = readwav(path)
  audio = audio.astype(np.float32)
  bins_per_octave = int(notes_per_octave * over_sample)
  n_bins = int(octaves * notes_per_octave * over_sample)
  constant_q_transform = librosa.cqt(audio,
                                     sr=sample_rate,
                                     hop_length=hop_length,
                                     bins_per_octave=bins_per_octave,
                                     n_bins=n_bins,
                                     filter_scale=res_factor,
                                     fmin=librosa.note_to_hz('C2'))
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

  # Saves the figure
  filename = os.path.basename(path)
  path = os.path.join(output_dir, filename.replace(".wav", "_rainbowgram.png"))
  plt.savefig(fname=path, dpi=600)


if __name__ == "__main__":
  for filename in glob.glob("output/gansynth/*.wav"):
    save_rainbowgram(filename, os.path.join("output",
                                            "rainbowgrams",
                                            "gansynth"))
  for filename in glob.glob("output/nsynth/*.wav"):
    save_rainbowgram(filename, os.path.join("output",
                                            "rainbowgrams",
                                            "nsynth"))
  for filename in glob.glob("sounds/*.wav"):
    save_rainbowgram(filename, os.path.join("output",
                                            "rainbowgrams",
                                            "sounds"))
