"""
- lakh https://colinraffel.com/projects/lmd/#get
  - dataset tutorial https://nbviewer.jupyter.org/github/craffel/midi-dataset/blob/master/Tutorial.ipynb
  - midi stats (time sig and others) https://nbviewer.jupyter.org/github/craffel/midi-ground-truth/blob/master/Statistics.ipynb
  - https://colinraffel.com/talks/c4dm2016lakh.pdf
- lakh pianoroll dataset
  - https://salu133445.github.io/lakh-pianoroll-dataset/
  - lakh pianorol https://github.com/salu133445/lakh-pianoroll-dataset
- synth lakh (nice post on instruments) http://www.slakh.com/
- https://composing.ai/
  - https://composing.ai/dataset list of datasets + reddit and al
- echo nest
  - echo nest examples http://static.echonest.com/enspex/
- music brainz
  - music brainz python wrapper https://python-musicbrainzngs.readthedocs.io/en/v0.6/
  - music brains web api https://musicbrainz.org/doc/Development/XML_Web_Service/Version_2
- million song
  - http://millionsongdataset.com/pages/tutorial/
  - dataset genre http://millionsongdataset.com/blog/11-2-28-deriving-genre-dataset/
  - dataset faq http://millionsongdataset.com/faq/
  - http://millionsongdataset.com/faq/#what-other-large-datasets-are-available
  - kaggle million song genre (learning) https://www.kaggle.com/c/mlp2016-7-msd-genre
- last.fm dataset http://millionsongdataset.com/lastfm/

check

- music ai lab https://musicai.citi.sinica.edu.tw/
- /musicbrainz (Group) 'data about the song coming from MusicBrainz'
- echo nest
- other magenta epiano dataset
- MSD AllMusic Top Genre Dataset (TopMAGD)
- https://salu133445.github.io/lakh-pianoroll-dataset/dataset.html
- https://salu133445.github.io/musegan/
- https://salu133445.github.io/
- https://developer.gracenote.com/web-api info

labels https://salu133445.github.io/lakh-pianoroll-dataset/labels.html
- Last.fm Dataset
- Million Song Dataset (MSD) Benchmarks
- Tagtraum genre annotations (http://www.tagtraum.com/msd_genre_datasets.html)

visual midi
- https://salu133445.github.io/pypianoroll/
"""

import json
import os

import IPython.display
import librosa
import matplotlib.pyplot as plt
import mir_eval.display
# Imports
import numpy as np
import pretty_midi
import tables

# Local path constants
DATA_PATH = 'D:\\Users\\Claire\\Data\\datasets\\lakh_midi_dataset\\lmd_matched'
RESULTS_PATH = 'D:\\Users\\Claire\\Data\\datasets\\lakh_midi_dataset'
# Path to the file match_scores.json distributed with the LMD
SCORE_FILE = os.path.join(RESULTS_PATH, 'match_scores.json')


# Utility functions for retrieving paths
def msd_id_to_dirs(msd_id):
  """Given an MSD ID, generate the path prefix.
  E.g. TRABCD12345678 -> A/B/C/TRABCD12345678"""
  return os.path.join(msd_id[2], msd_id[3], msd_id[4], msd_id)


def msd_id_to_mp3(msd_id):
  """Given an MSD ID, return the path to the corresponding mp3"""
  return os.path.join(DATA_PATH, 'msd', 'mp3',
                      msd_id_to_dirs(msd_id) + '.mp3')


def msd_id_to_h5(h5):
  """Given an MSD ID, return the path to the corresponding h5"""
  return os.path.join(RESULTS_PATH, 'lmd_matched_h5',
                      msd_id_to_dirs(msd_id) + '.h5')


def get_midi_path(msd_id, midi_md5, kind):
  """Given an MSD ID and MIDI MD5, return path to a MIDI file.
  kind should be one of 'matched' or 'aligned'. """
  return os.path.join(RESULTS_PATH, 'lmd_{}'.format(kind),
                      msd_id_to_dirs(msd_id), midi_md5 + '.mid')


with open(SCORE_FILE) as f:
  scores = json.load(f)

# Grab a Million Song Dataset ID from the scores dictionary
msd_id = list(scores)[1234]
print('Million Song Dataset ID {} has {} MIDI file matches:'.format(
  msd_id, len(scores[msd_id])))
for midi_md5, score in scores[msd_id].items():
  print('  {} with confidence score {}'.format(midi_md5, score))

# while True:
# Grab an MSD ID and its dictionary of matches
# msd_id, matches = scores.popitem()
# Grab a MIDI from the matches
# midi_md5, score = matches.popitem()
# Construct the path to the aligned MIDI
# aligned_midi_path = get_midi_path(msd_id, midi_md5, 'aligned')
# Load/parse the MIDI file with pretty_midi
# pm = pretty_midi.PrettyMIDI(aligned_midi_path)
# Look for a MIDI file which has lyric and key signature change events
# if len(pm.lyrics) > 5 and len(pm.key_signature_changes) > 0:
#   break

