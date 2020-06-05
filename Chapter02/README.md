# Chapter 2 - Generating drum sequences with DrumsRNN

[![Magenta Version 2.0.1](../docs/magenta-v2.0.1-badge.svg)](https://github.com/magenta/magenta/releases/tag/2.0.1)

This chapter will show you what many consider the foundation of music—percussion. We'll show the importance of Recurrent Neural Networks (RNNs) for music generation. You'll then learn how to use the Drums RNN model using a pre-trained drum kit model, by calling it in the command-line window and directly in Python, to generate drum sequences.  We'll introduce the different model parameters, including the model's MIDI encoding, and show how to interpret the output of the model.

## Code

Before you start, follow the [installation instructions for Magenta 2.0.1](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta/tree/master/Chapter01#installing-magenta).

### [Example 1](chapter_02_example_01.py) or [notebook](notebook.ipynb)

This example shows a basic Drums RNN generation with a hard coded primer. For the Python script, while in the Magenta environment (`conda activate magenta`):

```bash
# Runs a Drums RNN generation and shows the resulting plot in the browser
python chapter_02_example_01.py
```

For the Jupyter notebook:

```bash
jupyter notebook notebook.ipynb
```

### [Example 2](chapter_09_example_02.py)

This example shows a basic Drums RNN generation with synthesizer playback. For the Python script, you'll need to first install and configure a software synthesizer, then while in the Magenta environment (`conda activate magenta`):

```bash
# Runs a Drums RNN generation, shosw the resulting plot in the browser, and
# plays it in a sofware synth
python chapter_02_example_02.py
```

### [Example 3](chapter_02_example_03.py)

This example shows a basic Drums RNN generation with a looping synthesizer playback. For the Python script, you'll need to first install and configure a software synthesizer, then while in the Magenta environment (`conda activate magenta`):

```bash
# Runs a Drums RNN generation, shosw the resulting plot in the browser, and
# plays it in a sofware synth
python chapter_02_example_03.py
```
