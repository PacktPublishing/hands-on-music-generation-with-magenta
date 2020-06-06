# Chapter 4 - Latent space interpolation with MusicVAE 

[![Magenta Version 1.1.7](../docs/magenta-v1.1.7-badge.svg)](https://github.com/magenta/magenta/releases/tag/1.1.7)

This chapter will show the importance of continuous latent space of Variational Autoencoders (VAEs) and its importance in music generation compared to standard Autoencoders (AEs). We'll use the MusicVAE model, a hierarchical recurrent VAE, from Magenta to sample sequences and then interpolate between them, effectively morphing smoothly from one to another. We'll then see how to add groove, or humanization, to an existing sequence, using the GrooVAE model. We'll finish by looking at the TensorFlow code used to build the VAE model.

## Magenta Versioning

```diff
- A newer version of this code is available.
```

This branch shows the code for Magenta v1.1.7, which corresponds to the code in the book. For a more recent version, use the updated [Magenta v2.0.1 branch](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta/tree/magenta-v2.0.1/Chapter04).

## Code

Before you start, follow the [installation instructions for Magenta 1.1.7](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta/tree/master/Chapter01#installing-magenta).

### [Example 1](chapter_04_example_01.py) or [notebook](notebook.ipynb)

This example shows how to sample, interpolate and humanize a drums sequence using MusicVAE and various configurations. For the Python script, while in the Magenta environment (`conda activate magenta`):

```bash
# Runs the example, the output files (plot, midi) will be in the "output" folder
python chapter_04_example_01.py
```

For the Jupyter notebook:

```bash
jupyter notebook notebook.ipynb
```

### [Example 2](chapter_04_example_02.py)

This example shows how to sample and interpolate a melody sequence using MusicVAE and various configurations. For the Python script, while in the Magenta environment (`conda activate magenta`):

```bash
# Runs the example, the output files (plot, midi) will be in the "output" folder
python chapter_04_example_02.py
```

### [Example 3](chapter_04_example_03.py)

This example shows how to sample a trio (drums, melody, bass) sequence using MusicVAE and various configurations. For the Python script, while in the Magenta environment (`conda activate magenta`):

```bash
# Runs the example, the output files (plot, midi) will be in the "output" folder
python chapter_04_example_03.py
```
