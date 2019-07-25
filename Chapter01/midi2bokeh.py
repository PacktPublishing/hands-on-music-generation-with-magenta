import sys

import bokeh
import bokeh.plotting
import math
from bokeh.colors.groups import purple as colors
from bokeh.io import output_file, show
from bokeh.models import BoxAnnotation, ColumnDataSource
from bokeh.models import Range1d, Label
from pretty_midi import PrettyMIDI

BOX_HORIZONTAL_FILL_ALPHA_EVEN = 0.15
BOX_HORIZONTAL_FILL_ALPHA_ODD = 0.0
BOX_HORIZONTAL_LINE_ALPHA = 0.5

BOX_VERTICAL_FILL_ALPHA_EVEN = 0.15
BOX_VERTICAL_FILL_ALPHA_ODD = 0.0
BOX_VERTICAL_LINE_ALPHA = 0.75

BOX_BEAT_VERTICAL_FILL_ALPHA = 0
BOX_BEAT_VERTICAL_LINE_ALPHA = 0.3

# "sec" or "bar"
TIME_SCALING = "sec"


def get_qpm(pm):
  """Returns the first tempo change that is not zero, raises exception if not found"""
  qpm = None
  for tempo_change in pm.get_tempo_changes():
    if tempo_change.min() > 0 \
        and tempo_change.max() > 0 \
        and tempo_change.min() == tempo_change.max():
      if qpm:
        raise Exception("Multiple tempo changes are not supported " + str(
          pm.get_tempo_changes()))
      qpm = tempo_change.min()
  if not qpm:
    raise Exception(
      "Cannot find suitable qpm in " + str(pm.get_tempo_changes()))
  return qpm


def get_time_signature(pm):
  """Returns the first signature, raises exception if more than one signature"""
  if len(pm.time_signature_changes) != 1:
    raise Exception("Cannot find suitable time signature in " + str(
      pm.time_signature_changes))
  return pm.time_signature_changes[0]


def get_time_start():
  if TIME_SCALING == "sec":
    return 0
  elif TIME_SCALING == "bar":
    return 1
  else:
    raise Exception("Unknown time scaling " + TIME_SCALING)


def scale_time(pm, time):
  if TIME_SCALING == "sec":
    return time
  elif TIME_SCALING == "bar":
    return (time / (get_qpm(pm) / 60)) + 1
  else:
    raise Exception("Unknown time scaling " + TIME_SCALING)


def get_box_horizontal(pitch, fill_alpha, line_alpha):
  box = BoxAnnotation(bottom=pitch, top=pitch + 1, fill_color="gray",
                      fill_alpha=fill_alpha, line_alpha=line_alpha)
  box.level = "underlay"
  return box


def get_box_vertical(bar, fill_alpha, line_alpha):
  box = BoxAnnotation(left=bar, right=bar + 1, fill_color="gray",
                      fill_alpha=fill_alpha, line_alpha=line_alpha)
  box.level = "underlay"
  return box


def get_box_beat_vertical(bar, beat, beat_per_bar, fill_alpha, line_alpha):
  box = BoxAnnotation(left=bar + beat / beat_per_bar,
                      right=bar + beat / beat_per_bar + beat / beat_per_bar,
                      fill_color=None,
                      fill_alpha=fill_alpha,
                      line_alpha=line_alpha)
  box.level = "underlay"
  return box


def get_label(note):
  label = Label(x=-20, y=note + 0.2, x_units="screen", text=str(note),
                render_mode="css", text_font_size="8pt")
  return label


def plot_midi_file(filename):
  pm = PrettyMIDI(filename)
  return plot_midi(pm)


