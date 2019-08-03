"""
TODO see section from book
"""

import os

import magenta.music as mm
import tensorflow as tf
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2
from visual_midi import Plotter


def generate(unused_argv):
  """Generates a basic drum sequence of 4 seconds"""

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

  # Change the number of steps to be generated, which will define the length
  # of the generated sequence, used with the qpm. At 120 qpm, this
  # is equal to 4 seconds
  num_steps = 32
  # Change the temperature: the bigger this value, the more random is the
  # generation, with 1 being the default value, 1.25 being more random,
  # 0.75 being less random
  temperature = 1
  # Change the quarter per minute (also called BPM or beat per minute), a
  # measure of tempo. At 120 qpm, you have two beat per seconds
  qpm = 120

  # Calculate the number of seconds per step, useful to find the total time
  # of the generation in seconds. The steps per quarter in the generator is by
  # default 4, so the generator will generate 8 steps per bar
  # TODO why 8 steps per bar
  seconds_per_step = 60.0 / qpm / generator.steps_per_quarter
  total_seconds = num_steps * seconds_per_step

  # The generator options are the parameters passed to the generator, why is
  # the temperature and the generation section, from 0 to the total of seconds,
  # where the generator will generate notes
  generator_options = generator_pb2.GeneratorOptions()
  generator_options.args['temperature'].float_value = temperature
  generator_options.generate_sections.add(start_time=0, end_time=total_seconds)

  # Generates the notes from the arguments, starting with an empty note
  # sequence (no primer)
  empty_note_sequence = music_pb2.NoteSequence()
  sequence = generator.generate(empty_note_sequence, generator_options)

  # Outputs the midi file in the output directory
  midi_file = os.path.join("output", "out.mid")
  mm.midi_io.note_sequence_to_midi_file(sequence, midi_file)
  print("Generated midi file: " + str(os.path.abspath(midi_file)))

  # Outputs the plot file in the output directory and opens your browser for
  # visualisation
  plot_file = os.path.join("output", "out.html")
  print("Generated plot file: " + str(os.path.abspath(plot_file)))
  pretty_midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
  plotter = Plotter()
  plotter.show(pretty_midi, plot_file)

  return 0


if __name__ == "__main__":
  tf.app.run(generate)
