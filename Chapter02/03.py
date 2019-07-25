import os
import sys
import threading
import time

import magenta
import magenta.music as mm
import pretty_midi
import tensorflow as tf
from bokeh.io import output_file, show
from magenta.interfaces.midi.magenta_midi import midi_hub
from magenta.interfaces.midi.midi_interaction import adjust_sequence_times
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.music import sequences_lib
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2

from Chapter01.midi2plot import plot_midi


def app(unused_argv):
  # TODO
  hub = midi_hub.MidiHub(["magenta_in 1"],
                         ["VirtualMIDISynth #1 0"],
                         midi_hub.TextureType.POLYPHONIC)

  # TODO
  mm.notebook_utils.download_bundle("drum_kit_rnn.mag", "bundles")
  bundle = mm.sequence_generator_bundle.read_bundle_file(
    os.path.join("bundles", "drum_kit_rnn.mag"))

  # TODO
  generator_map = drums_rnn_sequence_generator.get_generator_map()
  generator = generator_map["drum_kit"](checkpoint=None, bundle=bundle)
  generator.initialize()

  output_file = os.path.join("output", "out.html")

  interaction = LooperMidi(
    hub, generator, output_file)
  interaction.start()
  interaction.join()

  return 0


class LooperMidi(threading.Thread):

  def __init__(self, midi_hub, sequence_generator, output_file):
    super(LooperMidi, self).__init__()
    self._midi_hub = midi_hub
    self._sequence_generator = sequence_generator
    self._output_file = output_file

  def run(self):
    # TODO
    primer_drums = magenta.music.DrumTrack(
      [frozenset(pitches) for pitches in [(36,), (), (), (), (46,)]])
    sequence = primer_drums.to_sequence(qpm=120)

    # TODO
    player = self._midi_hub.start_playback(sequence, allow_updates=True)

    # TODO
    qpm = 120

    # TODO
    # steps_per_quarter = 4
    seconds_per_step = 60.0 / qpm / self._sequence_generator.steps_per_quarter

    # TODO
    num_steps_per_bar = 8
    seconds_per_bar = num_steps_per_bar * seconds_per_step

    # TODO
    bar_per_loop = 2
    seconds_per_loop = bar_per_loop * seconds_per_bar

    # TODO
    num_loops = 4

    # TODO
    wall_start_time = time.time()

    # TODO
    pm = pretty_midi.PrettyMIDI()
    pm.instruments.append(pretty_midi.Instrument(0))

    # TODO
    plot_max_bar = 16

    # TODO
    for bar_count in range(0, sys.maxsize):
      # TODO
      tick_wall_start_time = time.time()

      # TODO
      cursor_time = bar_count * seconds_per_loop
      loop_start_time = cursor_time
      loop_end_time = loop_start_time + seconds_per_loop
      generation_start_time = loop_end_time
      generation_end_time = generation_start_time + seconds_per_loop

      # TODO
      print("bar_count: " + str(bar_count))
      print("cursor_time: " + str(cursor_time))
      print("loop_start_time: " + str(loop_start_time))
      print("loop_end_time: " + str(loop_end_time))
      print("generation_start_time: " + str(generation_start_time))
      print("generation_end_time: " + str(generation_end_time))
      print("tick_wall_start_time: " + str(tick_wall_start_time))
      print("tick_wall_start_time (adjusted): "
            + str(tick_wall_start_time - wall_start_time))

      # TODO
      sequence_adjusted = music_pb2.NoteSequence()
      sequence_adjusted.CopyFrom(sequence)
      sequence_adjusted = adjust_sequence_times(sequence_adjusted,
                                                wall_start_time)
      player.update_sequence(sequence_adjusted, start_time=cursor_time)

      # TODO
      pm_sequence = mm.midi_io.note_sequence_to_pretty_midi(sequence)
      for instrument in pm_sequence.instruments:
        for index, note in enumerate(instrument.notes):
          pm.instruments[0].notes.append(note)
      min_time = int(pm.get_end_time() - plot_max_bar + 1)
      remove = []
      for instrument in pm.instruments:
        for index, note in enumerate(instrument.notes):
          if (note.start < min_time):
            remove.append(note)
      [pm.instruments[0].notes.remove(note) for note in remove]
      output_file(self._output_file)
      plot = plot_midi(pm)
      show(plot)

      # TODO
      generator_options = generator_pb2.GeneratorOptions()
      generator_options.generate_sections.add(
        start_time=generation_start_time,
        end_time=generation_end_time)

      # TODO
      generator_options.args['temperature'].float_value = 1

      # TODO
      if bar_count % num_loops == 0:
        print("GENERATING")
        sequence = self._sequence_generator.generate(
          sequence, generator_options)
        sequence = sequences_lib.trim_note_sequence(
          sequence, generation_start_time, generation_end_time)
      else:
        print("LOOPING")
        sequence = sequences_lib.trim_note_sequence(
          sequence, loop_start_time, loop_end_time)
        sequence = sequences_lib.shift_sequence_times(
          sequence, seconds_per_loop)

      # TODO 1 wake up per bar
      sleep_time = seconds_per_loop - (
          (time.time() - wall_start_time) % seconds_per_loop)
      time.sleep(sleep_time)


if __name__ == "__main__":
  tf.app.run(app)
