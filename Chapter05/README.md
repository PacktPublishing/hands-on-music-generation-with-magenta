# Chapter 5 - Audio generation with NSynth and GANSynth

This chapter will show audio generation. We'll first provide an overview of WaveNet, an existing model for audio generation, especially efficient in text to speech applications. In Magenta, we'll use NSynth, a Wavenet Autoencoder model, to generate small audio clips, that can serve as instruments for a backing MIDI score. NSynth also enables audio transformation like scaling, time stretching and interpolation. We'll also use GANSynth, a faster approach based on generative adversarial network (GAN).

## Utils

There are some audio utilities in the [audio_utils.py](./audio_utils.py) file, useful for saving and loading the encodings (`save_encoding` and `load_encodings`), time stretching (`timestretch`) them and saving spectrogram plots (`save_spectrogram_plot` and `save_rainbowgram_plot`).

## Sounds and MIDI

We provide some sound samples and MIDI files for the examples.

- [midi/cs1-1pre-short.mid](./midi/cs1-1pre-short.mid) (from http://www.jsbach.net/midi/cs1-1pre.mid")
- [sounds/83249__zgump__bass-0205__crop.wav](./sounds/83249__zgump__bass-0205__crop.wav) (from https://freesound.org/people/zgump/sounds/83249/)
- [sounds/160045__jorickhoofd__metal-hit-with-metal-bar-resonance__crop.wav](./sounds/160045__jorickhoofd__metal-hit-with-metal-bar-resonance__crop.wav) (from https://freesound.org/people/jorickhoofd/sounds/160045/)
- [sounds/412017__skymary__cat-meow-short__crop.wav](./sounds/412017__skymary__cat-meow-short__crop.wav) (from https://freesound.org/people/skymary/sounds/412017/)
- [sounds/427567__maria-mannone__flute__crop.wav](./sounds/427567__maria-mannone__flute__crop.wav) (from https://freesound.org/people/Maria_Mannone/sounds/427567/)

## Code

### [Example 1](chapter_05_example_01.py)

This example shows how to use NSynth to interpolate between pairs of sounds.

```bash
# Runs the example, the output audio will be in the "output/nsynth" folder
python chapter_05_example_01.py
```

### [Example 2](chapter_05_example_02.py)

This example shows how to use GANSynth to generate intruments for a backing
score from a MIDI file.

```bash
# Runs the example, the output audio will be in the "output/gansynth" folder
python chapter_05_example_02.py
```
