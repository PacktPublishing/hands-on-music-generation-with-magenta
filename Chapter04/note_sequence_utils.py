"""
Common utilities for the book's code.
"""

import os
import time
from typing import Union, List, Optional

import magenta.music as mm
from magenta.protobuf.music_pb2 import NoteSequence
from visual_midi import Plotter


def save_midi(sequences: Union[NoteSequence, List[NoteSequence]],
              output_dir: Optional[str] = None,
              prefix: str = "sequence"):
  """
  Writes the sequences as MIDI files to the "output" directory, with the
  filename pattern "<prefix>_<index>_<date_time>" and "mid" as extension.

      :param sequences: a NoteSequence or list of NoteSequence to be saved
      :param output_dir: an optional subdirectory in the output directory
      :param prefix: an optional prefix for each file
  """
  output_dir = os.path.join("output", output_dir) if output_dir else "output"
  os.makedirs(output_dir, exist_ok=True)
  if not isinstance(sequences, list):
    sequences = [sequences]
  for (index, sequence) in enumerate(sequences):
    date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
    filename = f"{prefix}_{index:02}_{date_and_time}.mid"
    path = os.path.join(output_dir, filename)
    mm.midi_io.note_sequence_to_midi_file(sequence, path)
    print(f"Generated midi file: {os.path.abspath(path)}")


def save_plot(sequences: Union[NoteSequence, List[NoteSequence]],
              output_dir: Optional[str] = None,
              prefix: str = "sequence",
              **kwargs):
  """
  Writes the sequences as HTML plot files to the "output" directory, with the
  filename pattern "<prefix>_<index>_<date_time>" and "html" as extension.

      :param sequences: a NoteSequence or list of NoteSequence to be saved
      :param output_dir: an optional subdirectory in the output directory
      :param prefix: an optional prefix for each file
      :param kwargs: the keyword arguments to pass to the Plotter instance
  """
  output_dir = os.path.join("output", output_dir) if output_dir else "output"
  os.makedirs(output_dir, exist_ok=True)
  if not isinstance(sequences, list):
    sequences = [sequences]
  for (index, sequence) in enumerate(sequences):
    date_and_time = time.strftime("%Y-%m-%d_%H%M%S")
    filename = f"{prefix}_{index:02}_{date_and_time}.html"
    path = os.path.join(output_dir, filename)
    midi = mm.midi_io.note_sequence_to_pretty_midi(sequence)
    plotter = Plotter(**kwargs)
    plotter.save(midi, path)
    print(f"Generated plot file: {os.path.abspath(path)}")
