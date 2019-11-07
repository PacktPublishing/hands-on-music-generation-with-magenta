from multiprocessing import Manager


class Counter(object):

  def __init__(self,
               manager: Manager,
               total_count: int,
               print_step: int = 10):
    self._lock = manager.Lock()
    self._value = manager.Value('i', 0)
    self.total_count = total_count
    self.print_step = print_step

  def increment(self):
    with self._lock:
      self._value.value += 1
      if self._value.value % self.print_step == 0:
        print(f"Iteration count: {self._value.value}/{self.total_count}")

  def value(self):
    with self._lock:
      return self._value.value
