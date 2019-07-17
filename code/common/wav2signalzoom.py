import wave

import math
import matplotlib.pyplot as plt
import numpy as np

file = "C:\\Users\\Claire\\Projects\\magenta-ressources\\3-Audio 2 [2019-07-19 121135] mono.wav"

with wave.open(file, 'r') as wav_file:
  # Extract Raw Audio from Wav File
  signal = wav_file.readframes(-1)
  signal = np.fromstring(signal, 'Int16')
  signal = signal[
           math.floor(len(signal) * 0.251):math.floor(len(signal) * 0.2511)]

  # Split the data into channels
  channels = [[] for channel in range(wav_file.getnchannels())]
  for index, datum in enumerate(signal):
    channels[index % len(channels)].append(datum)

  # Get time from indices
  fs = wav_file.getframerate()
  time = np.linspace(0, len(signal) / len(channels) / fs,
                     num=len(signal) / len(channels))

  # Plot
  plt.figure(num=None, figsize=(3, 3), dpi=80, facecolor='w', edgecolor='k')
  for channel in channels:
    plt.plot(time, channel)
  plt.show()
