"""
This example shows how to synchronize a Magenta application with an external
device using MIDI clock and transport messages.
"""

import argparse
import time
from decimal import Decimal
from threading import Thread

import mido
from magenta.common.concurrency import Sleeper
from magenta.interfaces.midi.midi_hub import MidiHub

parser = argparse.ArgumentParser()
parser.add_argument("--midi_port", type=str, default="magenta_out")
args = parser.parse_args()


class Metronome(Thread):

  def __init__(self, outport, qpm):
    super(Metronome, self).__init__()
    self._message_clock = mido.Message(type='clock')
    self._message_start = mido.Message(type='start')
    self._message_stop = mido.Message(type='stop')
    self._message_reset = mido.Message(type='reset')
    self._outport = outport
    # Period of 4 ticks per bar, or 1 tick per beat
    self._period = Decimal(2.5) / qpm
    self._stop_signal = False

  def run(self):
    sleeper = Sleeper()

    # Sends reset and the start, we could also
    # use the "continue" message
    self._outport.send(self._message_reset)
    self._outport.send(self._message_start)

    # Loops until the stop signal is True
    while not self._stop_signal:
      # Calculates the next tick for current time
      now = Decimal(time.time())
      tick_number = max(0, int(now // self._period) + 1)
      tick_time = tick_number * self._period
      sleeper.sleep_until(float(tick_time))

      # Sends the clock message as soon it wakeup
      self._outport.send(self._message_clock)

      # Sends a stop message when finished
    self._outport.send(self._message_stop)

  def stop(self):
    self._stop_signal = True


def send_clock():
  # We find the proper input port for the software synth
  # (which is the output port for Magenta)
  output_ports = [name for name in mido.get_output_names()
                  if args.midi_port in name]
  if not output_ports:
    raise Exception(f"Cannot find proper output ports in: "
                    f"{mido.get_output_names()}")
  print(f"Sending clock to output port names: {output_ports}")

  # Start a new MIDI hub on that port (output only)
  midi_hub = MidiHub(input_midi_ports=[],
                     output_midi_ports=output_ports,
                     texture_type=None)
  outport = midi_hub._outport

  # Starts the metronome at 120 QPM
  metronome = Metronome(outport, 120)
  metronome.start()

  # Waits for 16 seconds and send the stop command
  metronome.join(timeout=16)
  metronome.stop()

  return 0


if __name__ == "__main__":
  send_clock()
