"""
This example shows a basic Drums RNN generation with a hard coded primer.
"""
import math
import os
import time

import magenta.music as mm
from magenta.music import constants
from magenta.protobuf import generator_pb2, music_pb2
from visual_midi import Plotter


def generate(bundle_name: str,
             sequence_generator,
             generator_id: str,
             qpm: int = 120,
             primer_filename: str = None,
             total_length_bars: int = 4,
             temperature: float = 1.0,
             beam_size: int = 1,
             branch_factor: int = 1,
             steps_per_iteration: int = 1,
             write_midi_to_disk: bool = False,
             write_plot_to_disk: bool = False):
  """TODO doc"""

  # Downloads the bundle from the magenta website, a bundle (.mag file) is a
  # trained model that is used by magenta
  # TODO
  mm.notebook_utils.download_bundle(bundle_name, "bundles")
  bundle = mm.sequence_generator_bundle.read_bundle_file(
    os.path.join("bundles", bundle_name))

  # Initialize the generator "drum_kit", this need to fit the bundle we
  # downloaded before
  # TODO
  generator_map = sequence_generator.get_generator_map()
  generator = generator_map[generator_id](checkpoint=None, bundle=bundle)
  generator.initialize()

  # Creates a primer sequence that is fed into the model for the generator,
  # which will generate a sequence based on this one
  # TODO
  if primer_filename:
    primer_sequence = mm.midi_io.midi_file_to_note_sequence(
      os.path.join("primers", primer_filename))
  else:
    primer_sequence = music_pb2.NoteSequence()

  # TODO
  if primer_sequence.tempos:
    if len(primer_sequence.tempos) > 1:
      raise Exception("No support for multiple tempos")
    qpm = primer_sequence.tempos[0].qpm
  else:
    qpm = qpm

  # TODO
  if primer_sequence.time_signatures:
    if len(primer_sequence.time_signatures) > 1:
      raise Exception("No support for multiple time signatures")
    primer_time_signature = primer_sequence.time_signatures[0]
  else:
    primer_time_signature = primer_sequence.time_signatures.add()
    primer_time_signature.time = 0
    primer_time_signature.numerator = 4
    primer_time_signature.denominator = 4

  # We will generate 3 bars, so with a
  # 1 bar primer we'll have 4 bars total

  # The steps per quarter for this generator
  # is 4 steps per quarter
  # TODO
  seconds_per_step = 60.0 / qpm / generator.steps_per_quarter

  # We are using a default 16 steps per bar, which is
  # 4/4 music sampled at 4 steps per quarter note
  # num_steps_per_bar = constants.DEFAULT_STEPS_PER_BAR
  # TODO
  steps_per_quarter_note = constants.DEFAULT_STEPS_PER_QUARTER
  num_steps_per_bar = (primer_time_signature.numerator * steps_per_quarter_note)

  # We calculate how many seconds per bar for
  # the generation time
  # TODO
  seconds_per_bar = num_steps_per_bar * seconds_per_step

  print("Seconds per step: " + str(seconds_per_step))
  print("Steps per bar: " + str(num_steps_per_bar))
  print("Seconds per bar: " + str(seconds_per_bar))

  # We store those time because the generation
  # will start after the end of the primer
  # TODO
  primer_sequence_length_bars = math.ceil(primer_sequence.total_time /
                                          seconds_per_bar)
  primer_sequence_length_time = primer_sequence_length_bars * seconds_per_bar

  # TODO
  primer_start_time = 0
  primer_end_time = primer_start_time + primer_sequence_length_time - 0.00001

  # Calculate the generation time, if zero bar, raise exception
  # TODO
  generation_length_bars = total_length_bars - primer_sequence_length_bars
  if generation_length_bars <= 0:
    raise Exception("Total length in bars too small "
                    + "(" + str(total_length_bars) + ")"
                    + ", needs to be at least one bar bigger than primer "
                    + "(" + str(primer_sequence_length_bars) + ")")
  generation_length_time = generation_length_bars * seconds_per_bar

  # TODO
  generation_start_time = primer_end_time
  generation_end_time = generation_start_time + generation_length_time

  # TODO
  print("Primer start and end: ["
        + str(primer_start_time) + ", "
        + str(primer_end_time) + "]")
  print("Generation start and end: ["
        + str(generation_start_time) + ", "
        + str(generation_end_time) + "]")

  # The generator interface is common for all models
  # TODO
  generator_options = generator_pb2.GeneratorOptions()
  generator_options.args['temperature'].float_value = temperature
  generator_options.args['beam_size'].int_value = beam_size
  generator_options.args['branch_factor'].int_value = branch_factor
  generator_options.args['steps_per_iteration'].int_value = steps_per_iteration
  generator_options.generate_sections.add(
    start_time=generation_start_time,
    end_time=generation_end_time)

  # We are using the primer sequence here instead of an empty sequence,
  # the resulting sequence is a NoteSequence instance
  # TODO
  sequence = generator.generate(primer_sequence, generator_options)
  time_signature = sequence.time_signatures.add()
  time_signature.time = 0
  time_signature.numerator = primer_time_signature.numerator
  time_signature.denominator = primer_time_signature.denominator

  # Write the resulting midi file to the output directory
  if write_midi_to_disk:
    date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
    generator_name = str(generator.__class__).split(".")[2]
    midi_filename = "%s_%s_%s.mid" % (generator_name, generator_id,
                                      date_and_time)
    midi_path = os.path.join("output", midi_filename)
    mm.midi_io.note_sequence_to_midi_file(sequence, midi_path)
    print("Generated midi file: " + str(os.path.abspath(midi_path)))

  # Write the resulting plot file to the output directory
  if write_plot_to_disk:
    date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
    generator_name = str(generator.__class__).split(".")[2]
    plot_filename = "%s_%s_%s.html" % (generator_name, generator_id,
                                       date_and_time)
    plot_path = os.path.join("output", plot_filename)
    pretty_midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
    plotter = Plotter()
    plotter.save(pretty_midi, plot_path)
    print("Generated plot file: " + str(os.path.abspath(plot_path)))

  return sequence
