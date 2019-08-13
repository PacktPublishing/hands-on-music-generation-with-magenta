import tensorflow as tf
from magenta.models.improv_rnn import improv_rnn_sequence_generator

from Chapter03 import generator


def app(unused_argv):
  # generator.generate(
  #   "chord_pitches_improv.mag",
  #   improv_rnn_sequence_generator,
  #   "basic_improv",
  #   primer_filename="Game_of_Thrones_Melody_Polyphonic.mid",
  #   total_length_bars=16,
  #   temperature=0.75,
  #   branch_factor=1,
  #   write_midi_to_disk=True,
  #   write_plot_to_disk=True
  # )
  #
  # generator.generate(
  #   "chord_pitches_improv.mag",
  #   improv_rnn_sequence_generator,
  #   "attention_improv",
  #   primer_filename="Game_of_Thrones_Melody_Polyphonic.mid",
  #   total_length_bars=16,
  #   temperature=0.75,
  #   branch_factor=1,
  #   write_midi_to_disk=True,
  #   write_plot_to_disk=True
  # )

  # TODO some things to be aware of
  # - no more than one melodies improv_rnn_sequence_generator.py:103
  # - chords and melodies start on the same step improv_rnn_sequence_generator.py:133

  # TODO not working
  generator.generate(
    "chord_pitches_improv.mag",
    improv_rnn_sequence_generator,
    "chord_pitches_improv",
    # primer_filename="Game_of_Thrones_Melody_Polyphonic.mid",
    total_length_bars=16,
    temperature=0.75,
    branch_factor=1,
    write_midi_to_disk=True,
    write_plot_to_disk=True
  )

  return 0


if __name__ == "__main__":
  tf.app.run(app)
