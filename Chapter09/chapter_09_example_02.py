"""
This example shows a basic Drums RNN generation with synthesizer playback,
using a MIDI hub to send the sequence to an external device.
"""
import argparse
import os
import time

import magenta.music as mm
import mido
import tensorflow as tf
from magenta.interfaces.midi.midi_hub import MidiHub
from magenta.interfaces.midi.midi_interaction import adjust_sequence_times
from magenta.models.drums_rnn import drums_rnn_sequence_generator
from magenta.music import constants
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2
from visual_midi import Plotter

parser = argparse.ArgumentParser()
parser.add_argument("--midi_port", type=str, default="FLUID Synth")
args = parser.parse_args()


def generate(unused_argv):
  # Downloads the bundle from the magenta website
  mm.notebook_utils.download_bundle("drum_kit_rnn.mag", "bundles")
  bundle = mm.sequence_generator_bundle.read_bundle_file(
    os.path.join("bundles", "drum_kit_rnn.mag"))

  # Initialize the generator "drum_kit"
  generator_map = drums_rnn_sequence_generator.get_generator_map()
  generator = generator_map["drum_kit"](checkpoint=None, bundle=bundle)
  generator.initialize()

  # Define constants
  qpm = 120
  num_bars = 3
  seconds_per_step = 60.0 / qpm / generator.steps_per_quarter
  num_steps_per_bar = constants.DEFAULT_STEPS_PER_BAR
  seconds_per_bar = num_steps_per_bar * seconds_per_step

  # Use a priming sequence
  primer_sequence = mm.midi_io.midi_file_to_note_sequence(
    os.path.join("primers", "Jazz_Drum_Basic_1_bar.mid"))
  primer_start_time = 0
  primer_end_time = primer_start_time + seconds_per_bar

  # Calculates the generation start and end time
  generation_start_time = primer_end_time
  generation_end_time = generation_start_time + (seconds_per_bar * num_bars)
  generator_options = generator_pb2.GeneratorOptions()
  generator_options.args['temperature'].float_value = 1.1
  generator_options.generate_sections.add(
    start_time=generation_start_time,
    end_time=generation_end_time)

  # Generates on primer sequence
  sequence = generator.generate(primer_sequence, generator_options)

  # Outputs the plot
  os.makedirs("output", exist_ok=True)
  plot_file = os.path.join("output", "out.html")
  pretty_midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
  plotter = Plotter()
  plotter.show(pretty_midi, plot_file)
  print(f"Generated plot file: {os.path.abspath(plot_file)}")

  # We find the proper input port for the software synth
  # (which is the output port for Magenta)
  output_ports = [name for name in mido.get_output_names()
                  if args.midi_port in name]
  if not output_ports:
    raise Exception(f"Cannot find proper output ports in: "
                    f"{mido.get_output_names()}")
  print(f"Playing generated MIDI in output port names: {output_ports}")

  # Start a new MIDI hub on that port (output only)
  midi_hub = MidiHub(input_midi_ports=[],
                     output_midi_ports=output_ports,
                     texture_type=None)

  # Start on a empty sequence, allowing the update of the
  # sequence for later. We don't especially need that right
  # now, because we could play the sequence immediately, but
  # it will be useful for later examples to have a player to
  # update new sequences with.
  empty_sequence = music_pb2.NoteSequence()
  player = midi_hub.start_playback(empty_sequence,
                                   allow_updates=True)
  # Remember that GM 1 compatible synthesizer will play the drums
  # sound bank if the MIDI channel is 10 (but the channel is zero
  # indexed in Magenta MIDI hub so you have to use 9).
  player._channel = 9

  # Now we can play our sequence, but we need to adjust it first.
  # The MIDI player will play the sequence according to wall time,
  # but our sequence starts at 0.
  # Create a new empty note sequence, copy the sequence
  # we want to play in the empty sequence, then move the
  # start of the sequence by wall_start_time amount
  wall_start_time = time.time()
  sequence_adjusted = music_pb2.NoteSequence()
  sequence_adjusted.CopyFrom(sequence)
  sequence_adjusted = adjust_sequence_times(sequence_adjusted,
                                            wall_start_time)

  # The update sequence is the equivalent of "play"
  player.update_sequence(sequence_adjusted,
                         start_time=wall_start_time)

  # We "join" on the thread, meaning the call will block
  # until the player has finished. Because the thread
  # never stops, this call will block indefinitely. By
  # adding a timeout of generation_end_time, the call will
  # return after the end of the sequence being played.
  try:
    print(f"Playing for {generation_end_time}")
    player.join(generation_end_time)
  except KeyboardInterrupt:
    # The KeyboardInterrupt is important if you want to press
    # CTRL-C during the playback to stop the player.
    print(f"Stopping")
    return 0


if __name__ == "__main__":
  tf.app.run(generate)
