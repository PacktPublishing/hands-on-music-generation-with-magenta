# Chapter 9 - Making Magenta interact with music applications

[![Magenta Version 2.0.1](../docs/magenta-v2.0.1-badge.svg)](https://github.com/magenta/magenta/releases/tag/2.0.1)

This chapter will show how Magenta fits in a broader picture by showing how to make it interact with other music applications such as Digital Audio Workstations (DAWs) and synthesizers. We'll explain how to send MIDI sequences from Magenta to FluidSynth and DAWs using the MIDI interface. By doing so, we'll learn how to handle MIDI ports on all platforms and how to loop MIDI sequences in Magenta. We'll show how to synchronize multiple applications using MIDI clocks and transport information. Finally, we'll cover Magenta Studio, a standalone packaging of Magenta based on Magenta.js that can also integrate into Ableton Live as a plugin.

## Magenta Versioning

```diff
- A newer version of this code is available.
```

This branch shows the code for Magenta v1.1.7, which corresponds to the code in the book. For a more recent version, use the updated [Magenta v2.0.1 branch](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta/tree/magenta-v2.0.1/Chapter09).

## Code

Before you start, follow the [installation instructions for Magenta 2.0.1](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta/tree/master/Chapter01#installing-magenta).

### [Example 1](chapter_09_example_01.py)

Utility functions for finding and creating MIDI ports.

```bash
python chapter_09_example_01.py
```

### [Example 2](chapter_09_example_02.py)

This example shows a basic Drums RNN generation with synthesizer playback, using a MIDI hub to send the sequence to an external device.

```bash
python chapter_09_example_02.py --midi_port="midi_port_name"
```

### [Example 3](chapter_09_example_03.py)

This example shows a basic Drums RNN generation with a looping synthesizer playback, using a MIDI hub to send the sequence to an external device.

```bash
python chapter_09_example_03.py --midi_port="midi_port_name"
```

### [Example 4](chapter_09_example_04.py)

This example shows how to synchronize a Magenta application with an external device using MIDI clock and transport messages.

```bash
python chapter_09_example_04.py --midi_port="midi_port_name"
```

### [Example 5](chapter_09_example_05.py)

This example shows a basic Drums RNN generation with a looping synthesizer playback, generating a new sequence at each loop, using a MIDI hub to send the sequence to an external device.

```bash
python chapter_09_example_05.py --midi_port="midi_port_name"
```
