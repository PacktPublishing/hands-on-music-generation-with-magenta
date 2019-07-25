import os
import sys
import threading
import time

import magenta
import magenta.music as mm
import tensorflow as tf
from bokeh.io import output_file, show
from magenta.interfaces.midi.magenta_midi import midi_hub
from magenta.interfaces.midi.midi_interaction import adjust_sequence_times
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2

from Chapter01.midi2plot import plot_midi




def app(unused_argv):
  # Initialize MidiHub.
  hub = midi_hub.MidiHub(["magenta_in 1"],
                         ["VirtualMIDISynth #1 0"],
                         midi_hub.TextureType.POLYPHONIC)

  # TODO ex
  # Bundle TODO describe
  mm.notebook_utils.download_bundle("drum_kit_rnn.mag", "bundles")
  bundle = mm.sequence_generator_bundle.read_bundle_file(
    os.path.join("bundles", "drum_kit_rnn.mag"))

  # Generator TODO describe
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
    magenta.music.DrumTrack([frozenset([36])])
    primer_drums = magenta.music.DrumTrack(
      [frozenset(pitches) for pitches in [(36,), (), (), (), (46,)]])
    sequence = primer_drums.to_sequence(qpm=120)

    player = self._midi_hub.start_playback(
      sequence, allow_updates=True)

    wall_start_time = time.time()

    # TODO describe
    qpm = 120

    # TODO describe
    # steps_per_quarter = 4
    seconds_per_step = 60.0 / qpm / self._sequence_generator.steps_per_quarter

    # TODO describe
    num_steps = 16

    # TODO describe
    total_seconds = num_steps * seconds_per_step

    # TODO describe
    primer_end_time = sequence.total_time

    # TODO describe
    start_time = primer_end_time + seconds_per_step
    end_time = total_seconds

    # TODO loop
    num_loops = 4

    for index in range(0, sys.maxsize):
      tick_wall_start_time = time.time()

      # TODO describe
      tick_start_time = start_time + index * total_seconds
      tick_end_time = end_time + index * total_seconds

      # TODO describe
      generator_options = generator_pb2.GeneratorOptions()
      generator_options.generate_sections.add(
        start_time=tick_start_time,
        end_time=tick_end_time)

      # TODO describe
      generator_options.args['temperature'].float_value = 0.1
      generator_options.args['beam_size'].int_value = 1
      generator_options.args['branch_factor'].int_value = 1
      generator_options.args['steps_per_iteration'].int_value = 1

      # TODO describe
      print("index: " + str(index))
      print("primer_end_time: " + str(primer_end_time))
      print("start_time: " + str(start_time))
      print("tick_start_time: " + str(tick_start_time))
      print("end_time: " + str(end_time))
      print("tick_end_time: " + str(tick_end_time))
      print("wall_start_time: " + str(wall_start_time))
      print("tick_wall_start_time: " + str(tick_wall_start_time))
      print("tick_wall_start_time (adjusted): "
            + str(tick_wall_start_time - wall_start_time))
      sequence = self._sequence_generator.generate(sequence, generator_options)
      # sequence = mm.trim_note_sequence(sequence, 1, 2)

      sequence_adjusted = music_pb2.NoteSequence()
      sequence_adjusted.CopyFrom(sequence)
      sequence_adjusted = adjust_sequence_times(sequence_adjusted,
                                                wall_start_time)
      player.update_sequence(sequence_adjusted, start_time=tick_wall_start_time)

      pm = mm.midi_io.note_sequence_to_pretty_midi(sequence)
      output_file(self._output_file)
      plot = plot_midi(pm)
      show(plot)

      time.sleep(total_seconds -
                 ((time.time() - wall_start_time) % total_seconds))


if __name__ == "__main__":
  tf.app.run(app)
