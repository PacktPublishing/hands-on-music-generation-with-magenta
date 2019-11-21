"""
Extract piano MIDI files corresponding to specific tags.
"""
import argparse
import random
import shutil
import timeit
from collections import Counter
from itertools import cycle
from multiprocessing import Manager
from multiprocessing.pool import Pool
from typing import List
from typing import Optional

import matplotlib.pyplot as plt
from bokeh.colors.groups import purple as colors

from multiprocessing_utils import AtomicCounter

parser = argparse.ArgumentParser()
parser.add_argument("--sample_size", type=int, default=1000)
parser.add_argument("--pool_size", type=int, default=4)
parser.add_argument("--path_dataset_dir", type=str, required=True)
parser.add_argument("--path_output_dir", type=str, required=True)
args = parser.parse_args()


# TODO extract from GMD

def process(msd_id: str, counter: AtomicCounter) -> Optional[dict]:
  try:
    # TODO
    pass
  except Exception as e:
    print(f"Exception during processing of {msd_id}: {e}")
  finally:
    counter.increment()


def app(msd_ids: List[str]):
  start = timeit.default_timer()

  # TODO cleanup
  shutil.rmtree(args.path_output_dir, ignore_errors=True)

  # TODO info
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

  # TODO histogram
  pm_pianos_list = [result["pm_pianos"] for result in results]
  pm_piano_lengths = [pm_piano.get_end_time()
                      for pm_pianos in pm_pianos_list
                      for pm_piano in pm_pianos]
  plt.figure(num=None, figsize=(10, 8), dpi=500)
  plt.hist(pm_piano_lengths, bins=100, color="darkmagenta")
  plt.title('Piano lengths')
  plt.ylabel('length (sec)')
  plt.show()

  tags_list = [result["tags"] for result in results]
  tags = [tag for tags in tags_list for tag in tags]
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
