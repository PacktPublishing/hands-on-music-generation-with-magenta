# Chapter 6 - Data preparation and pipelines

## Ref

- `https://www.reddit.com/r/WeAreTheMusicMakers/comments/3anwu8/the_drum_percussion_midi_archive_800k/`
- `https://www.reddit.com/r/WeAreTheMusicMakers/comments/3ajwe4/the_largest_midi_collection_on_the_internet/`
- https://elitedatascience.com/overfitting-in-machine-learning

## Primers

- primer/jazz-ride.mid https://musescore.com/user/7942286/scores/1906646
- primer/jazz-drum-basic.mid https://musescore.com/user/13700046/scores/4662816

## TODO

### Book

- TODO fix book attention for drumsrnn (not only lookback)
- TODO post youtube devoxx on reddit and fb and website

### Dataset (chapter 6)

- (DONE) 00: extract and save time and output
- 01: extract and save time and output
- 02: extract and save time and output
- 03: extract and save time and output
- 04: extract and save time and output
- 05: extract and save time and output
- 06: extract and save time and output
- 07: extract and save time and output
- 08: extract and save time and output
- 09: extract and save time and output

### Training (chapter 7)

- train / eval drumsrnn techno on full dataset extraction
- train / eval drumsrnn jazz on full dataset extraction
- train / eval melodyrnn jazz on full dataset extraction
- train drumsrnn and musicvae with comparison 

### Output

- chapter_06_example_00.py
    - Number of tracks: 116189, number of tracks in sample: 116189, number of results: 12634 (10.87%)
    - Time:  7197.6346254
- chapter_06_example_04.py
    - Number of tracks: 31034, number of tracks in sample: 31034, number of results: 30730 (99.02%)
    - Time:  1380.3484564
- training: 20:27:55 (step 0) - 20:46:40 (step 1000) - 19 min - total 20000 steps: 6 hours

## Training

```bash
# Jazz drums
cd "D:\Users\Claire\Data\training\drums_rnn"
convert_dir_to_note_sequences --input_dir="D:\Users\Claire\Data\datasets\jazz_dataset\drums\07" --output_file="notesequences.tfrecord" --recursive
drums_rnn_dataset --config="drum_kit" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
drums_rnn_train --config="drum_kit" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/training_drum_tracks.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128,128]" --num_training_steps=20000
drums_rnn_train --config="drum_kit" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/eval_drum_tracks.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128,128]" --num_training_steps=20000 --eval
drums_rnn_generate --config="drum_kit" --run_dir="logdir/run1" --hparams="batch_size=128,rnn_layer_sizes=[256,256,256]" --output_dir="generated" --num_outputs=10 --num_steps=128 --primer_drums="[(36,)]"

# Jazz piano
cd "D:\Users\Claire\Data\training\melody_rnn"
convert_dir_to_note_sequences --input_dir="D:\Users\Claire\Data\datasets\jazz_dataset\piano\08" --output_file="notesequences.tfrecord" --recursive
melody_rnn_create_dataset --config="attention_rnn" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
melody_rnn_train --config="attention_rnn" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/training_melodies.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --num_training_steps=20000
melody_rnn_train --config="attention_rnn" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/eval_melodies.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --eval
melody_rnn_generate --config="attention_rnn" --run_dir="logdir/run1" --output_dir="generated" --num_outputs=10 --num_steps=128 --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --primer_melody="[60]"

# Techno drums
# TODO
```

## Output

```
tensorflow.python.framework.errors_impl.InvalidArgumentError: Restoring from checkpoint failed. This is most likely due to a mismatch between the current graph and the graph from the checkpoint. Please ensure that you have not altered the graph expected based on the checkpoint. Original error:

Assign requires shapes of both tensors to match. lhs shape= [256] rhs shape= [128]
```