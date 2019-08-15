"""TODO performance_sequence_generator"""
import tensorflow as tf
from magenta.models.performance_rnn import performance_sequence_generator

from Chapter03 import generator


def app(unused_argv):
  generator.generate(
    "performance_with_dynamics.mag",
    performance_sequence_generator,
    "performance_with_dynamics",
    total_length_bars=8,
    temperature=1,
    branch_factor=1,
    write_midi_to_disk=True,
    write_plot_to_disk=True
  )

  return 0


if __name__ == "__main__":
  tf.app.run(app)
