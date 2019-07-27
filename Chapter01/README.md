# Chapter 01 - Introduction on Magenta and generative art

This chapter doesn't have any code, has it serves as an introduction to the book and an installation procedure. You can check out the [Jupyter Notebook](notebook.ipynb) to test your installation.

This chapter also provides [utility scripts](#utility-scripts) we'll be using thoughout the book.

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

## Installing Magenta

Installing Magenta using Conda is easier. Install Miniconda at https://conda.io/en/latest/miniconda.html, then:

```bash
# With conda installed, create a new environment for Magenta:
conda create --name magenta python=3.5

# Then activate it
conda activate magenta
```

Then you can install Magenta with:

```bash
# Installation
pip install magenta

## Test installation
python
>>> import magenta
>>> magenta.__version__
'1.1.2'
```

We won't be covering Magenta GPU installation here, please refer to the book.
