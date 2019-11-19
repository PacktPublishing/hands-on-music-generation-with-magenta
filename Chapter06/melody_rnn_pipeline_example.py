import os

import tensorflow as tf
from magenta.models.melody_rnn import melody_rnn_config_flags
from magenta.models.melody_rnn.melody_rnn_pipeline import EncoderPipeline
from magenta.pipelines import dag_pipeline
from magenta.pipelines import melody_pipelines
from magenta.pipelines import note_sequence_pipelines
from magenta.pipelines import pipeline
from magenta.pipelines import pipelines_common
from magenta.protobuf import music_pb2

flags = tf.app.flags
FLAGS = tf.app.flags.FLAGS
flags.DEFINE_string(
  'input', None,
  'TFRecord to read NoteSequence protos from.')
flags.DEFINE_string(
  'output_dir', None,
  'Directory to write training and eval TFRecord files. The TFRecord files '
  'are populated with  SequenceExample protos.')
flags.DEFINE_float(
  'eval_ratio', 0.1,
  'Fraction of input to set aside for eval set. Partition is randomly '
  'selected.')
flags.DEFINE_string(
  'log', 'INFO',
  'The threshold for what messages will be logged DEBUG, INFO, WARN, ERROR, '
  'or FATAL.')


def get_pipeline(config, eval_ratio=0.0):
  partitioner = pipelines_common.RandomPartition(
    music_pb2.NoteSequence,
    ['eval_melodies', 'training_melodies'],
    [eval_ratio])
  dag = {partitioner: dag_pipeline.DagInput(music_pb2.NoteSequence)}

  for mode in ['eval', 'training']:
    time_change_splitter = note_sequence_pipelines.TimeChangeSplitter(
      name='TimeChangeSplitter_' + mode)
    transposition_pipeline = note_sequence_pipelines.TranspositionPipeline(
      (0, 12), name='TranspositionPipeline_' + mode)
    quantizer = note_sequence_pipelines.Quantizer(
      steps_per_quarter=config.steps_per_quarter, name='Quantizer_' + mode)
    melody_extractor = melody_pipelines.MelodyExtractor(
      min_bars=15, max_steps=1024, min_unique_pitches=5,
      gap_bars=1.0, ignore_polyphonic_notes=False,
      name='MelodyExtractor_' + mode)
    encoder_pipeline = EncoderPipeline(config, name='EncoderPipeline_' + mode)

    dag[time_change_splitter] = partitioner[mode + '_melodies']
    dag[quantizer] = time_change_splitter
    dag[transposition_pipeline] = quantizer
    dag[melody_extractor] = transposition_pipeline
    dag[encoder_pipeline] = melody_extractor
    dag[dag_pipeline.DagOutput(mode + '_melodies')] = encoder_pipeline

  return dag_pipeline.DAGPipeline(dag)


def main(unused_argv):
  tf.logging.set_verbosity(FLAGS.log)

  config = melody_rnn_config_flags.config_from_flags()
  pipeline_instance = get_pipeline(config, eval_ratio=FLAGS.eval_ratio)

  FLAGS.input = os.path.expanduser(FLAGS.input)
  FLAGS.output_dir = os.path.expanduser(FLAGS.output_dir)
  pipeline.run_pipeline_serial(
    pipeline_instance,
    pipeline.tf_record_iterator(FLAGS.input, pipeline_instance.input_type),
    FLAGS.output_dir)


def console_entry_point():
  tf.app.run(main)


if __name__ == '__main__':
  console_entry_point()
