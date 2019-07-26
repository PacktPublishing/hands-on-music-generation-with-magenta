"""
This example shows a basic Drums RNN generation with a hard coded primer.
"""

import os

import magenta
import magenta.music as mm
import tensorflow as tf
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.protobuf import generator_pb2

from Chapter01.provided.midi2plot import Plotter


def generate(unused_argv):
  """Generates a basic drum sequence of 4 seconds based on a hard coded
  primer"""

  mm.notebook_utils.download_bundle("drum_kit_rnn.mag", "bundles")
  bundle = mm.sequence_generator_bundle.read_bundle_file(
    os.path.join("bundles", "drum_kit_rnn.mag"))

  generator_map = drums_rnn_sequence_generator.get_generator_map()
  generator = generator_map["drum_kit"](checkpoint=None, bundle=bundle)
  generator.initialize()

  num_steps = 32
  temperature = 1
  qpm = 120

  seconds_per_step = 60.0 / qpm / generator.steps_per_quarter
  total_seconds = num_steps * seconds_per_step

  # Creates a primer sequence that is fed into the model for the generator,
  # which will generate a sequence based on this one
  # A DrumTrack models a drum sequence by step, so you have step 1 being the
  # midi note 36 (bass drum), followed by 3 steps of silence (those four steps
  # constitutes the first beat or quarter), followed by both notes 36 and 41
  # being struck at the same time (followed by silence by these are optional)
  # TODO why quarter
  # TODO better example
  # TODO check midi note meaning
  primer_drums = magenta.music.DrumTrack(
    [frozenset(pitches) for pitches in
     [(36,), (), (), (), (36, 41), (), (), ()]])
  primer_sequence = primer_drums.to_sequence(qpm=120)
  primer_end_time = primer_sequence.total_time

  # Defines the start and end of the generation, which starts at the step
  # after the end of the primer (we'll see in 03.py this calculation makes
  # it harder to fall on proper beats) and ends at total seconds
  # The complete generation will thus contain the primer and the total length
  # needs to be at least the size of the primer
  generation_start_time = primer_end_time + seconds_per_step
  generation_end_time = total_seconds

  generator_options = generator_pb2.GeneratorOptions()
  generator_options.args['temperature'].float_value = temperature
  generator_options.generate_sections.add(
    start_time=generation_start_time,
    end_time=generation_end_time)

  # We are using the primer sequence here instead of an empty sequence
  sequence = generator.generate(primer_sequence, generator_options)

  midi_file = os.path.join("output", "out.mid")
  mm.midi_io.note_sequence_to_midi_file(sequence, midi_file)
  print("Generated midi file: " + str(os.path.abspath(midi_file)))

  plot_file = os.path.join("output", "out.html")
  print("Generated plot file: " + str(os.path.abspath(plot_file)))
  pretty_midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
  plotter = Plotter()
  plotter.show(pretty_midi, plot_file)

  return 0


if __name__ == "__main__":
  tf.app.run(generate)
