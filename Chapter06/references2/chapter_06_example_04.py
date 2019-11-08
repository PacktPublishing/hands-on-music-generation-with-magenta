"""
TODO how to stats artists
"""
import argparse
import collections
import random
import timeit
from itertools import cycle
from multiprocessing import Manager
from multiprocessing.pool import Pool
from typing import List, Optional

import matplotlib.pyplot as plt
import tables
from pretty_midi import PrettyMIDI, program_to_instrument_name

from lakh_utils import get_msd_score_matches, get_midi_path, \
  get_matched_midi_md5
from lakh_utils import msd_id_to_h5
from multiprocessing_utils import AtomicCounter

parser = argparse.ArgumentParser()
parser.add_argument("--sample_size", type=int, default=1000)
parser.add_argument("--path_dataset_dir", type=str, required=True)
parser.add_argument("--path_match_scores_file", type=str, required=True)
args = parser.parse_args()

MSD_SCORE_MATCHES = get_msd_score_matches(args.path_match_scores_file)


def get_programs(msd_id) -> Optional[list]:
  midi_md5 = get_matched_midi_md5(msd_id, MSD_SCORE_MATCHES)
  midi_path = get_midi_path(msd_id, midi_md5, "matched", args.path_dataset_dir)
  pm = PrettyMIDI(midi_path)
  programs = [instrument.program for instrument in pm.instruments
              if not instrument.is_drum]
  drums = [128 for instrument in pm.instruments if instrument.is_drum]
  if not programs and not drums:
    return
  return programs + drums


def process(msd_id: str, counter: AtomicCounter) -> Optional[dict]:
  try:
    with tables.open_file(msd_id_to_h5(msd_id, args.path_dataset_dir)) as h5:
      programs = get_programs(msd_id)
      return {"msd_id": msd_id, "programs": programs}
  except Exception as e:
    print(f"Exception during processing of {msd_id}: {e}")
    return
  finally:
    counter.increment()

def app(msd_ids: List[str]):
  start = timeit.default_timer()

  # TODO info
  with Pool(4) as pool:
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
  programs = []
  for result in results:
    for program in result["programs"]:
      programs.append(program)
  drums_programs = collections.Counter(programs).most_common(1)[0]
  most_common_programs = collections.Counter(programs).most_common(25)
  most_common_programs = [(program_to_instrument_name(program[0]), program[1])
                          for program in most_common_programs
                          if program[0] != 128]
  most_common_programs = [("Drums", drums_programs[1])] + most_common_programs
  print(most_common_programs)
  plt.hist(programs, bins=128)
  plt.title('Programs count')
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
