# Chapter 5 - Audio generation with GANSynth

TODO The length in samples of the output wave files (can be calculated by multiplying the desired number of seconds by 16000).

## Utils

```python
import os
import librosa
import glob
from audio_utils import save_rainbowgram_plot

for path in glob.glob("output/nsynth/*.wav"):
  audio, _ = librosa.load(path, 16000)
  filename = os.path.basename(path)
  output_dir = os.path.join("output", "nsynth", "plots")
  print(f"Writing rainbowgram for {path} in {output_dir}")
  save_rainbowgram_plot(audio,
                        filename=filename.replace(".wav", "_rainbowgram.png"),
                        output_dir=output_dir)
```

## Timing

ex1:

- GPU 1060 with encodings --- 231.81045055389404 seconds ---
- GPU 1060 without encodings --- 234.3661847114563 seconds ---

ex2:

- GPU 1060: --- 37.21484565734863 seconds ---

## Scripts

scripts/tile.sh:

```bash
# The result will be in output/nsynth/plots/tile.png
./scripts/tile_images.sh output/nsynth/plots
```

## Refs

- rainbowgram adapted from https://gist.github.com/jesseengel/e223622e255bd5b8c9130407397a0494

## Copyrights

TODO

- http://www.jsbach.net/midi/cs1-1pre.mid
- 83249__zgump__bass-0205__crop.wav
- 160045__jorickhoofd__metal-hit-with-metal-bar-resonance__crop.wav
- 412017__skymary__cat-meow-short__crop.wav
- 427567__maria-mannone__flute__crop.wav
