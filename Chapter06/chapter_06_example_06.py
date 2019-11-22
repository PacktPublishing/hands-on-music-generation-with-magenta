"""
Extract piano MIDI files. Some piano tracks are split into multiple separate
piano instruments, in which case we keep them split and merge them into
multiple MIDI files.
"""

import argparse
import copy
import os
import random
import shutil
import timeit
from itertools import cycle
from multiprocessing import Manager
from multiprocessing.pool import Pool
from typing import List
from typing import Optional

import matplotlib.pyplot as plt
import tables
from pretty_midi import Instrument
from pretty_midi import PrettyMIDI

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
parser.add_argument("--path_output_dir", type=str, required=True)
args = parser.parse_args()

# The list of all MSD ids (we might process only a sample)
MSD_SCORE_MATCHES = get_msd_score_matches(args.path_match_scores_file)
PIANO_PROGRAMS = list(range(0, 8))


def extract_pianos(msd_id: str) -> List[PrettyMIDI]:
  """
  Extracts a list of PrettyMIDI instance of all the separate piano tracks
  from the given MSD id.

  :param msd_id: the MSD id
  :return: the list of PrettyMIDI instances of the separate piano tracks
  """
  os.makedirs(args.path_output_dir, exist_ok=True)
  midi_md5 = get_matched_midi_md5(msd_id, MSD_SCORE_MATCHES)
  midi_path = get_midi_path(msd_id, midi_md5, args.path_dataset_dir)
  pm = PrettyMIDI(midi_path)
  pm.instruments = [instrument for instrument in pm.instruments
                    if instrument.program in PIANO_PROGRAMS
                    and not instrument.is_drum]
  pm_pianos = []
  if len(pm.instruments) > 1:
    for piano_instrument in pm.instruments:
      pm_piano = copy.deepcopy(pm)
      pm_piano_instrument = Instrument(program=piano_instrument.program)
      pm_piano.instruments = [pm_piano_instrument]
      for note in piano_instrument.notes:
        pm_piano_instrument.notes.append(note)
      pm_pianos.append(pm_piano)
  else:
    pm_pianos.append(pm)
  for index, pm_piano in enumerate(pm_pianos):
    if len(pm_piano.instruments) != 1:
      raise Exception(f"Invalid number of piano {msd_id}: "
                      f"{len(pm_piano.instruments)}")
    if pm_piano.get_end_time() > 1000:
      raise Exception(f"Piano track too long {msd_id}: "
                      f"{pm_piano.get_end_time()}")
  return pm_pianos


def process(msd_id: str, counter: AtomicCounter) -> Optional[dict]:
  """
  Processes the given MSD id and increments the counter. The
  method will call the extract_pianos method and write the resulting MIDI
  files to disk.

  :param msd_id: the MSD id to process
  :param counter: the counter to increment
  :return: the dictionary containing the MSD id and the PrettyMIDI pianos,
  raises an exception if the file cannot be processed
  """
  try:
    with tables.open_file(msd_id_to_h5(msd_id, args.path_dataset_dir)) as h5:
      pm_pianos = extract_pianos(msd_id)
      for index, pm_piano in enumerate(pm_pianos):
        pm_piano.write(os.path.join(args.path_output_dir,
                                    f"{msd_id}_{index}.mid"))
      return {"msd_id": msd_id, "pm_pianos": pm_pianos}
  except Exception as e:
    print(f"Exception during processing of {msd_id}: {e}")
  finally:
    counter.increment()


def app(msd_ids: List[str]):
  start = timeit.default_timer()

  # Cleanup the output directory
  shutil.rmtree(args.path_output_dir, ignore_errors=True)

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

  # Creates an histogram for the piano lengths
  pm_pianos_list = [result["pm_pianos"] for result in results]
  pm_piano_lengths = [pm_piano.get_end_time()
                      for pm_pianos in pm_pianos_list
                      for pm_piano in pm_pianos]
  plt.figure(num=None, figsize=(10, 8), dpi=500)
  plt.hist(pm_piano_lengths, bins=100, color="darkmagenta")
  plt.title('Piano lengths')
  plt.ylabel('length (sec)')
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
