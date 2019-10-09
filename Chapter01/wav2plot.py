import sys
import wave

import matplotlib.pyplot as plt
import numpy as np


def plot_wav(file):
  with wave.open(file, 'r') as wav_file:
    # Extract Raw Audio from Wav File
    signal = wav_file.readframes(-1)
    signal = np.fromstring(signal, 'Int16')

    # Split the data into channels
    channels = [[] for channel in range(wav_file.getnchannels())]
    for index, datum in enumerate(signal):
      channels[index % len(channels)].append(datum)

    # Get time from indices
    fs = wav_file.getframerate()
    time = np.linspace(0, len(signal) / len(channels) / fs,
                       num=len(signal) / len(channels))

    # Plot
    plt.figure(num=None, figsize=(16, 6), dpi=80, facecolor='w', edgecolor='k')
    for channel in channels:
      plt.plot(time, channel)
    plt.show()


if __name__ == "__main__":
  for wav_file in sys.argv[1:]:
    print(f"Plotting wav file {wav_file}")
    plot_wav(wav_file)
  sys.exit(0)
