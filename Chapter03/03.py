"""TODO polyphony_sequence_generator"""
import tensorflow as tf
from magenta.models.polyphony_rnn import polyphony_sequence_generator

from Chapter03 import generator


def app(unused_argv):
  generator.generate(
    "polyphony_rnn.mag",
    polyphony_sequence_generator,
    "polyphony",
    condition_on_primer=False,
    inject_primer_during_generation=False,
    temperature=0.9,
    branch_factor=1,
    primer_filename="Game_of_Thrones_Melody_Polyphonic.mid",
    write_midi_to_disk=True,
    write_plot_to_disk=True
  )

  generator.generate(
    "polyphony_rnn.mag",
    polyphony_sequence_generator,
    "polyphony",
    condition_on_primer=True,
    inject_primer_during_generation=False,
    temperature=0.9,
    branch_factor=1,
    primer_filename="Game_of_Thrones_Melody_Polyphonic.mid",
    write_midi_to_disk=True,
    write_plot_to_disk=True
  )

  generator.generate(
    "polyphony_rnn.mag",
    polyphony_sequence_generator,
    "polyphony",
    condition_on_primer=False,
    inject_primer_during_generation=True,
    temperature=0.9,
    branch_factor=1,
    primer_filename="Game_of_Thrones_Melody_Polyphonic.mid",
    write_midi_to_disk=True,
    write_plot_to_disk=True
  )

  generator.generate(
    "polyphony_rnn.mag",
    polyphony_sequence_generator,
    "polyphony",
    condition_on_primer=True,
    inject_primer_during_generation=True,
    temperature=0.9,
    branch_factor=1,
    primer_filename="Game_of_Thrones_Melody_Polyphonic.mid",
    write_midi_to_disk=True,
    write_plot_to_disk=True
  )

  return 0


if __name__ == "__main__":
  tf.app.run(app)
