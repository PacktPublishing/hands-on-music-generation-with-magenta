import tensorflow as tf
from magenta.models.melody_rnn import melody_rnn_sequence_generator

from Chapter03 import generator


def app(unused_argv):
  generator.generate(
    "basic_rnn.mag",
    melody_rnn_sequence_generator,
    "basic_rnn",
    primer_filename="Game_of_Thrones_Melody_Monophonic.mid",
    total_length_bars=16,
    temperature=0.75,
    branch_factor=1,
    write_midi_to_disk=True,
    write_plot_to_disk=True
  )

  generator.generate(
    "lookback_rnn.mag",
    melody_rnn_sequence_generator,
    "lookback_rnn",
    primer_filename="Game_of_Thrones_Melody_Monophonic.mid",
    total_length_bars=16,
    temperature=0.75,
    branch_factor=1,
    write_midi_to_disk=True,
    write_plot_to_disk=True
  )

  generator.generate(
    "attention_rnn.mag",
    melody_rnn_sequence_generator,
    "attention_rnn",
    primer_filename="Game_of_Thrones_Melody_Monophonic.mid",
    total_length_bars=16,
    temperature=0.75,
    branch_factor=1,
    write_midi_to_disk=True,
    write_plot_to_disk=True
  )

  return 0


if __name__ == "__main__":
  tf.app.run(app)
