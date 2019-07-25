import sys
import wave

import matplotlib.pyplot as plt
import numpy as np
from pylab import specgram, show


def plot_wav(file):
  with wave.open(file, 'r') as wav_file:
    # Extract Raw Audio from Wav File
    signal = wav_file.readframes(-1)
    signal = np.fromstring(signal, 'Int16')

    # Get time from indices
    fs = wav_file.getframerate()

    plt.figure(num=None, figsize=(16, 6), dpi=80, facecolor='w', edgecolor='k')
    specgram(signal, Fs=fs, scale_by_freq=True, sides='default')
    show()


if __name__ == "__main__":
  for wav_file in sys.argv[1:]:
    print("Plotting wav file " + wav_file)
    plot_wav(wav_file)
  sys.exit(0)
