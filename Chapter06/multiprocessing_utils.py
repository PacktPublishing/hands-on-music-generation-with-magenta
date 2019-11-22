"""
Threading (multiprocessing) utilities.
"""

import time
from itertools import cycle
from multiprocessing import Manager
from multiprocessing.pool import Pool
from typing import Optional

import math


class AtomicCounter(object):
  """
  A thread safe (atomic) counter with automatic printing
  of global progression.
  """

  def __init__(self,
               manager: Manager,
               total_count: int,
               print_step: Optional[int] = None):
    """
    Constructs the counter with the given arguments

    :param manager: the manager has to be instanciated outside for shared
    resources
    :param total_count: the total number of elements to process
    :param print_step: the number of step between each print, initialized
    to sensible default if not provided
    """
    self._lock = manager.Lock()
    self._value = manager.Value('i', 0)
    self._total_count = total_count
    self._start_time = time.time()
    if print_step:
      self._print_step = print_step
    else:
      # Nearest (floored) power of 10 from the total count:
      # - if count is 456, the print step will be of 100
      # - if count is 55698, the print step will be of 10000
      if total_count < 10:
        self._print_step = 1
      else:
        self._print_step = int(10 ** (math.floor(math.log10(total_count))) / 10)

  def _print(self):
    if not self._value.value:
      print(f"Iteration count: {self._value.value}/{self._total_count}")
      return
    current_time = time.time() - self._start_time
    expected_time = (current_time / self._value.value) * self._total_count
    remaining_time = expected_time - current_time
    completed_percentage = (current_time / expected_time) * 100
    print(f"Iteration count: {self._value.value}/{self._total_count} ("
          f"elapsed: {int(current_time)} sec, "
          f"remaining: {int(remaining_time)} sec, "
          f"total: {int(expected_time)} sec, "
          f"completion: {int(completed_percentage)}%)")

  def increment(self):
    """
    Increments the counter and prints the value if the print_step is met
    """
    with self._lock:
      if self._value.value == 0:
        self._print()
      self._value.value += 1
      if self._value.value % self._print_step == 0:
        self._print()

  def value(self):
    """
    Returns the value for the counter
    """
    with self._lock:
      return self._value.value


def _process(x: int, counter: AtomicCounter):
  try:
    # Process here, you can return None
    pass
  except Exception as e:
    print(f"Exception during processing of {x}: {e}")
  finally:
    counter.increment()


if __name__ == "__main__":
  # Example usage
  with Pool(4) as pool:
    # Add elements to process here
    elements = []
    manager = Manager()
    counter = AtomicCounter(manager, len(elements))
    print("START")
    results = pool.starmap(_process, zip(elements, cycle([counter])))
    results = [result for result in results if result]
    print("END")
