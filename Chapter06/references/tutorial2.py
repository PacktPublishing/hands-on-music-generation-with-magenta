import json
import os
from multiprocessing.pool import Pool

import tables
from tqdm import tqdm

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
# scores = random.sample(list(scores), 1000)
scores = list(scores)

# pool = multiprocessing.Pool(4)
# out1, out2, out3 = zip(*pool.map(calc_stuff, range(0, 10 * offset, offset)))

possible_genres = ["jazz", "blues", "funk"]


# def get_genres(msd_id):
#   with tables.open_file(msd_id_to_h5(msd_id)) as h5:
#     artist_terms = list(h5.root.metadata.artist_terms)
#     artist_mbtags = list(h5.root.musicbrainz.artist_mbtags)
#     echo_nest = set()
#     for artist_term in artist_terms:
#       artist_term = artist_term.decode("utf-8")
#       for category in possible_genres:
#         if category in artist_term:
#           echo_nest.add(artist_term)
#           # genres[category].add(artist_term)
#           # track_count[category] = track_count[category] + 1
#     musicbrainz = set()
#     for artist_term in artist_mbtags:
#       artist_term = artist_term.decode("utf-8")
#       for category in possible_genres:
#         if category in artist_term:
#           musicbrainz.add(artist_term)
#           # genres_mb[category].add(artist_term)
#           # track_count_mb[category] = track_count[category] + 1
#     return {echo_nest, musicbrainz}
#
#
# with Pool(5) as p:
#   genres = p.map(get_genres, scores, 1000)

genres = {"jazz": set(), "blues": set(), "funk": set()}
genres_mb = {"jazz": set(), "blues": set(), "funk": set()}
track_count = {"jazz": 0, "blues": 0, "funk": 0}
track_count_mb = {"jazz": 0, "blues": 0, "funk": 0}
for msd_id in tqdm(scores):
  with tables.open_file(msd_id_to_h5(msd_id)) as h5:
    title = h5.root.metadata.songs.cols.title[0]
    artist_name = h5.root.metadata.songs.cols.artist_name[0]
    release = h5.root.metadata.songs.cols.release[0]
    genre = h5.root.metadata.songs.cols.genre[0]
    artist_terms = list(h5.root.metadata.artist_terms)
    artist_mbtags = list(h5.root.musicbrainz.artist_mbtags)
    for artist_term in artist_terms:
      artist_term = artist_term.decode("utf-8")
      for category in genres.keys():
        if category in artist_term:
          genres[category].add(artist_term)
          track_count[category] = track_count[category] + 1
    for artist_term in artist_mbtags:
      artist_term = artist_term.decode("utf-8")
      for category in genres.keys():
        if category in artist_term:
          genres_mb[category].add(artist_term)
          track_count_mb[category] = track_count[category] + 1
          # if genre:
    #   print(f"{title} - {artist_name} - {release} - {genre}")
    # print(f"{title} - {artist_name} - {release} - "
    #       f"{genre} - {artist_terms} - {artist_mbtags}")
    # if ("jazz" in artist_terms or "jazz" in artist_mbtags):
    #   print(f"")

print("genres")
for key, value in genres.items():
  print(f"{key}: {len(value)}")
print(f"{genres}")
print(f"{track_count}")

print("genres mb")
for key, value in genres_mb.items():
  print(f"{key}: {len(value)}")
print(f"{genres_mb}")
print(f"{track_count_mb}")