def plot_midi(pm):
  p = bokeh.plotting.figure(tools="reset,hover,previewsave,wheel_zoom,pan")

  p.select(dict(type=bokeh.models.HoverTool)).tooltips = (
    {"pitch": "@top",
     "velocity": "@velocity",
     "duration": "@duration",
     "start_time": "@left",
     "end_time": "@right"})

  data = dict(
    top=[],
    bottom=[],
    left=[],
    right=[],
    duration=[],
    velocity=[],
    color=[],
  )

  pitch_min = 127
  pitch_max = 0
  first_note = None
  last_note = None
  for instrument in pm.instruments:
    for note in instrument.notes:
      pitch_max = max(pitch_max, note.pitch)
      pitch_min = min(pitch_min, note.pitch)
      color_index = (note.pitch - 37) % len(colors)
      start = scale_time(pm, note.start)
      end = scale_time(pm, (note.start + (note.end - note.start)))
      data["top"].append(note.pitch)
      data["bottom"].append(note.pitch + 1)
      data["left"].append(start)
      data["right"].append(end)
      data["duration"].append(end - start)
      data["velocity"].append(note.velocity)
      data["color"].append(colors[color_index].lighten(0.25))
      if not first_note:
        first_note = note
      last_note = note

  if not first_note or not last_note:
    raise Exception("No note in the file")

  source = ColumnDataSource(data=data)
  p.quad(left="left",
         right="right",
         top="top",
         bottom="bottom",
         line_alpha=1,
         line_color="black",
         color="color",
         source=source)

  for pitch in range(pitch_min, pitch_max + 1):
    fill_alpha = BOX_HORIZONTAL_FILL_ALPHA_EVEN if pitch % 2 == 0 else BOX_HORIZONTAL_FILL_ALPHA_ODD
    box = get_box_horizontal(pitch, fill_alpha, BOX_HORIZONTAL_LINE_ALPHA)
    p.add_layout(box)
    label = get_label(pitch)
    p.add_layout(label)

  start = math.floor(scale_time(pm, first_note.start))
  end = math.floor(scale_time(pm, last_note.start))

  for bar in range(start, end + 1):
    beat_per_bar = get_time_signature(
      pm).denominator if TIME_SCALING == 'bar' else 1
    # change alpha each beat_per_bar
    # (if time signature is 3/4 we'll change each 4 bars)
    fill_alpha = BOX_VERTICAL_FILL_ALPHA_EVEN \
      if math.ceil(bar / beat_per_bar) % 2 == 0 \
      else BOX_VERTICAL_FILL_ALPHA_ODD
    box = get_box_vertical(bar, fill_alpha, BOX_VERTICAL_LINE_ALPHA)
    p.add_layout(box)
    for beat in range(0, beat_per_bar):
      box = get_box_beat_vertical(
        bar,
        beat,
        beat_per_bar,
        BOX_BEAT_VERTICAL_FILL_ALPHA,
        BOX_BEAT_VERTICAL_LINE_ALPHA)
      p.add_layout(box)
      if beat != 0 and TIME_SCALING == 'bar':
        label = Label(
          x=bar + beat / beat_per_bar - 0.02,
          y=-24,
          y_units="screen",
          text=str(bar) + "." + str(beat),
          render_mode="css",
          text_font_size="7pt")
        p.add_layout(label)

  p.xgrid.grid_line_color = "black"
  p.ygrid.grid_line_color = None

  p.xgrid.grid_line_alpha = 0.30
  p.xgrid.grid_line_width = 1
  p.xgrid.grid_line_color = "black"

  p.xaxis.bounds = (start, end + 1)
  p.yaxis.bounds = (pitch_min, pitch_max + 1)

  p.yaxis.major_label_text_alpha = 0
  p.yaxis.major_tick_line_alpha = 0
  p.yaxis.minor_tick_line_alpha = 0

  p.xaxis.ticker = bokeh.models.SingleIntervalTicker(interval=1)
  p.xaxis.minor_tick_line_alpha = 0

  p.plot_width = 1200
  p.plot_height = 300
  p.xaxis.axis_label = "time (" + TIME_SCALING + ")"
  p.yaxis.axis_label = "pitch (MIDI)"

  p.x_range = Range1d(start, end + 1)
  p.y_range = Range1d(pitch_min, pitch_max + 1)

  return p


if __name__ == "__main__":
  for midi_file in sys.argv[1:]:
    plot_file = midi_file.replace(".mid", ".html")
    print("Plotting midi file " + midi_file + " to " + plot_file)
    output_file(midi_file.replace(".mid", ".html"))
    p = plot_midi_file(midi_file)
    show(p)
  sys.exit(0)
