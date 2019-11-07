"""
TODO threaded jazz filter on lakh
"""

import json
import multiprocessing
import os
import random
from typing import List, Optional

import tables

# Local path constants

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
scores = random.sample(list(scores_matches), 100)


# scores = list(scores)

def get_track_info(msd_id):
  with tables.open_file(msd_id_to_h5(msd_id)) as h5:
    artist_terms = list(h5.root.metadata.artist_terms)
    genres = [artist_term.decode("utf-8") for artist_term in artist_terms]
  return msd_id, {'genres': genres}


def is_track_filtered(track_genres, possible_genres):
  if not possible_genres:
    return True
  for track_genre in track_genres:
    for possible_genre in possible_genres:
      if possible_genre in track_genre:
        return True
  return False


def get_tracks_by_genre(possible_genres: Optional[List[str]] = None):
  pool = multiprocessing.Pool(2)
  tracks_info = pool.map(get_track_info, scores)

  tracks_by_genre = {}
  for msd_id, infos in tracks_info:
    genres = infos["genres"]
    filtered = is_track_filtered(genres, possible_genres)
    if not filtered:
      continue
    for genre in genres:
      if genre not in tracks_by_genre:
        tracks_by_genre[genre] = []
      tracks_by_genre[genre].append(msd_id)

  with open("chapter_06_example_01.csv", "w") as file:
    file.write(f"genre,msd_id\n")
    for genre, msd_ids in tracks_by_genre.items():
      file.write(f"{genre}")
      for msd_id in msd_ids:
        file.write(f",{msd_id}")
      file.write(f"\n")

  print()
  print("total")
  print(f"tracks_genre: {len(tracks_by_genre)}")

  print()
  print("out")
  for genre, msd_ids in tracks_by_genre.items():
    print(f"{genre}: {len(msd_ids)}")


if __name__ == "__main__":
  get_tracks_by_genre(["jazz"])
