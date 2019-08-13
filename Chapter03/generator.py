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
             qpm: float = constants.DEFAULT_QUARTERS_PER_MINUTE,
             primer_filename: str = None,
             total_length_bars: int = 4,
             temperature: float = 1.0,
             beam_size: int = 1,
             branch_factor: int = 1,
             steps_per_iteration: int = 1,
             write_midi_to_disk: bool = False,
             write_plot_to_disk: bool = False) -> music_pb2.NoteSequence:
  """Generates and returns a new sequence given the sequence generator.

  Uses the bundle name to download the bundle in the "bundles" directory if it
  doesn't already exist, then uses the sequence generator and the generator id
  to get the generator. Parameters can be provided for the generation phase.
  The MIDI and plot files can be written to disk.

      :param bundle_name: The bundle name to be downloaded and generated with.

      :param sequence_generator: The sequence generator module, which is the
      python module in the corresponding models subfolder.

      :param generator_id: The id of the generator configuration, this is the
      model's configuration.

      :param qpm: The QPM for the generated sequence. If a primer is provided,
      the primer QPM will be used and this parameter ignored.

      :param primer_filename: The filename for the primer, which will be taken
      from the "primers" directory. If left empty, and empty note sequence will
      be used.

      :param total_length_bars: The total length of the sequence, which contains
      the added length of the primer and the generated sequence together. This
      value need to be bigger than the primer length in bars.

      :param temperature: The temperature value for the generation algorithm,
      lesser than 1 is less random (closer to the primer), bigger than 1 is
      more random

      :param beam_size: The beam size for the generation algorithm, a bigger
      branch size means the generation algorithm will generate more sequence
      each iteration, meaning a less random sequence at the cost of more time.

      :param branch_factor: The branch factor for the generation algorithm,
      a bigger branch factor means the generation algorithm will keep more
      sequence candidates at each iteration, meaning a less random sequence
      at the cost of more time.

      :param steps_per_iteration: The number of steps the generation algorithm
      generates at each iteration, a bigger steps per iteration meaning there
      are less iterations in total because more steps gets generated each time.

      :param write_midi_to_disk: True to write the resulting sequence to disk as
      a MIDI file in the "output" folder. The filename naming pattern is:
      "GeneratorName_GeneratorId_DateTime.mid".

      :param write_plot_to_disk: True to write the resulting plot to disk as
      a HTML file in the "output" folder. The filename naming pattern is:
      "GeneratorName_GeneratorId_DateTime.html".

      :returns The generated NoteSequence
  """

  # Downloads the bundle from the magenta website, a bundle (.mag file) is a
  # trained model that is used by magenta
  mm.notebook_utils.download_bundle(bundle_name, "bundles")
  bundle = mm.sequence_generator_bundle.read_bundle_file(
    os.path.join("bundles", bundle_name))

  # Initialize the generator from the generator id, this need to fit the
  # bundle we downloaded before, and choose the model's configuration.
  generator_map = sequence_generator.get_generator_map()
  generator = generator_map[generator_id](checkpoint=None, bundle=bundle)
  generator.initialize()

  # Gets the primer sequence that is fed into the model for the generator,
  # which will generate a sequence based on this one.
  # If no primer sequence is given, the primer sequence is initialized
  # to an empty note sequence
  if primer_filename:
    primer_sequence = mm.midi_io.midi_file_to_note_sequence(
      os.path.join("primers", primer_filename))
  else:
    primer_sequence = music_pb2.NoteSequence()

  # Gets the QPM from the primer sequence. If it wasn't provided, take the
  # parameters that defaults to Magenta's default
  if primer_sequence.tempos:
    if len(primer_sequence.tempos) > 1:
      raise Exception("No support for multiple tempos")
    qpm = primer_sequence.tempos[0].qpm
  else:
    qpm = qpm

  # Gets the time signature from the primer sequence. If it wasn't provided,
  # we initialize it to a default 4/4
  if primer_sequence.time_signatures:
    if len(primer_sequence.time_signatures) > 1:
      raise Exception("No support for multiple time signatures")
    primer_time_signature = primer_sequence.time_signatures[0]
  else:
    primer_time_signature = primer_sequence.time_signatures.add()
    primer_time_signature.time = 0
    primer_time_signature.numerator = 4
    primer_time_signature.denominator = 4

  # Calculates the seconds per 1 step, which changes depending on the QPM value
  # (steps per quarter in generators are mostly 4)
  seconds_per_step = 60.0 / qpm / generator.steps_per_quarter

  # Calculate the number of steps per bar, which changes from the time
  # signature. If we have a 3/4 time signature, steps per bar is 12,
  # if 4/4, steps per bar is 16.
  steps_per_quarter_note = constants.DEFAULT_STEPS_PER_QUARTER
  num_steps_per_bar = (primer_time_signature.numerator * steps_per_quarter_note)

  # Calculate how many seconds per bar for the generation time
  seconds_per_bar = num_steps_per_bar * seconds_per_step

  print("Seconds per step: " + str(seconds_per_step))
  print("Steps per bar: " + str(num_steps_per_bar))
  print("Seconds per bar: " + str(seconds_per_bar))

  # Calculates the primer sequence length in bars and time by taking the
  # total time (which is the end of the last note) and finding the next bar
  # start time.
  primer_sequence_length_bars = math.ceil(primer_sequence.total_time /
                                          seconds_per_bar)
  primer_sequence_length_time = primer_sequence_length_bars * seconds_per_bar

  # Calculates the start and the end of the primer sequence.
  # We add a negative delta to the end, because if we don't some generators
  # won't start the generation right at the beginning of the bar, they will
  # start at the next step, meaning we'll have a small gap between the primer
  # and the generated sequence.
  primer_end_adjust = (0.00001 if primer_sequence_length_time > 0 else 0)
  primer_start_time = 0
  primer_end_time = (primer_start_time
                     + primer_sequence_length_time
                     - primer_end_adjust)

  # Calculates the generation time by taking the total time and substracting
  # the primer time. The resulting generation time needs to be bigger than zero.
  generation_length_bars = total_length_bars - primer_sequence_length_bars
  if generation_length_bars <= 0:
    raise Exception("Total length in bars too small "
                    + "(" + str(total_length_bars) + ")"
                    + ", needs to be at least one bar bigger than primer "
                    + "(" + str(primer_sequence_length_bars) + ")")
  generation_length_time = generation_length_bars * seconds_per_bar

  # Calculates the generate start and end time, the start time will contain
  # the previously added negative delta from the primer end time.
  # We remove the generation end time delta to end the generation
  # on the last bar.
  generation_start_time = primer_end_time
  generation_end_time = (generation_start_time
                         + generation_length_time
                         + primer_end_adjust)

  # Showtime
  print("Primer time: ["
        + str(primer_start_time) + ", "
        + str(primer_end_time) + "]")
  print("Generation time: ["
        + str(generation_start_time) + ", "
        + str(generation_end_time) + "]")

  # Pass the given parameters, the generator options are common for all models.
  generator_options = generator_pb2.GeneratorOptions()
  generator_options.args['temperature'].float_value = temperature
  generator_options.args['beam_size'].int_value = beam_size
  generator_options.args['branch_factor'].int_value = branch_factor
  generator_options.args['steps_per_iteration'].int_value = steps_per_iteration
  generator_options.generate_sections.add(
    start_time=generation_start_time,
    end_time=generation_end_time)

  # Generates the sequence. The resulting sequence do not have time signature
  # so we add the same as the primer.
  sequence = generator.generate(primer_sequence, generator_options)
  time_signature = sequence.time_signatures.add()
  time_signature.time = 0
  time_signature.numerator = primer_time_signature.numerator
  time_signature.denominator = primer_time_signature.denominator

  # Writes the resulting midi file to the output directory
  if write_midi_to_disk:
    date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
    generator_name = str(generator.__class__).split(".")[2]
    midi_filename = "%s_%s_%s.mid" % (generator_name, generator_id,
                                      date_and_time)
    midi_path = os.path.join("output", midi_filename)
    mm.midi_io.note_sequence_to_midi_file(sequence, midi_path)
    print("Generated midi file: " + str(os.path.abspath(midi_path)))

  # Writes the resulting plot file to the output directory
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
