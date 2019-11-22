import argparse

from pretty_midi import PrettyMIDI
from visual_midi import Plotter

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, required=True)
args = parser.parse_args()

if __name__ == "__main__":
  pm = PrettyMIDI(args.file)
  plot = Plotter(plot_bar_range_start=0, plot_bar_range_stop=8)
  plot.show(pm, "output.html")
  print(pm.get_tempo_changes())
  print(pm.time_signature_changes)
  print(pm.get_beats())
  print(pm.get_downbeats())
