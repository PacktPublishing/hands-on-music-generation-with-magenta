


# Hands-On Music Generation with Magenta

[![Magenta Version 1.1.7](./docs/magenta-v1.1.7-badge.svg)](https://github.com/magenta/magenta/releases/tag/1.1.7)

In Hands-On Music Generation with Magenta, we explore the role of deep learning in music generation and assisted music composition. Design and use machine learning models for music generation using Magenta and make them interact with existing music creation tools.

<p align="center">
<img width="33%" alt="Music Generation With Magenta Book Cover" title="Music Generation With Magenta Book Cover" src="./docs/music-generation-with-magenta-book-cover.jpeg">
<p>

## Links

- **[Packt Publishing](https://www.packtpub.com/eu/data/hands-on-music-generation-with-magenta) - Buy the book in ebook format or paperback**
- [Code in Action](https://www.youtube.com/playlist?list=PLWPX7CYPrFFqvJW-vPU0puAo8vqyzq0A6) - Videos that shows the code examples being executed and the resulting generation.
- [Amazon Kindle](https://www.amazon.com/Hands-Music-Generation-Magenta-composition-ebook/dp/B0847S8R48) or [Amazon Paperback](https://www.amazon.com/Hands-Music-Generation-Magenta-composition/dp/1838824413) - Also available on Amazon

## Table of Contents

- [Chapter 1 - Introduction on Magenta and generative art](Chapter01)
- [Chapter 2 - Generating drum sequences with Drums RNN](Chapter02)
- [Chapter 3 - Generating polyphonic melodies](Chapter03)
- [Chapter 4 - Latent space interpolation with Music VAE](Chapter04)
- [Chapter 5 - Audio generation with GANSynth](Chapter05)
- [Chapter 6 - Data preparation and pipelines](Chapter06)
- [Chapter 7 - Training an existing model on a specific style](Chapter07)
- [Chapter 8 - Magenta in the browser with Magenta.js](Chapter08)
- [Chapter 9 - Making Magenta interact with music applications](Chapter09)

## How to cite

```
@book{book,
    author    = {DuBreuil, Alexandre},
    title     = {Hands-On Music Generation with Magenta},
    publisher = {Packt Publishing Ltd.},
    address   = {Birmingham, UK},
    year      = 2020,
    isbn      = "9781838824419"
}
```

## Magenta Versioning

In the book, we use Magenta 1.1.7, but we provide updated code here, up to Magenta 2.1.2. The `master` branch corresponds to Magenta 1.1.7, and the `magenta-master` branch corresponds to Magenta 2.1.2 (for now). On the `magenta-master` branch, you can check the modifications (on the first example, for example) to migrate from 1.1.7 to 2.1.2 using:

```bash
git diff master Chapter02/chapter_02_example_01.py`
```

You can see what Magenta version you should be using by looking at the badge at the top of the README and in the Python files.

- [**Magenta v1.1.7** (in the `master` branch)](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta) - The book's code uses Magenta 1.1.7 which, at the time of publication, was the latest stable available version. The code for that version is in the default `master` branch and will stay there.
- [**Magenta HEAD (master)** (in the `magenta-master` branch)](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta/tree/magenta-master) - We also provide the code for newer versions of Magenta, we try to keep the code up-to-date when new (breaking) versions of Magenta are released.
    - [**Magenta v2.0.1** (the `magenta-v2.0.1` tag)](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta/releases/tag/magenta-v2.0.1) - Corresponds to [Magenta 2.0.1](https://github.com/magenta/magenta/releases/tag/2.0.1), should work with all 2.0.x versions (depends on Tensorflow 2.2.0)
    - [**Magenta v2.1.2** (the `magenta-v2.1.2` tag)](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta/releases/tag/magenta-v2.1.2) - Corresponds to [Magenta v2.1.2](https://github.com/magenta/magenta/releases/tag/v2.1.2), should work with all 2.1.x versions (depends on Tensorflow 2.3.1)
  
## Python Compatibility

We've only tested Magenta using Python 3.6 as interpreter. Magenta v2.x could work with more recent versions of Python but we didn't test them (see [Chapter01](Chapter01) for installation information).

## Windows Compatibility

Magenta 1.1.7 works on Windows, but there seems to be problems from Magenta 2.x onwards (see [#11](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta/issues/11) for more details)

  
## Errata
  
* Page 10: _Pen and paper generative music_ section: **minute** should be **minuet**
* Page 10: _Pen and paper generative music_ section: a total of **two** will output the measure 32 _should be_ a total of **three** will output the measure 32
### Download a free PDF

 <i>If you have already purchased a print or Kindle version of this book, you can get a DRM-free PDF version at no cost.<br>Simply click on the link to claim your free PDF.</i>
<p align="center"> <a href="https://packt.link/free-ebook/9781838824419">https://packt.link/free-ebook/9781838824419 </a> </p>