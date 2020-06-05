# Chapter 6 - Data preparation for training

[![Magenta Version 1.1.7](../docs/magenta-v1.1.7-badge.svg)](https://github.com/magenta/magenta/releases/tag/1.1.7)

This chapter will show how training our own models is crucial since it allows us to generate music in a specific style, generate specific structures or instruments. Building and preparing a dataset is the first step before training our own model. To do that, we first look at existing datasets and APIs to help us find meaningful data. Then, we build two datasets in MIDI for specific styles—dance and jazz. Finally, we prepare the MIDI files for training using data transformations and pipelines.

## Utils

There are some utilities for processing the Lakh MIDI Dataset (LMD) in the [lakh_utils.py](./lakh_utils.py) file and utilities for multiprocessing in the [multiprocessing_utils.py](./multiprocessing_utils.py) file with example usage.

There is a custom pipeline example for the Melody RNN model in the [melody_rnn_pipeline_example.py](./melody_rnn_pipeline_example.py) file. Change directory to the folder containing the Tensorflow records of NoteSequence and call the pipeline using:

```bash
python /path/to/the/pipeline/melody_rnn_pipeline_example.py --config="attention_rnn" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
``` 

## Code

Before you start, follow the [installation instructions for Magenta 1.1.7](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta/tree/master/Chapter01#installing-magenta).

### [Example 0](chapter_06_example_00.py)

Extract techno (four on the floor) drum rhythms.

```bash
python chapter_06_example_00.py --sample_size=1000 --pool_size=4 --path_dataset_dir=PATH_DATASET --path_output_dir=PATH_OUTPUT --bass_drums_on_beat_threshold=0.75 
```

### [Example 1](chapter_06_example_01.py)

Artist extraction using LAKHs dataset matched with the MSD dataset.

```bash
python chapter_06_example_01.py --sample_size=1000 --pool_size=4 --path_dataset_dir=PATH_DATASET --path_match_scores_file=PATH_MATCH_SCORES
```

### [Example 2](chapter_06_example_02.py)

Lists most common genres from the Last.fm API using the LAKHs dataset matched with the MSD dataset.

```bash
python chapter_06_example_02.py --sample_size=1000 --pool_size=4 --path_dataset_dir=PATH_DATASET --path_match_scores_file=PATH_MATCH_SCORES --last_fm_api_key=LAST_FM_API_KEY
```

### [Example 3](chapter_06_example_03.py)

Filter on specific tags from the Last.fm API using the LAKHs dataset matched with the MSD dataset.

```bash
python chapter_06_example_03.py --sample_size=1000 --pool_size=4 --path_dataset_dir=PATH_DATASET --path_match_scores_file=PATH_MATCH_SCORES --last_fm_api_key=LAST_FM_API_KEY --tags="['jazz', 'blues']"
```

### [Example 4](chapter_06_example_04.py)

Get statistics on instrument classes from the MIDI files.

```bash
python chapter_06_example_04.py --sample_size=1000 --pool_size=4 --path_dataset_dir=PATH_DATASET --path_match_scores_file=PATH_MATCH_SCORES
```

### [Example 5](chapter_06_example_05.py)

Extract drums MIDI files. Some drum tracks are split into multiple separate drum instruments, in which case we try to merge them into a single instrument and save only 1 MIDI file.

```bash
python chapter_06_example_05.py --sample_size=1000 --pool_size=4 --path_dataset_dir=PATH_DATASET --path_match_scores_file=PATH_MATCH_SCORES --path_output_dir=PATH_OUTPUT
```

### [Example 6](chapter_06_example_06.py)

Extract piano MIDI files. Some piano tracks are split into multiple separate piano instruments, in which case we keep them split and merge them into multiple MIDI files.

```bash
python chapter_06_example_06.py --sample_size=1000 --pool_size=4 --path_dataset_dir=PATH_DATASET --path_match_scores_file=PATH_MATCH_SCORES --path_output_dir=PATH_OUTPUT
```

### [Example 7](chapter_06_example_07.py)

Extract drums MIDI files corresponding to specific tags.

```bash
python chapter_06_example_07.py --sample_size=1000 --pool_size=4 --path_dataset_dir=PATH_DATASET --path_match_scores_file=PATH_MATCH_SCORES --path_output_dir=PATH_OUTPUT --last_fm_api_key=LAST_FM_API_KEY --tags="['jazz', 'blues']"
```

### [Example 8](chapter_06_example_08.py)

Extract piano MIDI files corresponding to specific tags.

```bash
python chapter_06_example_08.py --sample_size=1000 --pool_size=4 --path_dataset_dir=PATH_DATASET --path_match_scores_file=PATH_MATCH_SCORES --path_output_dir=PATH_OUTPUT --last_fm_api_key=LAST_FM_API_KEY --tags="['jazz', 'blues']"
```

### [Example 9](chapter_06_example_09.py)

Extract drums tracks from GMD.

```bash
python chapter_06_example_09.py --sample_size=1000 --pool_size=4 --path_dataset_dir=PATH_DATASET --path_output_dir=PATH_OUTPUT
```
