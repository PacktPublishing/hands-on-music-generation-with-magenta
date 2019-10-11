import sys

import pretty_midi

# TODO rename append to merge
# TODO merge to different instruments and show in pretty midi
# TODO add to pretty different colors per instrument flag

def append():
  # Usage: python merge.py output file1 file2 file3 ...
  if len(sys.argv) <= 1:
    print("Usage: python merge.py output file1 file2 file3 ...")
    exit(0)
  output_filename = sys.argv[1]
  input_filenames = sys.argv[2:]

  print("Merging: " + str(input_filenames))

  # Create input midi object for each file
  input_midis = [pretty_midi.PrettyMIDI(f) for f in input_filenames]

  # Create output midi object with instrument (program 0)
  instrument = pretty_midi.Instrument(program=0)
  output_midi = pretty_midi.PrettyMIDI()
  output_midi.instruments.append(instrument)

  # Copy the notes from instruments 0 from each input midi to output midi. Adds
  # offset to note.start and note.end of the length of the current input midi at
  # each iteration to avoid superposition of each tracks.
  offset = 0
  for input_midi in input_midis:
    for note in input_midi.instruments[0].notes:
      note_shift = pretty_midi.Note(
        start=note.start + offset,
        end=note.end + offset,
        pitch=note.pitch,
        velocity=note.velocity)
      output_midi.instruments[0].notes.append(note_shift)
    offset += input_midi.get_end_time()

  # Write output midi file
  print("Output: " + str(output_filename))
  output_midi.write(output_filename)


if __name__ == "__main__":
  append()
