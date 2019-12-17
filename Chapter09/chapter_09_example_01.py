"""
TODO
"""

import mido


def find_midi_ports():
  print(f"Input ports: {mido.get_input_names()}")
  print(f"Output ports: {mido.get_output_names()}")


if __name__ == "__main__":
  find_midi_ports()
