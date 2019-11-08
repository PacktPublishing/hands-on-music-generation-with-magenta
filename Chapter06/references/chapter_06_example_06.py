import json
import json
import os
import random
import timeit
from json import JSONDecodeError
from multiprocessing import Manager
from multiprocessing.pool import Pool

import matplotlib.pyplot as plt
import requests
import tables

# Local path constants
from threading_utils import AtomicCounter

RESULTS_PATH = 'D:\\project\\dataset\\lakh'
# Path to the file match_scores.json distributed with the LMD
SCORE_FILE = os.path.join(RESULTS_PATH, 'match_scores.json')
DATASET_DIR = "D:\\project\\dataset\\jazz_midi\\drums\\v1"

print(os.environ['LAST_FM_API_KEY'])


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



def clean(byte):
  # TODO this has no impact
  string = byte.decode("utf-8")
  for separator in ["(", "-", "/", ";", "["]:
    if separator in string:
      string = string[:string.index(separator)]
  string = string.strip()
  string = string.replace("_", "")
  string = string.replace("  ", " ")
  return string


def get_genres(msd_id, counter):
  if counter.value() % 10 == 0:
    print(f"Iteration count: {counter.value()}/{counter.total}")
  with tables.open_file(msd_id_to_h5(msd_id)) as h5:
    title = h5.root.metadata.songs.cols.title[0]
    # TODO test if this improves matching or not
    title = clean(title)
    artist = h5.root.metadata.songs.cols.artist_name[0]
    artist = clean(artist)
    last_fm_api_key = os.environ['LAST_FM_API_KEY']
    request = (f"https://ws.audioscrobbler.com/2.0/"
               f"?method=track.gettoptags"
               f"&artist={artist}"
               f"&track={title}"
               f"&api_key={last_fm_api_key}"
               f"&format=json")
    response = requests.get(request)
    try:
      json = response.json()
      # print(json)
    except JSONDecodeError as e:
      print(f"Error in request for '{artist}' - '{title}': '{e}'")
      return
    if "error" in json:
      print(f"Error in request for '{artist}' - '{title}': '{json['message']}'")
      return
    if "toptags" not in json:
      print(f"Error in request for '{artist}' - '{title}': no top tags")
      return
    tags = [tag["name"] for tag in json["toptags"]["tag"]]
    tags = [tag.lower() for tag in tags if tag]
    # print(f"Top tags for {msd_id}: {tags}")
    counter.increment()
    return msd_id, tags


def get_drums_tracks(possible_genres=None):
  start = timeit.default_timer()
  from itertools import cycle

  # TODO track genres
  with Pool(4) as pool:
    manager = Manager()
    counter = AtomicCounter(manager, len(scores))
    print("START")
    track_genres = pool.starmap(get_genres, zip(scores, cycle([counter])))
    track_genres = [track_genre for track_genre in track_genres if track_genre]
    print("END")
    match_percentage = len(track_genres) / len(scores) * 100
    print(f"Number of tracks: {len(scores_matches)}, "
          f"Number of tracks in sample: {len(scores)}, "
          f"number of matched tracks: {len(track_genres)} "
          f"({match_percentage}%)")

  # TODO drum extract
  genres_count = []

  def count_genres(genres):
    for possible_genre in possible_genres:
      for genre in genres:
        if possible_genre == genre:
          genres_count.append(genre)
          return

  for msd_id, genres in track_genres:
    count_genres(genres)

  match_percentage = len(genres_count) / len(track_genres) * 100
  print(f"Number of matched tracks: {len(track_genres)}, "
        f"number of matched genres: {len(genres_count)} ({match_percentage}%)")
  print(genres_count)

  # TODO histogram
  plt.hist(genres_count, bins=len(possible_genres))
  plt.ylabel('count')
  # plt.xticks(rotation=30, horizontalalignment="right")
  plt.title('Genre count')
  plt.show()

  stop = timeit.default_timer()
  print('Time: ', stop - start)


if __name__ == "__main__":
  get_drums_tracks(["jazz", "blues", "country"])
