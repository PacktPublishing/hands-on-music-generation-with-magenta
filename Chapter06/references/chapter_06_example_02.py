"""
TODO threaded artist filter on lakh
"""
import matplotlib.pyplot as plt

import timeit

import json
import multiprocessing
import os
import random
from multiprocessing.pool import Pool
from typing import List, Optional

import tables

# Local path constants
from tqdm import tqdm

RESULTS_PATH = 'D:\\project\\dataset\\lakh'
# Path to the file match_scores.json distributed with the LMD
SCORE_FILE = os.path.join(RESULTS_PATH, 'match_scores.json')


# Utility functions for retrieving paths
def msd_id_to_dirs(msd_id):
  """Given an MSD ID, generate the path prefix.
  E.g. TRABCD12345678 -> A/B/C/TRABCD12345678"""
  return os.path.join(msd_id[2], msd_id[3], msd_id[4], msd_id)


def msd_id_to_h5(msd_id):
  """Given an MSD ID, return the path to the corresponding h5"""
  return os.path.join(RESULTS_PATH, 'lmd_matched_h5',
                      msd_id_to_dirs(msd_id) + '.h5')


with open(SCORE_FILE) as f:
  scores_matches = json.load(f)

# Grab a Million Song Dataset ID from the scores dictionary
scores = random.sample(list(scores_matches), 1000)
# scores = list(scores)

def get_track_info(msd_id):
  with tables.open_file(msd_id_to_h5(msd_id)) as h5:
    artist_name = h5.root.metadata.songs.cols.artist_name[0].decode("utf-8")
  return msd_id, {'artist': artist_name}


def get_tracks_by_artist(possible_artists: Optional[List[str]] = None):
  start = timeit.default_timer()
  with Pool(2) as pool:
    track_infos = pool.map(get_track_info, scores)
  stop = timeit.default_timer()
  print('Time: ', stop - start)

  start = timeit.default_timer()
  tracks_by_artist = {}
  for msd_id, infos in track_infos:
    artist = infos["artist"]
    if possible_artists and artist not in possible_artists:
      continue
    if artist not in tracks_by_artist:
      tracks_by_artist[artist] = []
    tracks_by_artist[artist].append(msd_id)

  with open("chapter_06_example_02.csv", "w") as file:
    file.write(f"artist,msd_id\n")
    for artist, msd_ids in tracks_by_artist.items():
      file.write(f"\"{artist}\"")
      for msd_id in msd_ids:
        file.write(f",{msd_id}")
      file.write(f"\n")
  stop = timeit.default_timer()
  print('Time: ', stop - start)

  print()
  print("total")
  print(f"artists: {len(tracks_by_artist)}")

  print()
  print("out")
  for artist, msd_ids in tracks_by_artist.items():
    print(f"{artist}: {len(msd_ids)}")

  import collections
  artists = [infos["artist"] for msd_id, infos in track_infos]
  most_common_artists = collections.Counter(artists).most_common(10)
  print(most_common_artists)

  # plt.hist([artist for artist, count in most_common_artists], bins=10)
  # plt.hist(artists, bins=5)
  plt.bar([a for a, b in most_common_artists],
          [b for a, b in most_common_artists])
  plt.ylabel('count')
  plt.xticks(rotation=30, horizontalalignment="right")
  plt.title('Artist song count')
  plt.show()

  # import matplotlib.pyplot as plt
  # plt.hist(x, bins=10)
  # plotting.plot_hist([s['n_instruments'] for s in statistics], range(22),
  #                    'Number of instruments', 'Thousands of MIDI files')
  # plt.xticks(range(0, 22, 5), range(0, 22 - 5, 5) + ['20+']);


if __name__ == "__main__":
  get_tracks_by_artist()
