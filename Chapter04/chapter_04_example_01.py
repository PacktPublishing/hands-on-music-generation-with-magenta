"""
This example shows how to sample, interpolate and humanize a drums sequence
using MusicVAE and various configurations.
"""

import os
from typing import List

import magenta.music as mm
import tensorflow as tf
from magenta.models.music_vae import TrainedModel, configs
from magenta.music import DEFAULT_STEPS_PER_BAR
from magenta.protobuf.music_pb2 import NoteSequence
from six.moves import urllib

from note_sequence_utils import save_midi, save_plot


def download_checkpoint(model_name: str,
                        checkpoint_name: str,
                        target_dir: str):
  """
  Downloads a Magenta checkpoint to target directory.

  Target directory target_dir will be created if it does not already exist.

      :param model_name: magenta model name to download
      :param checkpoint_name: magenta checkpoint name to download
      :param target_dir: local directory in which to write the checkpoint
  """
  tf.gfile.MakeDirs(target_dir)
  checkpoint_target = os.path.join(target_dir, checkpoint_name)
  if not os.path.exists(checkpoint_target):
    response = urllib.request.urlopen(
      f"https://storage.googleapis.com/magentadata/models/"
      f"{model_name}/checkpoints/{checkpoint_name}")
    data = response.read()
    local_file = open(checkpoint_target, 'wb')
    local_file.write(data)
    local_file.close()


def get_model(name: str):
  """
  Returns the model instance from its name.

      :param name: the model name
  """
  checkpoint = name + ".tar"
  download_checkpoint("music_vae", checkpoint, "checkpoints")
  return TrainedModel(
    # Removes the .lohl in some training checkpoint which shares the same config
    configs.CONFIG_MAP[name.split(".")[0] if "." in name else name],
    # The batch size changes the number of sequences to be processed together,
    # we'll be working with maximum 6 sequences (during groove)
    batch_size=8,
    checkpoint_dir_or_path=os.path.join("checkpoints", checkpoint))


def sample(model_name: str,
           num_steps_per_sample: int) -> List[NoteSequence]:
  """
  Samples 2 sequences using the given model.
  """
  model = get_model(model_name)

  # Uses the model to sample 2 sequences,
  # with the number of steps and default temperature
  sample_sequences = model.sample(n=2, length=num_steps_per_sample)

  # Saves the midi and the plot in the sample folder
  save_midi(sample_sequences, "sample", model_name)
  save_plot(sample_sequences, "sample", model_name)

  return sample_sequences


def interpolate(model_name: str,
                sample_sequences: List[NoteSequence],
                num_steps_per_sample: int,
                num_output: int,
                total_bars: int) -> NoteSequence:
  """
  Interpolates between 2 sequences using the given model.
  """
  if len(sample_sequences) != 2:
    raise Exception(f"Wrong number of sequences, "
                    f"expected: 2, actual: {len(sample_sequences)}")
  if not sample_sequences[0].notes or not sample_sequences[1].notes:
    raise Exception(f"Empty note sequences, "
                    f"sequence 1 length: {len(sample_sequences[0].notes)}, "
                    f"sequence 2 length: {len(sample_sequences[1].notes)}")

  model = get_model(model_name)

  # Use the model to interpolate between the 2 input sequences,
  # with the number of output (counting the start and end sequence),
  # number of steps per sample and default temperature
  #
  # This might throw a NoExtractedExamplesError exception if the
  # sequences are not properly formed (for example if the sequences
  # are not quantized, a sequence is empty or not of the proper length).
  interpolate_sequences = model.interpolate(
    start_sequence=sample_sequences[0],
    end_sequence=sample_sequences[1],
    num_steps=num_output,
    length=num_steps_per_sample)

  # Saves the midi and the plot in the interpolate folder
  save_midi(interpolate_sequences, "interpolate", model_name)
  save_plot(interpolate_sequences, "interpolate", model_name)

  # Concatenates the resulting sequences (of length num_output) into one
  # single sequence.
  # The second parameter is a list containing the number of seconds
  # for each input sequence. This is useful if some of the input
  # sequences do not have notes at the end (for example the last
  # note ends at 3.5 seconds instead of 4)
  interpolate_sequence = mm.sequences_lib.concatenate_sequences(
    interpolate_sequences, [4] * num_output)

  # Saves the midi and the plot in the merge folder,
  # with the plot having total_bars size
  save_midi(interpolate_sequence, "merge", model_name)
  save_plot(interpolate_sequence, "merge", model_name,
            plot_max_length_bar=total_bars,
            bar_fill_alphas=[0.50, 0.50, 0.05, 0.05])

  return interpolate_sequence


