# Chapter 1 - Introduction on Magenta and generative art

[![Magenta Version 2.0.1](../docs/magenta-v2.0.1-badge.svg)](https://github.com/magenta/magenta/releases/tag/2.0.1)

This chapter will show you the basics of generative music and what already exists. You'll learn about the new techniques of artwork generation, such as machine learning, and how those techniques can be applied to produce music and art. Google's Magenta open source research platform will be introduced, along with Google's open source machine learning platform TensorFlow, along with an overview of its different parts and the installation of the required software for this book. We'll finish the installation by generating a simple MIDI file on the command line.

## Magenta Versioning

```diff
- A newer version of this code is available.
```

This branch shows the code for Magenta v1.1.7, which corresponds to the code in the book. For a more recent version, use the updated [Magenta v2.0.1 branch](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta/tree/magenta-v2.0.1/Chapter01).

## Code

This chapter doesn't have any code, since it serves as an introduction to the book and as an installation procedure. You can check out the [Jupyter Notebook](notebook.ipynb) to test your installation.

## Installing Magenta

Installing Magenta using Conda is easier. First [install Miniconda](https://conda.io/en/latest/miniconda.html), then:

```bash
# Create a new environment for Magenta with Python 3.6.x as interpreter
conda create --name magenta python=3.6

# Then activate it
conda activate magenta
```

Then you can install Magenta Version 2.0.1 and the dependencies for the book using:

```bash
pip install magenta==2.0.1 visual_midi tables
```

We're using version 2.0.1 for this code repository. You might be able to follow the examples using another version, but since Magenta's code changes quite a lot, imports might change depending on the version.

```bash
# Check Magenta versoin
python -c "import magenta; print(magenta.__version__)"
## 2.0.1

# Check Tensorflow versoin
python -c "import tensorflow; print(tensorflow.__version__)"
## 2.2.0
```

## Utility Scripts

### [Visual MIDI](https://github.com/dubreuia/visual_midi)

Transforms a MIDI file to a plot, most of the diagram in this book has been done with this tool.

### `wav2plot.py`

Transforms a WAV file to a plot.

```bash
# The script will open the output plot file
python wav2plot.py "my_wav_file.wav"
```

### `wav2spectrogram.py`

Transforms a WAV file to a spectrogram.

```bash
# The script will open the output plot file
python wav2spectrogram.py "my_wav_file.wav"
```
