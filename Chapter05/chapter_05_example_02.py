"""
This example shows how to use GANSynth to generate intruments for a backing
score from a MIDI file.
"""

import os
import time
import zipfile

import numpy as np
import tensorflow as tf
from magenta.models.gansynth.lib import flags as lib_flags
from magenta.models.gansynth.lib import model as lib_model
from magenta.models.gansynth.lib.generate_util import combine_notes
from magenta.models.gansynth.lib.generate_util import get_random_instruments
from magenta.models.gansynth.lib.generate_util import get_z_notes
from magenta.models.gansynth.lib.generate_util import load_midi
from magenta.models.gansynth.lib.generate_util import save_wav
from six.moves import urllib

from audio_utils import save_spectrogram_plot

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string(
  "log", "WARN",
  "The threshold for what messages will be logged. DEBUG, INFO, WARN, ERROR, "
  "or FATAL.")


def download_checkpoint(checkpoint_name: str,
                        target_dir: str = "checkpoints") -> None:
  """
  Downloads a Magenta checkpoint to target directory and extracts it.

  Target directory target_dir will be created if it does not already exist.

      :param checkpoint_name: magenta checkpoint name to download,
      one of "acoustic_only" or "all_instruments"
      :param target_dir: local directory in which to write the checkpoint
  """
  tf.gfile.MakeDirs(target_dir)
  checkpoint_target = os.path.join(target_dir, f"{checkpoint_name}.zip")
  if not os.path.exists(checkpoint_target):
    response = urllib.request.urlopen(
      f"https://storage.googleapis.com/magentadata/"
      f"models/gansynth/{checkpoint_name}.zip")
    data = response.read()
    local_file = open(checkpoint_target, 'wb')
    local_file.write(data)
    local_file.close()
    with zipfile.ZipFile(checkpoint_target, 'r') as zip:
      zip.extractall(target_dir)


def get_midi_notes(midi_filename: str = "cs1-1pre-short.mid") -> dict:
  """
  Returns a notes information dictionary for the gansynth lib.

  :param midi_filename: the midi filename to load, it needs to be present
  in the "midi" folder
  """
  midi_path = os.path.join("midi", midi_filename)
  note_sequence, notes = load_midi(midi_path)
  return notes


def generate_audio(notes: dict,
                   seconds_per_instrument: int = 5,
                   batch_size: int = 16,
                   checkpoint_dir: str = "checkpoints/acoustic_only") \
    -> np.ndarray:
  """
  Generates an audio clip from the notes information dictionary, by randomly
  sampling "instruments" from the latent space (sounds of a given time),
  and generating samples from them.

  :param notes: the notes dictionary, must come
  from magenta.models.gansynth.lib.generate_util.load_midi
  :param seconds_per_instrument: the number of seconds for each instrument
  :param batch_size: the batch size for the model
  :param checkpoint_dir: the checkpoint folder
  """
  flags = lib_flags.Flags({"batch_size_schedule": [batch_size]})
  model = lib_model.Model.load_from_path(checkpoint_dir, flags)

  # Distribute latent vectors linearly in time
  z_instruments, t_instruments = get_random_instruments(
    model,
    notes["end_times"][-1],
    secs_per_instrument=seconds_per_instrument)

  # Get latent vectors for each note
  z_notes = get_z_notes(notes["start_times"], z_instruments, t_instruments)

  # Generate audio for each note
  audio_notes = model.generate_samples_from_z(z_notes, notes["pitches"])

  # Make a single audio clip
  audio_clip = combine_notes(audio_notes,
                             notes["start_times"],
                             notes["end_times"],
                             notes["velocities"])

  return audio_clip


def save_audio(audio_clip: np.ndarray) -> None:
  """
  Writes the audio clip to disk as a spectogram plot (constant Q transform)
  and wav file. See audio_utils.save_spectogram_plot.

  :param audio_clip: the audio clip to save
  """
  # Saves the CQT Spectrogram on disk
  save_spectrogram_plot(audio_clip,
                        output_dir=os.path.join("output", "gansynth"))

  # Saves the wav file on disk
  date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
  filename = f"{date_and_time}.wav"
  path = os.path.join(os.path.join("output", "gansynth"), filename)
  save_wav(audio_clip, path)


def app(unused_argv):
  # Downloads and extracts the checkpoint to "checkpoint/acoustic_only"
  download_checkpoint("acoustic_only")

  # Loads the midi file and get the notes dictionary
  notes = get_midi_notes()

  # Generates the audio clip from the notes dictionary
  audio_clip = generate_audio(notes)

  # Saves the audio plot and the audio file
  save_audio(audio_clip)


if __name__ == "__main__":
  tf.logging.set_verbosity(FLAGS.log)
  tf.app.run(app)
