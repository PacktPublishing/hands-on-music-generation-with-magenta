"""
Extract techno (four on the floor) drum rhythms.
"""
import argparse
import copy
import glob
import os
import random
import shutil
import timeit
from itertools import cycle
from multiprocessing import Manager
from multiprocessing.pool import Pool
from typing import List
from typing import Optional

import math
import matplotlib.pyplot as plt
from pretty_midi import Instrument
from pretty_midi import PrettyMIDI

from multiprocessing_utils import AtomicCounter

parser = argparse.ArgumentParser()
parser.add_argument("--sample_size", type=int, required=True, default=1000)
parser.add_argument("--pool_size", type=int, required=True, default=4)
parser.add_argument("--path_dataset_dir", type=str, required=True)
parser.add_argument("--path_dataset_dir", type=str, required=True)
parser.add_argument("--path_output_dir", type=str, required=True)
parser.add_argument("--bass_drums_on_beat_threshold", type=float, required=True,
                    default=0)
args = parser.parse_args()

MIDI_PATHS = glob.glob(os.path.join(args.path_dataset_dir, "**", "*.mid"),
                       recursive=True)


def extract_drums(midi_path: str) -> Optional[PrettyMIDI]:
  os.makedirs(args.path_output_dir, exist_ok=True)
  pm = PrettyMIDI(midi_path)
  pm_drums = copy.deepcopy(pm)
  pm_drums.instruments = [instrument for instrument in pm_drums.instruments
                          if instrument.is_drum]
  if len(pm_drums.instruments) > 1:
    # Some drum tracks are split, we can merge them
    drums = Instrument(program=0, is_drum=True)
    for instrument in pm_drums.instruments:
      for note in instrument.notes:
        drums.notes.append(note)
    pm_drums.instruments = [drums]
  if len(pm_drums.instruments) != 1:
    raise Exception(f"Invalid number of drums {midi_path}: "
                    f"{len(pm_drums.instruments)}")
  return pm_drums


def get_bass_drums_on_beat(pm_drums: PrettyMIDI) -> float:
  beats = pm_drums.get_beats()
  bass_drums = [note.start for note in pm_drums.instruments[0].notes
                if note.pitch == 35 or note.pitch == 36]
  bass_drums_on_beat = []
  for beat in beats:
    beat_has_bass_drum = False
    for bass_drum in bass_drums:
      if math.isclose(beat, bass_drum):
        beat_has_bass_drum = True
        break
    bass_drums_on_beat.append(True if beat_has_bass_drum else False)
  num_bass_drums_on_beat = len([bd for bd in bass_drums_on_beat if bd])
  return num_bass_drums_on_beat / len(bass_drums_on_beat)


def process(midi_path: str, counter: AtomicCounter) -> Optional[dict]:
  try:
    pm_drums = extract_drums(midi_path)
    bass_drums_on_beat = get_bass_drums_on_beat(pm_drums)
    if bass_drums_on_beat >= args.bass_drums_on_beat_threshold:
      midi_filename = os.path.basename(midi_path)
      pm_drums.write(os.path.join(args.path_output_dir, f"{midi_filename}.mid"))
    else:
      raise Exception(f"Not on beat {midi_path}: {bass_drums_on_beat}")
    return {"midi_path": midi_path,
            "pm_drums": pm_drums,
            "bass_drums_on_beat": bass_drums_on_beat}
  except Exception as e:
    pass
    # print(f"Exception during processing of {midi_path}: {e}")
  finally:
    counter.increment()


def app(midi_paths: List[str]):
  start = timeit.default_timer()

  # TODO cleanup
  shutil.rmtree(args.path_output_dir, ignore_errors=True)

  # TODO info
  with Pool(args.pool_size) as pool:
    manager = Manager()
    counter = AtomicCounter(manager, len(midi_paths), 1000)
    print("START")
    results = pool.starmap(process, zip(midi_paths, cycle([counter])))
    results = [result for result in results if result]
    print("END")
    results_percentage = len(results) / len(midi_paths) * 100
    print(f"Number of tracks: {len(MIDI_PATHS)}, "
          f"number of tracks in sample: {len(midi_paths)}, "
          f"number of results: {len(results)} "
          f"({results_percentage:.2f}%)")

  # TODO histogram
  pm_drums = [result["pm_drums"] for result in results]
  pm_drums_lengths = [pm.get_end_time() for pm in pm_drums]
  plt.hist(pm_drums_lengths, bins=100)
  plt.title('Drums lengths')
  plt.ylabel('length (sec)')
  plt.show()

  bass_drums_on_beat = [result["bass_drums_on_beat"] for result in results]
  plt.hist(bass_drums_on_beat, bins=100)
  plt.title('Bass drums on beat')
  plt.ylabel('count')
  plt.show()

  stop = timeit.default_timer()
  print("Time: ", stop - start)


if __name__ == "__main__":
  if args.sample_size:
    # Process a sample of it
    MIDI_PATHS_SAMPLE = random.sample(list(MIDI_PATHS), args.sample_size)
  else:
    # Process all the dataset
    MIDI_PATHS_SAMPLE = list(MIDI_PATHS)
  app(MIDI_PATHS_SAMPLE)
