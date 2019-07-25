import wave

import matplotlib.pyplot as plt
import numpy as np
from pylab import specgram, show

file = "C:\\Users\\Claire\\Projects\\magenta-ressources\\3-Audio 2 [2019-07-19 121135] mono.wav"

with wave.open(file, 'r') as wav_file:
  # Extract Raw Audio from Wav File
  signal = wav_file.readframes(-1)
  signal = np.fromstring(signal, 'Int16')

  # Get time from indices
  fs = wav_file.getframerate()

  plt.figure(num=None, figsize=(16, 6), dpi=80, facecolor='w', edgecolor='k')
  spectrogram = specgram(signal, Fs=fs, scale_by_freq=True, sides='default')
  show()
