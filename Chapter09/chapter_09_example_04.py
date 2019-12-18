import time
from threading import Thread

import mido
from magenta.common.concurrency import Sleeper
from magenta.interfaces.midi import midi_hub as mh


# TODO check import names midi_hub


class Metronome(Thread):

  def __init__(self,
               outport,
               qpm,
               start_time=0,
               stop_time=None):
    self._outport = outport
    self._message = mido.Message(type='clock')
    self.update(qpm, start_time, stop_time)
    super(Metronome, self).__init__()

  def update(self, qpm, start_time=0, stop_time=None):
    self._period = 2.5 / qpm
    self._start_time = start_time
    self._stop_time = stop_time

  def run(self):
    sleeper = Sleeper()
    while True:
      now = time.time()
      tick_number = max(0, int((now - self._start_time) // self._period) + 1)
      tick_time = tick_number * self._period + self._start_time

      if self._stop_time is not None and self._stop_time < tick_time:
        break

      sleeper.sleep_until(tick_time)
      self._outport.send(self._message)

  def stop(self, stop_time=0, block=True):
    self._stop_time = stop_time
    if block:
      self.join()


def send_clock():
  input_ports = [name for name in mido.get_output_names()
                 if "magenta_out" in name]
  if not input_ports:
    raise Exception(f"Cannot find proper input port in: "
                    f"{mido.get_output_names()}")
  midi_hub = mh.MidiHub([], input_ports, None)
  outport = midi_hub._outport
  metronome = Metronome(outport, 120)
  metronome.start()
  metronome.join()


if __name__ == "__main__":
  send_clock()
