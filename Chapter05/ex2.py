import librosa
import matplotlib.pyplot as plt
import numpy as np
from magenta.models.gansynth.lib import flags as lib_flags
from magenta.models.gansynth.lib import generate_util as gu
from magenta.models.gansynth.lib import model as lib_model
from magenta.models.gansynth.lib.generate_util import combine_notes
from magenta.music.notebook_utils import colab_play as play
from magenta.protobuf.music_pb2 import NoteSequence


def specplot(audio_clip):
  p_min = np.min(36)
  p_max = np.max(84)
  f_min = librosa.midi_to_hz(p_min)
  f_max = 2 * librosa.midi_to_hz(p_max)
  octaves = int(np.ceil(np.log2(f_max) - np.log2(f_min)))
  bins_per_octave = 36
  n_bins = int(bins_per_octave * octaves)
  C = librosa.cqt(audio_clip, sr=SR, hop_length=2048, fmin=f_min, n_bins=n_bins,
                  bins_per_octave=bins_per_octave)
  power = 10 * np.log10(np.abs(C) ** 2 + 1e-6)
  plt.matshow(power[::-1, 2:-2], aspect='auto', cmap=plt.cm.magma)
  plt.yticks([])
  plt.xticks([])


BATCH_SIZE = 16
SR = 16000

CKPT_DIR = '/content/gansynth/acoustic_only'
flags = lib_flags.Flags({'batch_size_schedule': [BATCH_SIZE]})

model = lib_model.Model.load_from_path(CKPT_DIR, flags)

seconds_per_instrument = 5  # @param {type:"slider", min:1, max:10, step:1}

notes = NoteSequence()

# @markdown This cell plays and displays a [Constant-Q spectrogram](https://en.wikipedia.org/wiki/Constant-Q_transform) of the synthesized audio.

# Distribute latent vectors linearly in time
z_instruments, t_instruments = gu.get_random_instruments(
  model, notes['end_times'][-1], secs_per_instrument=seconds_per_instrument)

# Get latent vectors for each note
z_notes = gu.get_z_notes(notes['start_times'], z_instruments, t_instruments)

# Generate audio for each note
print('Generating {} samples...'.format(len(z_notes)))
audio_notes = model.generate_samples_from_z(z_notes, notes['pitches'])

# Make a single audio clip
audio_clip = combine_notes(audio_notes,
                           notes['start_times'],
                           notes['end_times'],
                           notes['velocities'])

# Play the audio
print('\nAudio:')
play(audio_clip, sample_rate=SR)
print('CQT Spectrogram:')
specplot(audio_clip)
