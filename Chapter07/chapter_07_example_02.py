"""
Tensor validator and note sequence splitter (training and evaluation datasets)
for the MusicVAE model.
"""
import argparse

from magenta.models.music_vae.configs import CONFIG_MAP
from magenta.pipelines.dag_pipeline import DAGPipeline
from magenta.pipelines.dag_pipeline import DagInput
from magenta.pipelines.dag_pipeline import DagOutput
from magenta.pipelines.pipeline import Pipeline
from magenta.pipelines.pipeline import run_pipeline_serial
from magenta.pipelines.pipeline import tf_record_iterator
from magenta.pipelines.pipelines_common import RandomPartition
from magenta.protobuf.music_pb2 import NoteSequence

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, required=True)
parser.add_argument("--input", type=str, required=True)
parser.add_argument("--output_dir", type=str, required=True)
parser.add_argument("--eval_ratio", type=float, default=0.1)


class TensorValidator(Pipeline):

  def __init__(self, type_, name, config):
    super(TensorValidator, self).__init__(type_, type_, name)
    self._model = CONFIG_MAP[config]
    self._data_converter = self._model.data_converter

  def transform(self, note_sequence):
    tensors = self._data_converter.to_tensors(note_sequence)
    # For a config of splice each 2 bars, the tensor is split
    # on 2 bars with lengths like: <class 'tuple'> (32, 32, 32, 32, 32)
    if tensors.lengths:
      path = str(note_sequence).split('\n')[0:2]
      print(f"Ok tensor {tensors.lengths} for {path}")
      return [note_sequence]
    else:
      path = str(note_sequence).split('\n')[0:2]
      print(f"Empty tensor for {path}")
      return []


def partition(config: str, input: str, output_dir: str, eval_ratio: int):
  modes = ["eval", "train"]
  partitioner = RandomPartition(NoteSequence, modes, [eval_ratio])
  dag = {partitioner: DagInput(NoteSequence)}
  for mode in modes:
    validator = TensorValidator(NoteSequence, f"{mode}_TensorValidator", config)
    dag[validator] = partitioner[f"{mode}"]
    dag[DagOutput(f"{mode}")] = validator
  pipeline = DAGPipeline(dag)
  run_pipeline_serial(
    pipeline, tf_record_iterator(input, pipeline.input_type), output_dir)


def main():
  args = parser.parse_args()
  if args.eval_ratio < 0.0 or args.eval_ratio > 1.0:
    raise ValueError(f"Flag eval_ratio not in [0.0, 1.0]: {args.eval_ratio}")
  partition(args.config, args.input, args.output_dir, args.eval_ratio)


if __name__ == "__main__":
  main()
