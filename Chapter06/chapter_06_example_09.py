"""
Extract drums tracks from GMD.
"""

import argparse
from typing import Optional

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
