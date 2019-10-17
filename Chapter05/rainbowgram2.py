import glob

import librosa
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read as readwav


def plot_notes(path):
  peak = 70
  fig, ax = plt.subplots()

  # Constants
  n_fft = 512
  hop_length = 256
  SR = 16000
  over_sample = 4
  res_factor = 0.8
  octaves = 6
  notes_per_octave = 10

  # Plotting functions
  cdict = {'red': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

           'green': ((0.0, 0.0, 0.0),
                     (1.0, 0.0, 0.0)),

           'blue': ((0.0, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),

           'alpha': ((0.0, 1.0, 1.0),
                     (1.0, 0.0, 0.0))
           }

  my_mask = matplotlib.colors.LinearSegmentedColormap('MyMask', cdict)
  plt.register_cmap(cmap=my_mask)

  # Add several samples together
  if isinstance(path, list):
    for i, p in enumerate(path):
      sr, a = readwav(path)
      audio = a if i == 0 else a + audio
  # Load one sample
  else:
    sr, audio = readwav(path)
  audio = audio.astype(np.float32)
  C = librosa.cqt(audio,
                  sr=sr,
                  hop_length=hop_length,
                  bins_per_octave=int(notes_per_octave * over_sample),
                  n_bins=int(octaves * notes_per_octave * over_sample),
                  filter_scale=res_factor,
                  fmin=librosa.note_to_hz('C2'))
  mag, phase = librosa.core.magphase(C)
  phase_angle = np.angle(phase)
  phase_unwrapped = np.unwrap(phase_angle)
  dphase = phase_unwrapped[:, 1:] - phase_unwrapped[:, :-1]
  dphase = np.concatenate([phase_unwrapped[:, 0:1], dphase], axis=1) / np.pi
  mag = (librosa.power_to_db(mag ** 2, amin=1e-13, top_db=peak,
                             ref=np.max) / peak) + 1
  ax.set_facecolor('white')
  ax.set_xticks([])
  ax.set_yticks([])
  ax.matshow(dphase[::-1, :], cmap=plt.cm.rainbow)
  ax.matshow(mag[::-1, :], cmap=my_mask)

  plt.savefig(fname=filename.replace(".wav", "__2.png"), dpi=600)


if __name__ == "__main__":
  for filename in glob.glob("output/nsynth/*.wav"):
    plot_notes(filename)
