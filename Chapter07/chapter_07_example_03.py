"""
Configuration for the Drums RNN model that inverts the snares and bass drums.
"""

import tensorflow as tf
from magenta.models.drums_rnn.drums_rnn_model import default_configs
from magenta.models.shared.events_rnn_model import EventSequenceRnnConfig
from magenta.music import LookbackEventSequenceEncoderDecoder
from magenta.music import MultiDrumOneHotEncoding
from magenta.protobuf.generator_pb2 import GeneratorDetails

INVERTED_DRUM_TYPE_PITCHES = [
  # kick drum (inverted from snare drum)
  [38, 27, 28, 31, 32, 33, 34, 37, 39, 40, 56, 65, 66, 75, 85],

  # snare drum (inverted from kick drum)
  [36, 35],
]

inverted_drum_kit = EventSequenceRnnConfig(
  GeneratorDetails(
    id='inverted_drum_kit',
    description='Drums RNN with inverted drums and binary counters.'
  ),
  LookbackEventSequenceEncoderDecoder(
    MultiDrumOneHotEncoding(INVERTED_DRUM_TYPE_PITCHES, True),
    lookback_distances=[],
    binary_counter_bits=6),
  tf.contrib.training.HParams(
    batch_size=128,
    rnn_layer_sizes=[256, 256, 256],
    dropout_keep_prob=0.5,
    attn_length=64,
    clip_norm=3,
    learning_rate=0.001))

default_configs['inverted_drum_kit'] = inverted_drum_kit
