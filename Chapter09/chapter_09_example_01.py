"""
Utility functions for finding and creating MIDI ports.
"""

import mido
from magenta.interfaces.midi.midi_hub import MidiHub


def find_midi_ports():
  print(f"Input ports: {mido.get_input_names()}")
  print(f"Output ports: {mido.get_output_names()}")


def create_virtual_midi_ports():
  MidiHub(input_midi_ports=["magenta_in"],
          output_midi_ports=["magenta_out"],
          texture_type=None)


if __name__ == "__main__":
  find_midi_ports()
  # create_virtual_midi_ports()
