import os
import sys
from enum import Enum

import bokeh
import bokeh.plotting
import math
from bokeh.colors.groups import purple as colors
from bokeh.embed import file_html
from bokeh.io import output_file, show
from bokeh.layouts import column
from bokeh.models import BoxAnnotation, ColumnDataSource
from bokeh.models import Range1d, Label
from bokeh.models.callbacks import CustomJS
from bokeh.models.widgets.buttons import Button
from bokeh.resources import CDN
from pretty_midi import PrettyMIDI

BOX_HORIZONTAL_FILL_ALPHA_EVEN = 0.15
BOX_HORIZONTAL_FILL_ALPHA_ODD = 0.0
BOX_HORIZONTAL_LINE_ALPHA = 0.5

BOX_VERTICAL_FILL_ALPHA_EVEN = 0.15
BOX_VERTICAL_FILL_ALPHA_ODD = 0.0
BOX_VERTICAL_LINE_ALPHA = 0.75

BOX_BEAT_VERTICAL_FILL_ALPHA = 0
BOX_BEAT_VERTICAL_LINE_ALPHA = 0.3


class TimeScaling(Enum):
  SEC = 1
  BAR = 2

  def __str__(self):
    return self.name


class Plotter:

  def __init__(self,
               time_scaling=TimeScaling.SEC,
               max_bar=None,
               live_reload=False):
    self._time_scaling = time_scaling
    self._max_bar = max_bar
    self._live_reload = live_reload
    self._show_counter = 0

  def _get_qpm(self, pretty_midi):
    """Returns the first tempo change that is not zero,
    raises exception if not found"""
    qpm = None
    for tempo_change in pretty_midi.get_tempo_changes():
      if tempo_change.min() > 0 \
          and tempo_change.max() > 0 \
          and tempo_change.min() == tempo_change.max():
        if qpm:
          raise Exception("Multiple tempo changes are not supported "
                          + str(pretty_midi.get_tempo_changes()))
        qpm = tempo_change.min()
    if not qpm:
      raise Exception("Cannot find suitable qpm in "
                      + str(pretty_midi.get_tempo_changes()))
    return qpm

  def _get_time_signature(self, pretty_midi):
    """Returns the first signature,
    raises exception if more than one signature"""
    if len(pretty_midi.time_signature_changes) != 1:
      raise Exception("Cannot find suitable time signature in "
                      + str(pretty_midi.time_signature_changes))
    return pretty_midi.time_signature_changes[0]

  def _get_time_start(self):
    if self._time_scaling is TimeScaling.SEC:
      return 0
    elif self._time_scaling is TimeScaling.BAR:
      return 1
    else:
      raise Exception("Unknown time scaling " + str(self._time_scaling))

  def _scale_time(self, qpm, time):
    if self._time_scaling is TimeScaling.SEC:
      return time
    elif self._time_scaling is TimeScaling.BAR:
      return (time / (qpm / 60)) + 1
    else:
      raise Exception("Unknown time scaling " + str(self._time_scaling))

  @staticmethod
  def _get_box_horizontal(pitch, fill_alpha, line_alpha):
    box = BoxAnnotation(bottom=pitch, top=pitch + 1, fill_color="gray",
                        fill_alpha=fill_alpha, line_alpha=line_alpha)
    box.level = "underlay"
    return box

  @staticmethod
  def _get_box_vertical(bar, fill_alpha, line_alpha):
    box = BoxAnnotation(left=bar, right=bar + 1, fill_color="gray",
                        fill_alpha=fill_alpha, line_alpha=line_alpha)
    box.level = "underlay"
    return box

  @staticmethod
  def _get_box_beat_vertical(bar, beat, beat_per_bar,
                             fill_alpha, line_alpha):
    box = BoxAnnotation(left=bar + beat / beat_per_bar,
                        right=bar + beat / beat_per_bar + beat / beat_per_bar,
                        fill_color=None,
                        fill_alpha=fill_alpha,
                        line_alpha=line_alpha)
    box.level = "underlay"
    return box

  @staticmethod
  def _get_label(note):
    label = Label(x=-20, y=note + 0.2, x_units="screen", text=str(note),
                  render_mode="css", text_font_size="8pt")
    return label

  def _is_note_filtered(self, pretty_midi, note):
    if not self._max_bar:
      return True
    min_time = int(pretty_midi.get_end_time() - self._max_bar + 1)
    if note.start < min_time:
      return False
    return True

  def plot_midi(self, pretty_midi):
    plot = bokeh.plotting.figure(tools="reset,hover,previewsave,wheel_zoom,pan")

    plot.select(dict(type=bokeh.models.HoverTool)).tooltips = (
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
    for instrument in pretty_midi.instruments:
      for note in instrument.notes:
        if self._is_note_filtered(pretty_midi, note):
          pitch_max = max(pitch_max, note.pitch)
          pitch_min = min(pitch_min, note.pitch)
          color_index = (note.pitch - 37) % len(colors)
          start = self._scale_time(self._get_qpm(pretty_midi),
                                   note.start)
          end = self._scale_time(self._get_qpm(pretty_midi),
                                 note.start + (note.end - note.start))
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
    plot.quad(left="left",
              right="right",
              top="top",
              bottom="bottom",
              line_alpha=1,
              line_color="black",
              color="color",
              source=source)

    for pitch in range(pitch_min, pitch_max + 1):
      if pitch % 2 == 0:
        fill_alpha = BOX_HORIZONTAL_FILL_ALPHA_EVEN
      else:
        fill_alpha = BOX_HORIZONTAL_FILL_ALPHA_ODD
      box = self._get_box_horizontal(pitch, fill_alpha,
                                     BOX_HORIZONTAL_LINE_ALPHA)
      plot.add_layout(box)
      label = self._get_label(pitch)
      plot.add_layout(label)

    start = math.floor(self._scale_time(self._get_qpm(pretty_midi),
                                        first_note.start))
    end = math.floor(self._scale_time(self._get_qpm(pretty_midi),
                                      last_note.start))

    for bar in range(start, end + 1):
      if self._time_scaling is TimeScaling.BAR:
        beat_per_bar = self._get_time_signature(pretty_midi).denominator
      elif self._time_scaling is TimeScaling.SEC:
        beat_per_bar = 1
      else:
        raise Exception("Unknown time scaling " + str(self._time_scaling))
      # change alpha each beat_per_bar
      # (if time signature is 3/4 we'll change each 4 bars)
      fill_alpha = BOX_VERTICAL_FILL_ALPHA_EVEN \
        if math.ceil(bar / beat_per_bar) % 2 == 0 \
        else BOX_VERTICAL_FILL_ALPHA_ODD
      box = self._get_box_vertical(bar, fill_alpha, BOX_VERTICAL_LINE_ALPHA)
      plot.add_layout(box)
      for beat in range(0, beat_per_bar):
        box = self._get_box_beat_vertical(
          bar,
          beat,
          beat_per_bar,
          BOX_BEAT_VERTICAL_FILL_ALPHA,
          BOX_BEAT_VERTICAL_LINE_ALPHA)
        plot.add_layout(box)
        if beat != 0 and self._time_scaling is TimeScaling.BAR:
          label = Label(
            x=bar + beat / beat_per_bar - 0.02,
            y=-24,
            y_units="screen",
            text=str(bar) + "." + str(beat),
            render_mode="css",
            text_font_size="7pt")
          plot.add_layout(label)

    plot.xgrid.grid_line_color = "black"
    plot.ygrid.grid_line_color = None

    plot.xgrid.grid_line_alpha = 0.30
    plot.xgrid.grid_line_width = 1
    plot.xgrid.grid_line_color = "black"

    plot.xaxis.bounds = (start, end + 1)
    plot.yaxis.bounds = (pitch_min, pitch_max + 1)

    plot.yaxis.major_label_text_alpha = 0
    plot.yaxis.major_tick_line_alpha = 0
    plot.yaxis.minor_tick_line_alpha = 0

    plot.xaxis.ticker = bokeh.models.SingleIntervalTicker(interval=1)
    plot.xaxis.minor_tick_line_alpha = 0

    plot.plot_width = 1200
    plot.plot_height = 300
    plot.xaxis.axis_label = "time (" + str(self._time_scaling) + ")"
    plot.yaxis.axis_label = "pitch (MIDI)"

    plot.x_range = Range1d(start, end + 1)
    plot.y_range = Range1d(pitch_min, pitch_max + 1)

    if self._live_reload:
      callback = CustomJS(code="clearInterval(liveReloadInterval)")
      button = Button(label="stop live reload")
      button.js_on_click(callback)
      layout = column(button, plot)
    else:
      layout = column(plot)

    return layout

  def show(self, pretty_midi, plot_file):
    plot = self.plot_midi(pretty_midi)
    if self._live_reload:
      html = file_html(plot, CDN, template_variables={'plot_script': 'lol'})
      html = html.replace("</head>", """
              <script type="text/javascript">
                var liveReloadInterval = window.setInterval(function(){
                  location.reload();
                }, 2000);
              </script>
              </head>""")
      with open(plot_file, 'w') as file:
        file.write(html)
      if self._show_counter == 0:
        import webbrowser
        webbrowser.open("file://" + os.path.realpath(plot_file), new=2)
    else:
      output_file(plot_file)
      show(plot)
    self._show_counter += 1
    return plot


if __name__ == "__main__":
  for midi_file in sys.argv[1:]:
    plot_file = midi_file.replace(".mid", ".html")
    print("Plotting midi file " + midi_file + " to " + plot_file)
    pretty_midi = PrettyMIDI(midi_file)
    plotter = Plotter(time_scaling=TimeScaling.SEC)
    plotter.show(pretty_midi, plot_file)
  sys.exit(0)
