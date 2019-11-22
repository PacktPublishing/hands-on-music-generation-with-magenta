"""
Filter on specific tags from the Last.fm API using the LAKHs dataset
matched with the MSD dataset.
"""

import argparse
import ast
import random
import timeit
from collections import Counter
from itertools import cycle
from multiprocessing import Manager
from multiprocessing.pool import Pool
from typing import List
from typing import Optional

import matplotlib.pyplot as plt
import requests
import tables
from bokeh.colors.groups import purple as colors

from lakh_utils import get_msd_score_matches
from lakh_utils import msd_id_to_h5
from multiprocessing_utils import AtomicCounter

parser = argparse.ArgumentParser()
parser.add_argument("--sample_size", type=int, default=1000)
parser.add_argument("--pool_size", type=int, default=4)
parser.add_argument("--path_dataset_dir", type=str, required=True)
parser.add_argument("--path_match_scores_file", type=str, required=True)
parser.add_argument("--last_fm_api_key", type=str, required=True)
parser.add_argument("--tags", type=str, required=True)
args = parser.parse_args()

# The list of all MSD ids (we might process only a sample)
MSD_SCORE_MATCHES = get_msd_score_matches(args.path_match_scores_file)
TAGS = ast.literal_eval(args.tags)


def get_tags(h5) -> Optional[list]:
  """
  Returns the top tags (ordered most popular first) from the Last.fm API
  using the title and the artist name from the h5 database.

  :param h5: the h5 database for the title and artist
  :return: the list of tags
  """
  title = h5.root.metadata.songs.cols.title[0].decode("utf-8")
  artist = h5.root.metadata.songs.cols.artist_name[0].decode("utf-8")
  request = (f"https://ws.audioscrobbler.com/2.0/"
             f"?method=track.gettoptags"
             f"&artist={artist}"
             f"&track={title}"
             f"&api_key={args.last_fm_api_key}"
             f"&format=json")
  response = requests.get(request, timeout=10)
  json = response.json()
  if "error" in json:
    raise Exception(f"Error in request for '{artist}' - '{title}': "
                    f"'{json['message']}'")
  if "toptags" not in json:
    raise Exception(f"Error in request for '{artist}' - '{title}': "
                    f"no top tags")
  tags = [tag["name"] for tag in json["toptags"]["tag"]]
  tags = [tag.lower().strip() for tag in tags if tag]
  return tags


def process(msd_id: str, counter: AtomicCounter) -> Optional[dict]:
  """
  Processes the given MSD id and increments the counter. The
  method will call the get_tags method.

  :param msd_id: the MSD id to process
  :param counter: the counter to increment
  :return: the dictionary containing the MSD id and the tags, raises an
  exception if the file cannot be processed
  """
  try:
    with tables.open_file(msd_id_to_h5(msd_id, args.path_dataset_dir)) as h5:
      tags = get_tags(h5)
      return {"msd_id": msd_id, "tags": tags}
  except Exception as e:
    print(f"Exception during processing of {msd_id}: {e}")
  finally:
    counter.increment()


def app(msd_ids: List[str]):
  start = timeit.default_timer()

  # Starts the threads
  with Pool(args.pool_size) as pool:
    manager = Manager()
    counter = AtomicCounter(manager, len(msd_ids))
    print("START")
    results = pool.starmap(process, zip(msd_ids, cycle([counter])))
    results = [result for result in results if result]
    print("END")
    results_percentage = len(results) / len(msd_ids) * 100
    print(f"Number of tracks: {len(MSD_SCORE_MATCHES)}, "
          f"number of tracks in sample: {len(msd_ids)}, "
          f"number of results: {len(results)} "
          f"({results_percentage:.2f}%)")

  # Finds which tags matches and count the results
  tags = []
  unique_tags = set()
  for result in results:
    result_tags = result["tags"]
    matching_tags = [tag for tag in result_tags if tag in TAGS]
    if matching_tags:
      joined_tag = "+".join(matching_tags)
      tags.append(joined_tag)
      unique_tags.add(joined_tag)
  match_percentage = len(tags) / len(results) * 100
  print(f"Number of results: {len(results)}, "
        f"number of matched tags: {len(tags)} "
        f"({match_percentage:.2f}%)")

  # Creates a bar chart for the most common tags
  most_common_tags = Counter(tags).most_common()
  plt.figure(num=None, figsize=(10, 8), dpi=500)
  plt.bar([tag for tag, _ in most_common_tags],
          [count for _, count in most_common_tags],
          color=[color.name for color in colors
                 if color.name != "lavender"])
  plt.title("Tags count for " + ",".join(TAGS))
  plt.xticks(rotation=30, horizontalalignment="right")
  plt.ylabel("count")
  plt.show()

  stop = timeit.default_timer()
  print("Time: ", stop - start)


if __name__ == "__main__":
  if args.sample_size:
    # Process a sample of it
    MSD_IDS = random.sample(list(MSD_SCORE_MATCHES), args.sample_size)
  else:
    # Process all the dataset
    MSD_IDS = list(MSD_SCORE_MATCHES)
  app(MSD_IDS)
