import math

from pretty_midi import PrettyMIDI

midi_path = "D:\\project\\dataset\\techno_midi\\drums\\v9\\TRIFOZS128F42A7B8B.mid"
pm = PrettyMIDI(midi_path)
# plotter = Plotter(plot_bar_range_start=0, plot_bar_range_stop=16)
# plotter.show(pm, os.path.join("output", "out.html"))

beats = pm.get_beats()
print(beats)

bass_drums = [note.start for note in pm.instruments[0].notes
              if note.pitch == 35 or note.pitch == 36]
print(bass_drums)

bass_drums_on_beat = []
for beat in beats:
  beat_has_bass_drum = False
  for bass_drum in bass_drums:
    if math.isclose(beat, bass_drum):
      beat_has_bass_drum = True
      break
  bass_drums_on_beat.append(True if beat_has_bass_drum else False)
print(bass_drums_on_beat)

num_bass_drums_on_beat = len([bd for bd in bass_drums_on_beat if bd])
percentage_bass_drums_on_beat = (num_bass_drums_on_beat /
                                 len(bass_drums_on_beat) * 100)
print(f"{num_bass_drums_on_beat}/{len(bass_drums_on_beat)} "
      f"({percentage_bass_drums_on_beat:.2f}%)")
print()
