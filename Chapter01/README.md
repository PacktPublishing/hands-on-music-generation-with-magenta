# Chapter 01 - Introduction on Magenta and generative art

In this chapter, you’ll learn the basics of generative artwork and what already exists. You’ll learn about the new techniques of artwork generation, like machine learning, and how those techniques can be applied to produce music and art. Magenta will be introduced, along with Tensorflow, with an overview of its different parts and the installation of the required software for this book. We’ll finish the installation by generating a simple MIDI file on the command line.

The following topics will be covered in this chapter:

- Overview of generative artwork
- New techniques with Machine Learning
- Magenta and Tensorflow in music generation
- Installation of Magenta
- Generating a basic MIDI file

## Code

This chapter doesn't have any code, has it serves as an introduction to the book and an installation procedure. You can check out the [Jupyter Notebook](notebook.ipynb) to test your installation.

This chapter also provides [utility scripts](#utility-scripts) we'll be using throughout the book.

## Installing Magenta

Installing Magenta using Conda is easier. First [install Miniconda](https://conda.io/en/latest/miniconda.html), then:

```bash
# Create a new environment for Magenta with Python 3.5.x as interpreter
conda create --name magenta python=3.5

# Then activate it
conda activate magenta
```

Then you can install Magenta with:

```bash
# Installation
pip install magenta

## Test installation
python -c "import magenta; print(magenta.__version__)"
```

## Installing Magenta GPU

TODO compatibility version grid

## Utility Scripts

### [`midi2plot.py`](https://github.com/dubreuia/midi2plot)

Transforms a MIDI file to a plot, most of the diagram in this book has been done with this tool.

### `wav2plot.py`

Transforms a WAV file to a plot.

```bash
python wav2plot.py my_wav_file.wav
```

### `wav2spectrogram.py`

Transforms a WAV file to a spectrogram.

```bash
python wav2spectrogram.py my_wav_file.wav
```
