"""
TODO threaded artist filter on lakh
"""
import collections
import copy
import json
import os
import random
import timeit
from itertools import cycle
from multiprocessing import Manager
from multiprocessing.pool import Pool

import matplotlib.pyplot as plt
import tables
# Local path constants
from pretty_midi import PrettyMIDI, Instrument, program_to_instrument_name

from multiprocessing_utils import AtomicCounter

RESULTS_PATH = 'D:\\project\\dataset\\lakh'
# Path to the file match_scores.json distributed with the LMD
SCORE_FILE = os.path.join(RESULTS_PATH, 'match_scores.json')


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
scores = random.sample(list(scores_matches), 1000)


# scores = list(scores)

def get_midi_path2(msd_id):
  max_score = 0
  matched_midi_md5 = None
  for midi_md5, score in scores_matches[msd_id].items():
    if score > max_score:
      max_score = score
      matched_midi_md5 = midi_md5
  if not matched_midi_md5:
    print(f"Not matched {msd_id}: {scores_matches[msd_id]}")
  midi_path = get_midi_path(msd_id, matched_midi_md5, "matched")
  return midi_path


def get_pretty_midi(msd_id):
  pm = None
  try:
    pm = PrettyMIDI(get_midi_path2(msd_id))
  except Exception as e:
    print(f"Malformed MIDI {msd_id}: {e}")
  return pm


def get_programs(msd_id, counter):
  with tables.open_file(msd_id_to_h5(msd_id)) as h5:
    pm = get_pretty_midi(msd_id)
    if not pm:
      return
    programs = [instrument.program for instrument in pm.instruments
                if not instrument.is_drum]
    drums = [128 for instrument in pm.instruments if instrument.is_drum]
    if not programs and not drums:
      return
    counter.increment()
    return {"msd_id": msd_id, "programs": programs + drums}


def get_drums_tracks():
  start = timeit.default_timer()

  # TODO track info
  with Pool(4) as pool:
    manager = Manager()
    counter = AtomicCounter(manager, len(scores))
    print("START")
    track_programs = pool.starmap(get_programs,
                                  zip(scores, cycle([counter])))
    track_programs = [track_program for track_program in track_programs
                      if track_program]
    print("END")
    match_percentage = len(track_programs) / len(scores) * 100
    print(f"Number of tracks: {len(scores_matches)}, "
          f"Number of tracks in sample: {len(scores)}, "
          f"number of program tracks: {len(track_programs)} "
          f"({match_percentage}%)")

  # TODO group alike programs
  # TODO merge multiple track drums

  # TODO histogram
  programs = []
  for infos in track_programs:
    for program in infos["programs"]:
      programs.append(program)
  drums_programs = collections.Counter(programs).most_common(1)[0]
  most_common_programs = collections.Counter(programs).most_common(25)
  most_common_programs = [(program_to_instrument_name(program[0]), program[1])
                          for program in most_common_programs
                          if program[0] != 128]
  most_common_programs = [("Drums", drums_programs[1])] + most_common_programs
  print(most_common_programs)
  plt.hist(programs, bins=128)
  # plt.bar([program for program, _ in most_common_programs],
  #         [count for _, count in most_common_programs])
  plt.ylabel('count')
  plt.title('Programs count')
  plt.show()

  stop = timeit.default_timer()
  print('Time: ', stop - start)


if __name__ == "__main__":
  get_drums_tracks()
