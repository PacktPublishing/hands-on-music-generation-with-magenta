"""
Configuration for the MusicVAE model, using the MIDI bass programs.
"""

import tensorflow as tf
from magenta.common import merge_hparams
from magenta.models.music_vae import Config
from magenta.models.music_vae import MusicVAE
from magenta.models.music_vae import lstm_models
from magenta.models.music_vae.configs import CONFIG_MAP
from magenta.models.music_vae.data import BASS_PROGRAMS
from magenta.models.music_vae.data import NoteSequenceAugmenter
from magenta.models.music_vae.data import OneHotMelodyConverter
from magenta.models.music_vae.music_vae_train import FLAGS
from magenta.models.music_vae.music_vae_train import run

CONFIG_MAP["cat-bass_2bar_small"] = Config(
  model=MusicVAE(lstm_models.BidirectionalLstmEncoder(),
                 lstm_models.CategoricalLstmDecoder()),
  hparams=merge_hparams(
    lstm_models.get_default_hparams(),
    tf.contrib.training.HParams(
      batch_size=512,
      max_seq_len=32,
      z_size=256,
      enc_rnn_size=[512],
      dec_rnn_size=[256, 256],
      free_bits=0,
      max_beta=0.2,
      beta_rate=0.99999,
      sampling_schedule="inverse_sigmoid",
      sampling_rate=1000,
    )),
  note_sequence_augmenter=NoteSequenceAugmenter(transpose_range=(-5, 5)),
  data_converter=OneHotMelodyConverter(
    valid_programs=BASS_PROGRAMS,
    skip_polyphony=False,
    max_bars=100,
    slice_bars=2,
    steps_per_quarter=4),
  train_examples_path=None,
  eval_examples_path=None,
)


def main(unused_argv):
  run(CONFIG_MAP)


if __name__ == "__main__":
  tf.logging.set_verbosity(FLAGS.log)
  tf.app.run(main)
