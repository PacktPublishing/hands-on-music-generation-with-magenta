import os

import magenta
import tensorflow as tf
from bokeh.io import output_file, show
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.music import midi_io
from magenta.music import notebook_utils
from magenta.music import sequence_generator_bundle
from magenta.protobuf import generator_pb2

from Chapter01.midi2plot import plot_midi


def generate(unused_argv):
  # Bundle TODO describe
  notebook_utils.download_bundle("drum_kit_rnn.mag", "bundles")
  bundle = sequence_generator_bundle.read_bundle_file(
    os.path.join("bundles", "drum_kit_rnn.mag"))

  # Generator TODO describe
  generator_map = drums_rnn_sequence_generator.get_generator_map()
  generator = generator_map["drum_kit"](checkpoint=None, bundle=bundle)
  generator.initialize()

  # TODO describe
  primer_drums = magenta.music.DrumTrack(
    [frozenset(pitches) for pitches in [(36,), (), (), (), (46,), (), (), ()]])
  primer_sequence = primer_drums.to_sequence(qpm=120)

  # TODO describe
  qpm = 120

  # TODO describe
  # steps_per_quarter = 4
  seconds_per_step = 60.0 / qpm / generator.steps_per_quarter

  # TODO describe
  num_steps = 32

  # TODO describe
  total_seconds = num_steps * seconds_per_step

  # TODO describe
  # TODO same as min / max in 02
  primer_end_time = primer_sequence.total_time

  # TODO describe
  start_time = primer_end_time + seconds_per_step
  end_time = total_seconds

  # TODO describe
  generator_options = generator_pb2.GeneratorOptions()
  generator_options.generate_sections.add(
    start_time=1,
    end_time=end_time)

  # TODO describe
  generator_options.args['temperature'].float_value = 1
  generator_options.args['beam_size'].int_value = 1
  generator_options.args['branch_factor'].int_value = 1
  generator_options.args['steps_per_iteration'].int_value = 1

  # TODO describe
  sequence = generator.generate(primer_sequence, generator_options)

  # TODO print
  last_end_time = max(n.end_time for n in sequence.notes)
  first_start_time = min(n.start_time for n in sequence.notes)
  primer_length = last_end_time - first_start_time
  print("seconds_per_step: " + str(seconds_per_step))
  print("num_steps: " + str(num_steps))
  print("total_seconds: " + str(total_seconds))
  print("primer_end_time: " + str(primer_end_time))
  print("start_time: " + str(start_time))
  print("end_time: " + str(end_time))
  print("last_end_time: " + str(last_end_time))
  print("first_start_time: " + str(first_start_time))
  print("primer_length: " + str(primer_length))

  # TODO describe
  midi_file = os.path.join("output", "out.mid")
  midi_io.note_sequence_to_midi_file(sequence, midi_file)
  print(midi_file)

  # TODO describe
  plot_file = os.path.join("output", "out.html")
  print(plot_file)
  pm = midi_io.note_sequence_to_pretty_midi(sequence)
  output_file(plot_file)
  plot = plot_midi(pm)
  show(plot)

  return 0


if __name__ == "__main__":
  tf.app.run(generate)
