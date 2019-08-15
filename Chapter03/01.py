"""TODO melody_rnn_sequence_generator"""
import tensorflow as tf
from magenta.models.melody_rnn import melody_rnn_sequence_generator

from Chapter03 import generator2


def app(unused_argv):
  generator2.generate(
    "basic_rnn.mag",
    melody_rnn_sequence_generator,
    "basic_rnn",
    primer_filename="Fur_Elisa_Beethoveen_Monophonic.mid",
    total_length_steps=54,
    temperature=1,
    branch_factor=1,
    write_midi_to_disk=True,
    write_plot_to_disk=True)

  generator2.generate(
    "lookback_rnn.mag",
    melody_rnn_sequence_generator,
    "lookback_rnn",
    primer_filename="Fur_Elisa_Beethoveen_Monophonic.mid",
    total_length_steps=54,
    temperature=1,
    branch_factor=1,
    write_midi_to_disk=True,
    write_plot_to_disk=True
  )

  generator2.generate(
    "attention_rnn.mag",
    melody_rnn_sequence_generator,
    "attention_rnn",
    primer_filename="Fur_Elisa_Beethoveen_Monophonic.mid",
    total_length_steps=54,
    temperature=1,
    branch_factor=1,
    write_midi_to_disk=True,
    write_plot_to_disk=True
  )

  return 0


if __name__ == "__main__":
  tf.app.run(app)