def groove(model_name: str,
           interpolate_sequence: NoteSequence,
           num_steps_per_sample: int,
           num_output: int,
           total_bars: int) -> NoteSequence:
  """
  Adds groove to the given sequence by splitting it in manageable sequences
  and using the given model to humanize it.
  """
  model = get_model(model_name)

  # Split the sequences in chunks of 4 seconds (which is 2 bars at 120 qpm),
  # which is necessary since the model is trained for 2 bars
  split_interpolate_sequences = mm.sequences_lib.split_note_sequence(
    interpolate_sequence, 4)

  if len(split_interpolate_sequences) != num_output:
    raise Exception(f"Wrong number of interpolate size, "
                    f"expected: 10, actual: {len(split_interpolate_sequences)}")

  # Uses the model to encode the list of sequences, returning the encoding
  # (also called z or latent vector) which will the used in the decoding,
  # The other values mu and sigma are not used, but kept in the code for
  # clarity.
  #
  # The resulting array shape is (a, b), where a is the number of
  # split sequences (should correspond to num_output), and b is the encoding
  # size.
  #
  # This might throw a NoExtractedExamplesError exception if the
  # sequences are not properly formed (for example if the sequences
  # are not quantized, a sequence is empty or not of the proper length).
  encoding, mu, sigma = model.encode(
    note_sequences=split_interpolate_sequences)

  # Uses the model to decode the encoding (also called z or latent vector),
  # returning a list of humanized sequence with one element per encoded
  # sequences (each of length num_steps_per_sample).
  groove_sequences = model.decode(
    z=encoding, length=num_steps_per_sample)

  # Concatenates the resulting sequences (of length num_output) into one
  # single sequence.
  groove_sequence = mm.sequences_lib.concatenate_sequences(
    groove_sequences, [4] * num_output)

  # Saves the midi and the plot in the groove folder,
  # with the plot having total_bars size
  save_midi(groove_sequence, "groove", model_name)
  save_plot(groove_sequence, "groove", model_name,
            plot_max_length_bar=total_bars, show_velocity=True,
            bar_fill_alphas=[0.50, 0.50, 0.05, 0.05])

  return groove_sequence


def app(unused_argv):
  # Number of interpolated sequences (counting the start and end sequences)
  num_output = 6

  # Number of bar per sample, also giving the size of the interpolation splits
  num_bar_per_sample = 2

  # Number of steps per sample and interpolation splits
  num_steps_per_sample = num_bar_per_sample * DEFAULT_STEPS_PER_BAR

  # The total number of bars
  total_bars = num_output * num_bar_per_sample

  # Samples 2 new sequences with "lokl" model which is optimized for sampling
  generated_sample_sequences = sample("cat-drums_2bar_small.lokl",
                                      num_steps_per_sample)

  # Interpolates between the 2 sequences, returns 1 sequence
  # with "hikl" which is optimized for sampling
  generated_interpolate_sequence = interpolate("cat-drums_2bar_small.hikl",
                                               generated_sample_sequences,
                                               num_steps_per_sample,
                                               num_output,
                                               total_bars)

  # Adds groove to the whole sequence
  generated_groove_sequence = groove("groovae_2bar_humanize",
                                     generated_interpolate_sequence,
                                     num_steps_per_sample,
                                     num_output,
                                     total_bars)

  print(f"Generated groove sequence total time: "
        f"{generated_groove_sequence.total_time}")

  return 0


if __name__ == "__main__":
  tf.app.run(app)
