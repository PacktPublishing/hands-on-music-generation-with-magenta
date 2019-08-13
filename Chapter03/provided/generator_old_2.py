"""
This example shows a basic Drums RNN generation with a hard coded primer.
"""
import math
import os

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
             temperature: float = 1,
             write_midi_to_disk: bool = False,
             write_plot_to_disk: bool = False):
  """TODO doc"""

  # Downloads the bundle from the magenta website, a bundle (.mag file) is a
  # trained model that is used by magenta
  mm.notebook_utils.download_bundle(bundle_name, "bundles")
  bundle = mm.sequence_generator_bundle.read_bundle_file(
    os.path.join("bundles", bundle_name))

  # Initialize the generator "drum_kit", this need to fit the bundle we
  # downloaded before
  generator_map = sequence_generator.get_generator_map()
  generator = generator_map[generator_id](checkpoint=None, bundle=bundle)
  generator.initialize()

  # Creates a primer sequence that is fed into the model for the generator,
  # which will generate a sequence based on this one
  if primer_filename:
    primer_sequence = mm.midi_io.midi_file_to_note_sequence(
      os.path.join("primers", primer_filename))
  else:
    primer_sequence = music_pb2.NoteSequence()

  if primer_sequence and primer_sequence.tempos:
    qpm = primer_sequence.tempos[0].qpm
  else:
    qpm = qpm

  # We will generate 3 bars, so with a
  # 1 bar primer we'll have 4 bars total

  # The steps per quarter for this generator
  # is 4 steps per quarter
  seconds_per_step = 60.0 / qpm / generator.steps_per_quarter

  # We are using a default 16 steps per bar, which is
  # 4/4 music sampled at 4 steps per quarter note
  # num_steps_per_bar = constants.DEFAULT_STEPS_PER_BAR
  steps_per_quarter_note = constants.DEFAULT_STEPS_PER_QUARTER
  num_steps_per_bar = (primer_sequence.time_signatures[0].numerator
                       * steps_per_quarter_note)

  # We calculate how many seconds per bar for
  # the generation time
  seconds_per_bar = num_steps_per_bar * seconds_per_step

  print("Seconds per step: " + str(seconds_per_step))
  print("Seconds per bar: " + str(seconds_per_bar))

  # We store those time because the generation
  # will start after the end of the primer
  primer_sequence_length_bars = math.ceil(primer_sequence.total_time /
                                          seconds_per_bar)
  primer_sequence_length_time = primer_sequence_length_bars * seconds_per_bar

  primer_start_time = 0
  primer_end_time = primer_start_time + primer_sequence_length_time

  # TODO magenta.music.sequence_generator.SequenceGeneratorError: Got GenerateSection request for section that is before the end of the NoteSequence. This model can only extend sequences. Requested start time: 2.0535722499999998, Final note end time: 2.1331853770833336

  # Calculate the generation time, if zero bar, raise exception
  generation_length_bars = total_length_bars - primer_sequence_length_bars
  if generation_length_bars <= 0:
    raise Exception("Total length in bars too small "
                    "(" + str(total_length_bars) + ")"
               ", needs to be at least one bar bigger than primer "
               "(" + str(primer_sequence_length_bars) + ")")
  generation_length_time = generation_length_bars * seconds_per_bar

  # We calculate the generation start and end
  # for a duration of num_bars
  generation_start_time = primer_end_time
  generation_end_time = generation_start_time + generation_length_time

  # generation_start_time = primer_sequence.total_time

  print("Primer start and end: ["
        + str(primer_start_time) + ", "
        + str(primer_end_time) + "]")
  print("Generation start and end: ["
        + str(generation_start_time) + ", "
        + str(generation_end_time) + "]")

  # TODO another calculation is : https://guitargearfinder.com/guides/convert-ms-milliseconds-bpm-beats-per-minute-vice-versa/
  # If your song is in 3/4 time (three beats per bar) at a tempo of 150 bpm,
  # you know that there are 150 beats per minute. That means 0.4 seconds per
  # beat (60 seconds / 150 beats). There are three beats per bar, so one bar
  # lasts for 1.2 seconds (0.4 x 3).

  # TODO step and beat explain
  # qpm 167.9999328000269
  # 60/qpm*3 = 1.071429 (seconds per bar)
  # [pitch: 67
  # velocity: 64
  # end_time: 0.33854180208333334
  # , pitch: 60
  # velocity: 64
  # start_time: 0.357143
  # end_time: 0.6956848020833334
  # , pitch: 63
  # velocity: 64
  # start_time: 0.714286
  # end_time: 0.8831848770833334
  # , pitch: 65
  # velocity: 64
  # start_time: 0.8928575
  # end_time: 1.0617563770833334
  # , pitch: 67
  # velocity: 64
  # start_time: 1.071429
  # end_time: 1.4099708020833335
  # , pitch: 60
  # velocity: 64
  # start_time: 1.428572
  # end_time: 1.7671138020833335
  # , pitch: 63
  # velocity: 64
  # start_time: 1.785715
  # end_time: 1.9546138770833335
  # , pitch: 65
  # velocity: 64
  # start_time: 1.9642865
  # end_time: 2.1331853770833336
  # ]

  # The generator interface is common for all models
  generator_options = generator_pb2.GeneratorOptions()

  # Add a bit of temperature for more flavor
  print("Temperature: " + str(temperature))
  generator_options.args['temperature'].float_value = temperature

  # Defines the generation section
  generator_options.generate_sections.add(
    start_time=generation_start_time,
    end_time=generation_end_time)

  # We are using the primer sequence here instead of an empty sequence,
  # the resulting sequence is a NoteSequence instance
  sequence = generator.generate(primer_sequence, generator_options)
  time_signature = sequence.time_signatures.add()
  time_signature.time = 0
  time_signature.numerator = primer_sequence.time_signatures[0].numerator
  time_signature.denominator = primer_sequence.time_signatures[0].denominator

  # TODO see magenta.music.midi_io.midi_to_note_sequence

  # Write the resulting midi file to the output directory
  if write_midi_to_disk:
    midi_file = os.path.join("output", "out.mid")
    mm.midi_io.note_sequence_to_midi_file(sequence, midi_file)
    print("Generated midi file: " + str(os.path.abspath(midi_file)))

  # Write the resulting plot file to the output directory
  if write_plot_to_disk:
    plot_file = os.path.join("output", "out.html")
    pretty_midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
    plotter = Plotter()
    plotter.save(pretty_midi, plot_file)
    print("Generated plot file: " + str(os.path.abspath(plot_file)))

  return sequence