# MIDI files in LMD-aligned are aligned to 7digital preview clips from the MSD
# Let's listen to this aligned MIDI along with its preview clip
# Load in the audio data
# audio, fs = librosa.load(msd_id_to_mp3(msd_id))
# Synthesize the audio using fluidsynth
# midi_audio = pm.fluidsynth(fs)
# Play audio in one channel, synthesized MIDI in the other
# IPython.display.Audio([audio, midi_audio[:audio.shape[0]]], rate=fs)

with tables.open_file(msd_id_to_h5(msd_id)) as h5:
  print('ID: {}'.format(msd_id))
  print('"{}" by {} on "{}"'.format(
    h5.root.metadata.songs.cols.title[0],
    h5.root.metadata.songs.cols.artist_name[0],
    h5.root.metadata.songs.cols.release[0]))
  print('Top 5 artist terms:',
        ', '.join(list(h5.root.metadata.artist_terms)[:5]))

exit(0)

# Retrieve piano roll of the MIDI file
piano_roll = pm.get_piano_roll()
# Use 7 octaves starting from C1
piano_roll = piano_roll[12:96]
# Retrieve the audio corresponding to this MSD entry
audio, fs = librosa.load(msd_id_to_mp3(msd_id))
# Compute constant-Q spectrogram
cqt = librosa.logamplitude(librosa.cqt(audio))
# Normalize for visualization
cqt = librosa.util.normalize(cqt)

plt.figure(figsize=(10, 6))
plt.subplot(211)
librosa.display.specshow(piano_roll, y_axis='cqt_note', cmap=plt.cm.hot)
plt.title('MIDI piano roll')
plt.subplot(212)
librosa.display.specshow(cqt, y_axis='cqt_note', x_axis='time',
                         cmap=plt.cm.hot, vmin=np.percentile(cqt, 25))
plt.title('Audio CQT')

# Retrieve piano roll of one of the instruments
piano_roll = pm.instruments[4].get_piano_roll()
piano_roll = piano_roll[12:96]
plt.figure(figsize=(10, 3))
librosa.display.specshow(piano_roll, y_axis='cqt_note', cmap=plt.cm.hot)
# Get the text name of this instrument's program number
program_name = pretty_midi.program_to_instrument_name(pm.instruments[4].program)
plt.title('Instrument 4 ({}) piano roll'.format(program_name))

# pretty_midi also provides direct access to the pitch and start/end time of each note
intervals = np.array(
  [[note.start, note.end] for note in pm.instruments[4].notes])
notes = np.array([note.pitch for note in pm.instruments[4].notes])
plt.figure(figsize=(10, 3))
mir_eval.display.piano_roll(intervals, midi=notes, facecolor='orange')
plt.title('Instrument 4 ({}) piano roll'.format(program_name))
plt.xlabel('Time')
plt.ylabel('MIDI note number')

# Retrieve the beats and downbeats from pretty_midi
# Note that the beat phase will be wrong until the first time signature change after 0s
# So, let's start beat tracking from that point
first_ts_after_0 = \
  [ts.time for ts in pm.time_signature_changes if ts.time > 0.][0]
# Get beats from pretty_midi, supplying a start time
beats = pm.get_beats(start_time=first_ts_after_0)
# .. downbeats, too
downbeats = pm.get_downbeats(start_time=first_ts_after_0)
# Display meter on top of waveform
plt.figure(figsize=(10, 3))
librosa.display.waveplot(audio, color='green', alpha=.5)
mir_eval.display.events(beats, base=-1, height=2, color='orange')
mir_eval.display.events(downbeats, base=-1, height=2, color='black', lw=2)

# Synthesize clicks at these downbeat times
beat_clicks = librosa.clicks(beats, length=audio.shape[0])
downbeat_clicks = librosa.clicks(downbeats, click_freq=2000,
                                 length=audio.shape[0])
IPython.display.Audio([audio, beat_clicks + downbeat_clicks], rate=fs)

# Print out all key changes in the MIDI file
for key_change in pm.key_signature_changes:
  print('Key {} starting at time {:.2f}'.format(
    pretty_midi.key_number_to_key_name(key_change.key_number), key_change.time))

# Get the boundaries of each line in the lyrics
lines = [0] + [n for n, lyric in enumerate(pm.lyrics) if '\r' in lyric.text]
for start, end in zip(lines[:-1], lines[1:]):
  # Print the times of each lyric in the line, delimited by |
  print('|'.join('{:>8.3f}'.format(lyric.time)
                 for lyric in pm.lyrics[start:end]
                 if lyric.text != '\r'))
  # Print the text of each lyric in the line, delimited by |
  print('|'.join('{:>8}'.format(lyric.text)
                 for lyric in pm.lyrics[start:end]
                 if lyric.text != '\r'))
