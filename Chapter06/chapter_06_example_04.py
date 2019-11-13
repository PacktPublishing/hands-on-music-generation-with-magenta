"""
Get statistics on instrument classes from the MIDI files.
"""
import argparse
import random
import timeit
from collections import Counter
from itertools import cycle
from multiprocessing import Manager
from multiprocessing.pool import Pool
from typing import List
from typing import Optional

import matplotlib.pyplot as plt
import tables
from bokeh.colors.groups import purple as colors
from pretty_midi import PrettyMIDI
from pretty_midi import program_to_instrument_class

from lakh_utils import get_matched_midi_md5
from lakh_utils import get_midi_path
from lakh_utils import get_msd_score_matches
from lakh_utils import msd_id_to_h5
from multiprocessing_utils import AtomicCounter

parser = argparse.ArgumentParser()
parser.add_argument("--sample_size", type=int, default=1000)
parser.add_argument("--pool_size", type=int, default=4)
parser.add_argument("--path_dataset_dir", type=str, required=True)
parser.add_argument("--path_match_scores_file", type=str, required=True)
args = parser.parse_args()

MSD_SCORE_MATCHES = get_msd_score_matches(args.path_match_scores_file)


def get_instrument_classes(msd_id) -> Optional[list]:
  midi_md5 = get_matched_midi_md5(msd_id, MSD_SCORE_MATCHES)
  midi_path = get_midi_path(msd_id, midi_md5, args.path_dataset_dir)
  pm = PrettyMIDI(midi_path)
  classes = [program_to_instrument_class(instrument.program)
             for instrument in pm.instruments
             if not instrument.is_drum]
  drums = ["Drums" for instrument in pm.instruments if instrument.is_drum]
  classes = classes + drums
  if not classes:
    raise Exception(f"No program classes for {msd_id}: "
                    f"{len(classes)}")
  return classes


def process(msd_id: str, counter: AtomicCounter) -> Optional[dict]:
  try:
    with tables.open_file(msd_id_to_h5(msd_id, args.path_dataset_dir)) as h5:
      classes = get_instrument_classes(msd_id)
      return {"msd_id": msd_id, "classes": classes}
  except Exception as e:
    print(f"Exception during processing of {msd_id}: {e}")
  finally:
    counter.increment()


def app(msd_ids: List[str]):
  start = timeit.default_timer()

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

  classes_list = [result["classes"] for result in results]
  classes = [c for classes in classes_list for c in classes]
  most_common_classes = Counter(classes).most_common()
  plt.figure(num=None, figsize=(10, 8), dpi=500)
  plt.bar([c for c, _ in most_common_classes],
          [count for _, count in most_common_classes],
          color=[color.name for color in colors
                 if color.name != "lavender"])
  plt.title('Instrument classes')
  plt.xticks(rotation=30, horizontalalignment="right")
  plt.ylabel('count')
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
