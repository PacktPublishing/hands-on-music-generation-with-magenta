"""
This example shows a basic Drums RNN generation with a hard coded primer.
"""

import os

import magenta.music as mm
import tensorflow as tf
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.music import constants
from magenta.protobuf import generator_pb2
from visual_midi import Plotter


def generate(unused_argv):
  # Downloads the bundle from the magenta website, a bundle (.mag file) is a
  # trained model that is used by magenta
  mm.notebook_utils.download_bundle("drum_kit_rnn.mag", "bundles")
  bundle = mm.sequence_generator_bundle.read_bundle_file(
    os.path.join("bundles", "drum_kit_rnn.mag"))

  # Initialize the generator "drum_kit", this need to fit the bundle we
  # downloaded before
  generator_map = drums_rnn_sequence_generator.get_generator_map()
  generator = generator_map["drum_kit"](checkpoint=None, bundle=bundle)
  generator.initialize()

  # We will generate 3 bars, so with a
  # 1 bar primer we'll have 4 bars total
  num_bars = 3
  qpm = 120

  # The steps per quarter for this generator
  # is 4 steps per quarter
  seconds_per_step = 60.0 / qpm / generator.steps_per_quarter

  # We are using a default 16 steps per bar, which is
  # 4/4 music sampled at 4 steps per quarter note
  num_steps_per_bar = constants.DEFAULT_STEPS_PER_BAR

  # We calculate how many seconds per bar for
  # the generation time
  seconds_per_bar = num_steps_per_bar * seconds_per_step

  print("Seconds per step: " + str(seconds_per_step))
  print("Seconds per bar: " + str(seconds_per_bar))

  # Creates a primer sequence that is fed into the model for the generator,
  # which will generate a sequence based on this one
  # A DrumTrack models a drum sequence by step, so you have step 1 being the
  # midi note 36 (bass drum), followed by 3 steps of silence (those four steps
  # constitutes the first beat or quarter), followed by both notes 36 and 41
  # being struck at the same time (followed by silence by these are optional)
  primer_drums = mm.DrumTrack(
    [frozenset(pitches) for pitches in
     [(38, 51), (), (36,), (),
      (38, 44, 51), (), (36,), (),
      (), (), (38,), (),
      (38, 44), (), (36, 51), (), ]])
  primer_sequence = primer_drums.to_sequence(qpm=qpm)

  # We store those time because the generation
  # will start after the end of the primer
  primer_start_time = 0
  primer_end_time = primer_start_time + seconds_per_bar

  # We calculate the generation start and end
  # for a duration of num_bars
  generation_start_time = primer_end_time
  generation_end_time = generation_start_time + (seconds_per_bar * num_bars)

  print("Primer start and end: ["
        + str(primer_start_time) + ", "
        + str(primer_end_time) + "]")
  print("Generation start and end: ["
        + str(generation_start_time) + ", "
        + str(generation_end_time) + "]")

  # The generator interface is common for all models
  generator_options = generator_pb2.GeneratorOptions()

  # Add a bit of temperature for more flavor
  temperature = 1.1
  print("Temperature: " + str(temperature))
  generator_options.args['temperature'].float_value = temperature

  # Defines the generation section
  generator_options.generate_sections.add(
    start_time=generation_start_time,
    end_time=generation_end_time)

  # We are using the primer sequence here instead of an empty sequence,
  # the resulting sequence is a NoteSequence instance
  sequence = generator.generate(primer_sequence, generator_options)

  # Write the resulting midi file to the output directory
  midi_file = os.path.join("output", "out.mid")
  mm.midi_io.note_sequence_to_midi_file(sequence, midi_file)
  print("Generated midi file: " + str(os.path.abspath(midi_file)))

  # Write the resulting plot file to the output directory
  plot_file = os.path.join("output", "out.html")
  print("Generated plot file: " + str(os.path.abspath(plot_file)))
  pretty_midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
  plotter = Plotter()
  plotter.show(pretty_midi, plot_file)

  return 0


if __name__ == "__main__":
  tf.app.run(generate)
