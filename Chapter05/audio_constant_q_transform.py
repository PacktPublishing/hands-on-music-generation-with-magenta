import glob

import librosa

from audio_utils import save_spectogram_plot

if __name__ == "__main__":
  filenames = glob.glob("output/nsynth/*.wav")
  for filename in filenames:
    audio, _ = librosa.load(filename, sr=16000)
    save_spectogram_plot(audio,
                         filename=filename.replace(".wav", ".png"),
                         output_dir=".")
