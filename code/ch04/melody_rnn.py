import os

from bokeh.io import output_file, show
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.music import notebook_utils
from magenta.music import plot_sequence
from magenta.music import sequence_generator_bundle
from magenta.music import sequence_proto_to_midi_file
from magenta.music import sequence_proto_to_pretty_midi
from magenta.protobuf import generator_pb2
from magenta.protobuf import music_pb2

from datetime import datetime

# Model name one of: [basic_rnn, mono_rnn, lookback_rnn, attention_rnn]
MODEL_NAME = "attention_rnn"

# Bundle name is drum_kit_rnn
BUNDLE_NAME = MODEL_NAME + ".mag"

# Constants
DATETIME = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
BUNDLE_DIR = "bundles"
OUTPUT_DIR = "output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
MIDI_FILE = OUTPUT_DIR + "/" + MODEL_NAME + "_" + DATETIME + ".mid"
PLOT_FILE = OUTPUT_DIR + "/" + MODEL_NAME + "_" + DATETIME + ".html"

# The higher the value, the more random is the generated sequence
# 1.0 is the default value ; 1.25 is more random ; 0.75 is less random
TEMPERATURE = 1.0

# The primer sequence TODO describe

# Bundle TODO describe
notebook_utils.download_bundle(BUNDLE_NAME, BUNDLE_DIR)
bundle = sequence_generator_bundle.read_bundle_file(os.path.join(BUNDLE_DIR, BUNDLE_NAME))

# Generator TODO describe
generator_map = melody_rnn_sequence_generator.get_generator_map()
generator = generator_map[MODEL_NAME](checkpoint=None, bundle=bundle)
generator.initialize()

# Generator options TODO describe
generator_options = generator_pb2.GeneratorOptions()
generator_options.args["temperature"].float_value = TEMPERATURE

# TODO is this unused?
generate_section = generator_options.generate_sections.add(start_time=0, end_time=30)

# Generate the sequence TODO describe
sequence = generator.generate(music_pb2.NoteSequence(), generator_options)

# Outputs the midi file TODO describe
midi_file = sequence_proto_to_midi_file(sequence, MIDI_FILE)
midi_file_pretty = sequence_proto_to_pretty_midi(sequence)
# https://stackoverflow.com/questions/6030087/play-midi-files-in-python

# Outputs the plot file TODO describe
plot = plot_sequence(sequence, False)
output_file(PLOT_FILE)
show(plot)
