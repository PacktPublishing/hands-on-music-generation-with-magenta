"""
TODO threaded artist filter on lakh
"""
import copy
import json
import os
import random
import timeit
from multiprocessing.pool import Pool

import matplotlib.pyplot as plt
import tables
# Local path constants
from pretty_midi import PrettyMIDI, Instrument

RESULTS_PATH = 'D:\\project\\dataset\\lakh'
# Path to the file match_scores.json distributed with the LMD
SCORE_FILE = os.path.join(RESULTS_PATH, 'match_scores.json')
DATASET_DIR = "D:\\project\\dataset\\jazz_midi\\drums\\v1"


# Utility functions for retrieving paths
def msd_id_to_dirs(msd_id):
  """Given an MSD ID, generate the path prefix.
  E.g. TRABCD12345678 -> A/B/C/TRABCD12345678"""
  return os.path.join(msd_id[2], msd_id[3], msd_id[4], msd_id)


def get_midi_path(msd_id, midi_md5, kind):
  """Given an MSD ID and MIDI MD5, return path to a MIDI file.
  kind should be one of 'matched' or 'aligned'. """
  return os.path.join(RESULTS_PATH, 'lmd_{}'.format(kind),
                      msd_id_to_dirs(msd_id), midi_md5 + '.mid')


def msd_id_to_h5(msd_id):
  """Given an MSD ID, return the path to the corresponding h5"""
  return os.path.join(RESULTS_PATH, 'lmd_matched_h5',
                      msd_id_to_dirs(msd_id) + '.h5')


with open(SCORE_FILE) as f:
  scores_matches = json.load(f)

# Grab a Million Song Dataset ID from the scores dictionary
scores = random.sample(list(scores_matches), 100)


# scores = list(scores)

def get_track_info(msd_id):
  with tables.open_file(msd_id_to_h5(msd_id)) as h5:
    artist_name = h5.root.metadata.songs.cols.artist_name[0].decode("utf-8")
    max_score = 0
    matched_midi_md5 = None
    for midi_md5, score in scores_matches[msd_id].items():
      if score > max_score:
        max_score = score
        matched_midi_md5 = midi_md5
    if not matched_midi_md5:
      print(f"Not matched {msd_id}: {scores_matches[msd_id]}")
    midi_path = get_midi_path(msd_id, matched_midi_md5, "matched")
    pm = None
    try:
      pm = PrettyMIDI(midi_path)
    except Exception as e:
      print(f"Malformed MIDI {msd_id}: {e}")
  return msd_id, {
    'artist': artist_name,
    'pretty_midi': pm
  }


def extract_drum_instrument(msd_id, pm: PrettyMIDI):
  if not pm:
    return
  pm_drums = copy.deepcopy(pm)
  pm_drums.instruments = []
  for instrument in pm.instruments:
    if instrument.is_drum:
      instrument_copy = Instrument(program=0, is_drum=True)
      for note in instrument.notes:
        instrument_copy.notes.append(note)
      pm_drums.instruments.append(instrument_copy)
      break
  if len(pm_drums.instruments) != 1:
    print(f"Invalid number of drums {msd_id}: {len(pm_drums.instruments)}")
    return
  return msd_id, pm_drums


def get_drums_tracks():
  start = timeit.default_timer()

  # TODO track info
  with Pool(4) as pool:
    track_infos = pool.map(get_track_info, scores)

  # TODO drum extract
  # TODO merge multiple drum tracks
  with Pool(4) as pool:
    pms = [(msd_id, infos["pretty_midi"]) for msd_id, infos in track_infos]
    pm_drums = pool.starmap(extract_drum_instrument, pms)
    pm_drums = [(pm_drum[0], pm_drum[1]) for pm_drum in pm_drums if pm_drum]
    drum_lengths = [pm_drum.get_end_time() for _, pm_drum in pm_drums]
    [pm_drum.write(os.path.join(DATASET_DIR, f"{msd_id}.mid"))
     for msd_id, pm_drum in pm_drums]
  print(f"Number of drums tracks: {len(drum_lengths)}")

  # TODO histogram
  plt.hist(drum_lengths, bins=10)
  plt.ylabel('length (sec)')
  plt.title('Drums length')
  plt.show()

  stop = timeit.default_timer()
  print('Time: ', stop - start)


if __name__ == "__main__":
  get_drums_tracks()
