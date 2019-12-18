"""
This example shows a basic Drums RNN generation with a
looping synthesizer playback.
"""

import os
import time
from decimal import Decimal

import magenta.music as mm
import mido
import tensorflow as tf
from magenta.common import concurrency
from magenta.interfaces.midi import midi_hub as mh
from magenta.interfaces.midi.midi_interaction import adjust_sequence_times
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.music import constants
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2
from visual_midi import Plotter


# TODO check import names midi_hub

def generate(unused_argv):
  mm.notebook_utils.download_bundle("drum_kit_rnn.mag", "bundles")
  bundle = mm.sequence_generator_bundle.read_bundle_file(
    os.path.join("bundles", "drum_kit_rnn.mag"))

  generator_map = drums_rnn_sequence_generator.get_generator_map()
  generator = generator_map["drum_kit"](checkpoint=None, bundle=bundle)
  generator.initialize()

  qpm = 120
  num_bars = 3
  seconds_per_step = 60.0 / qpm / generator.steps_per_quarter
  num_steps_per_bar = constants.DEFAULT_STEPS_PER_BAR
  seconds_per_bar = num_steps_per_bar * seconds_per_step

  primer_sequence = mm.midi_io.midi_file_to_note_sequence(
    os.path.join("primers", "Jazz_Drum_Basic_1_bar.mid"))
  primer_start_time = 0
  primer_end_time = primer_start_time + seconds_per_bar

  generation_start_time = primer_end_time
  generation_end_time = generation_start_time + (seconds_per_bar * num_bars)

  generator_options = generator_pb2.GeneratorOptions()
  generator_options.args['temperature'].float_value = 1.1
  generator_options.generate_sections.add(
    start_time=generation_start_time,
    end_time=generation_end_time)

  sequence = generator.generate(primer_sequence, generator_options)

  os.makedirs("output", exist_ok=True)
  plot_file = os.path.join("output", "out.html")
  pretty_midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
  plotter = Plotter()
  plotter.show(pretty_midi, plot_file)
  print(f"Generated plot file: {os.path.abspath(plot_file)}")

  input_ports = [name for name in mido.get_output_names()
                 if "magenta_out" in name]
  if not input_ports:
    raise Exception(f"Cannot find proper input port in: "
                    f"{mido.get_output_names()}")
  print(f"Playing generated MIDI in input port names: {input_ports}")

  midi_hub = mh.MidiHub([], input_ports, None)

  empty_sequence = music_pb2.NoteSequence()
  player = midi_hub.start_playback(empty_sequence,
                                   allow_updates=True)
  player._channel = 9
  outport = midi_hub._outport
  message_clock = mido.Message(type='clock')
  message_start = mido.Message(type='start')
  message_stop = mido.Message(type='stop')
  message_reset = mido.Message(type='reset')

  # We calculate the length of the generated sequence in seconds,
  # which gives up the loop time in seconds
  loop_time = generation_end_time - primer_start_time
  print(f"Loop time is {loop_time}")

  sleeper = concurrency.Sleeper()
  # TODO One time per bar
  period = Decimal(240) / qpm
  period = period * (num_bars + 1)
  while True:
    try:
      # TODO
      now = Decimal(time.time())
      tick_number_next = max(0, int(now // period) + 1)
      tick_number = tick_number_next - 1
      tick_time_next = tick_number_next * period
      tick_time = tick_number * period

      # TODO
      sequence_adjusted = music_pb2.NoteSequence()
      sequence_adjusted.CopyFrom(sequence)
      sequence_adjusted = adjust_sequence_times(sequence_adjusted,
                                                float(tick_time))
      # TODO
      player.update_sequence(sequence_adjusted,
                             start_time=float(tick_time))

      # TODO
      sleeper.sleep_until(float(tick_time_next))
    except KeyboardInterrupt:
      print(f"Stopping")
      return 0


if __name__ == "__main__":
  tf.app.run(generate)
