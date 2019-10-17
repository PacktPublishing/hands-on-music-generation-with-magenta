import os

import magenta.music as mm
import tensorflow as tf
from magenta.models.gansynth.lib import flags as lib_flags
from magenta.models.gansynth.lib import model as lib_model
from magenta.models.gansynth.lib.generate_util import combine_notes
from magenta.models.gansynth.lib.generate_util import get_random_instruments
from magenta.models.gansynth.lib.generate_util import get_z_notes
from magenta.models.gansynth.lib.generate_util import load_midi
from magenta.models.gansynth.lib.generate_util import save_wav

# TODO get checkpoint https://storage.googleapis.com/magentadata/models/gansynth/acoustic_only.zip
from audio_utils import save_spectogram_plot

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string(
  "log", "WARN",
  "The threshold for what messages will be logged. DEBUG, INFO, WARN, ERROR, "
  "or FATAL.")


def app(unused_argv):
  # TODO midi
  notes = get_midi()

  # TODO generate audio
  audio_clip = generate_audio(notes)

  # TODO show and write audio
  write_audio(audio_clip)


def get_midi(midi_filename: str = "cs1-1pre-short.mid"):
  """
  TODO
  """
  midi_path = os.path.join("midi", midi_filename)
  note_sequence, notes = load_midi(midi_path)
  # TODO use utils
  mm.plot_sequence(note_sequence)
  return notes


def generate_audio(notes,
                   batch_size: int = 16,
                   checkpoint_dir: str = "checkpoints/gansynth/acoustic_only"):
  """
  TODO
  """
  flags = lib_flags.Flags({"batch_size_schedule": [batch_size]})
  model = lib_model.Model.load_from_path(checkpoint_dir, flags)
  seconds_per_instrument = 5

  # Distribute latent vectors linearly in time
  z_instruments, t_instruments = get_random_instruments(
    model,
    notes["end_times"][-1],
    secs_per_instrument=seconds_per_instrument)

  # Get latent vectors for each note
  z_notes = get_z_notes(notes["start_times"], z_instruments, t_instruments)

  # Generate audio for each note
  print(f"Generating {len(z_notes)} samples...")
  audio_notes = model.generate_samples_from_z(z_notes, notes["pitches"])

  # Make a single audio clip
  audio_clip = combine_notes(audio_notes,
                             notes["start_times"],
                             notes["end_times"],
                             notes["velocities"])

  return audio_clip


def write_audio(audio_clip):
  """
  TODO
  """
  # TODO https://en.wikipedia.org/wiki/Constant-Q_transform
  print("CQT Spectrogram:")
  save_spectogram_plot(audio_clip,
                       output_dir=os.path.join("output", "gansynth"))

  # TODO Write the file
  wav_filename = os.path.join("output", "gansynth", "generated_clip.wav")
  save_wav(audio_clip, wav_filename)


if __name__ == "__main__":
  tf.logging.set_verbosity(FLAGS.log)
  tf.app.run(app)
