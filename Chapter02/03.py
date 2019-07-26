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

from Chapter01.provided.midi2plot import plot_midi


def app(unused_argv):
  """TODO app"""

  mm.notebook_utils.download_bundle("drum_kit_rnn.mag", "bundles")
  bundle = mm.sequence_generator_bundle.read_bundle_file(
    os.path.join("bundles", "drum_kit_rnn.mag"))

  generator_map = drums_rnn_sequence_generator.get_generator_map()
  sequence_generator = generator_map["drum_kit"](checkpoint=None, bundle=bundle)
  sequence_generator.initialize()

  primer_drums = magenta.music.DrumTrack(
    [frozenset(pitches) for pitches in [(36,), (), (), (), (46,)]])
  primer_sequence = primer_drums.to_sequence(qpm=120)

  qpm = 120

  # TODO Parameters
  output_file = os.path.join("output", "out.html")
  # TODO Parameters
  bar_per_loop = 2
  # TODO Parameters
  num_loops = 4
  # TODO
  hub = midi_hub.MidiHub(["magenta_in 1"],
                         ["VirtualMIDISynth #1 0"],
                         midi_hub.TextureType.POLYPHONIC)

  # TODO
  interaction = LooperMidi(
    hub,
    sequence_generator,
    primer_sequence,
    output_file=output_file,
    qpm=qpm,
    bar_per_loop=bar_per_loop,
    num_loops=num_loops,
  )
  interaction.start()
  interaction.join()

  return 0


# TODO use constructor parameters for bpm, etc.
class LooperMidi(threading.Thread):

  def __init__(self,
               midi_hub,
               sequence_generator,
               primer_sequence,
               output_file=os.path.join("output", "out.html"),
               qpm=120,
               bar_per_loop=1,
               num_loops=2):
    super(LooperMidi, self).__init__()
    self._midi_hub = midi_hub
    self._sequence_generator = sequence_generator
    self._primer_sequence = primer_sequence
    self._output_file = output_file
    self._qpm = qpm
    self._bar_per_loop = bar_per_loop
    self._num_loops = num_loops

  def run(self):
    # TODO
    sequence = self._primer_sequence
    player = self._midi_hub.start_playback(sequence, allow_updates=True)

    # TODO
    seconds_per_step = 60.0 / self._qpm / self._sequence_generator.steps_per_quarter
    num_steps_per_bar = self._sequence_generator.steps_per_quarter * 2
    seconds_per_bar = num_steps_per_bar * seconds_per_step
    seconds_per_loop = self._bar_per_loop * seconds_per_bar

    # TODO MOVE
    pm = pretty_midi.PrettyMIDI()
    pm.instruments.append(pretty_midi.Instrument(0))

    # TODO MOVE
    plot_max_bar = 16

    # TODO
    wall_start_time = time.time()

    # TODO
    for bar_count in range(0, sys.maxsize):
      # TODO
      cursor_time = bar_count * seconds_per_loop

      # TODO
      sequence_adjusted = music_pb2.NoteSequence()
      sequence_adjusted.CopyFrom(sequence)
      sequence_adjusted = adjust_sequence_times(sequence_adjusted,
                                                wall_start_time)
      player.update_sequence(sequence_adjusted, start_time=cursor_time)

      # TODO MOVE
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
      loop_start_time = cursor_time
      loop_end_time = loop_start_time + seconds_per_loop
      generation_start_time = loop_end_time
      generation_end_time = generation_start_time + seconds_per_loop
      generator_options = generator_pb2.GeneratorOptions()
      generator_options.args['temperature'].float_value = 1
      generator_options.generate_sections.add(
        start_time=generation_start_time,
        end_time=generation_end_time)

      # TODO
      if bar_count % self._num_loops == 0:
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
