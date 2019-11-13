# Jazz drum extractor

```bash
cd "D:\Users\Claire\Data\training\jazz_drums"
convert_dir_to_note_sequences --input_dir="D:\Users\Claire\Data\datasets\jazz_dataset\drums\07" --output_file="notesequences.tfrecord" --recursive
drums_rnn_create_dataset --config="drum_kit" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
```

```
I1112 17:18:37.259325 10640 pipeline.py:384] Processed 500 inputs so far. Produced 791 outputs.
I1112 17:18:37.259325 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_track_lengths_in_bars:
  [7,8): 1
  [8,10): 1
  [10,20): 4
  [20,30): 10
  [30,40): 48
  [40,50): 1
I1112 17:18:37.261353 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_discarded_too_long: 0
I1112 17:18:37.263377 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_discarded_too_short: 56
I1112 17:18:37.264352 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_truncated: 47
I1112 17:18:37.265327 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_track_lengths_in_bars:
  [7,8): 24
  [8,10): 41
  [10,20): 160
  [20,30): 87
  [30,40): 389
  [40,50): 20
  [50,100): 5
I1112 17:18:37.266377 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_discarded_too_long: 0
I1112 17:18:37.266377 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_discarded_too_short: 1637
I1112 17:18:37.267327 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_truncated: 411
I1112 17:18:37.267327 10640 statistics.py:141] DAGPipeline_RandomPartition_eval_drum_tracks_count: 51
I1112 17:18:37.268326 10640 statistics.py:141] DAGPipeline_RandomPartition_training_drum_tracks_count: 449
I1112 17:19:15.895682 10640 pipeline.py:384] Processed 1000 inputs so far. Produced 1586 outputs.
I1112 17:19:15.895682 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_track_lengths_in_bars:
  [7,8): 2
  [8,10): 6
  [10,20): 13
  [20,30): 17
  [30,40): 97
  [40,50): 4
I1112 17:19:15.895682 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_discarded_too_long: 0
I1112 17:19:15.896682 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_discarded_too_short: 177
I1112 17:19:15.896682 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_truncated: 98
I1112 17:19:15.896682 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_track_lengths_in_bars:
  [7,8): 40
  [8,10): 79
  [10,20): 298
  [20,30): 162
  [30,40): 820
  [40,50): 34
  [50,100): 14
I1112 17:19:15.897654 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_discarded_too_long: 0
I1112 17:19:15.897654 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_discarded_too_short: 2747
I1112 17:19:15.898681 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_truncated: 847
I1112 17:19:15.899741 10640 statistics.py:141] DAGPipeline_RandomPartition_eval_drum_tracks_count: 103
I1112 17:19:15.899741 10640 statistics.py:141] DAGPipeline_RandomPartition_training_drum_tracks_count: 897
I1112 17:19:54.231841 10640 pipeline.py:384] Processed 1500 inputs so far. Produced 2384 outputs.
I1112 17:19:54.231841 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_track_lengths_in_bars:
  [7,8): 3
  [8,10): 12
  [10,20): 27
  [20,30): 25
  [30,40): 143
  [40,50): 4
I1112 17:19:54.234860 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_discarded_too_long: 0
I1112 17:19:54.235852 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_discarded_too_short: 234
I1112 17:19:54.236860 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_truncated: 144
I1112 17:19:54.236860 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_track_lengths_in_bars:
  [7,8): 64
  [8,10): 110
  [10,20): 442
  [20,30): 234
  [30,40): 1250
  [40,50): 54
  [50,100): 16
I1112 17:19:54.238840 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_discarded_too_long: 0
I1112 17:19:54.240837 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_discarded_too_short: 3665
I1112 17:19:54.240837 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_truncated: 1275
I1112 17:19:54.241813 10640 statistics.py:141] DAGPipeline_RandomPartition_eval_drum_tracks_count: 152
I1112 17:19:54.243842 10640 statistics.py:141] DAGPipeline_RandomPartition_training_drum_tracks_count: 1348
I1112 17:20:30.749841 10640 pipeline.py:384] Processed 2000 inputs so far. Produced 3113 outputs.
I1112 17:20:30.749841 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_track_lengths_in_bars:
  [7,8): 5
  [8,10): 13
  [10,20): 38
  [20,30): 32
  [30,40): 180
  [40,50): 6
I1112 17:20:30.753812 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_discarded_too_long: 0
I1112 17:20:30.753812 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_discarded_too_short: 286
I1112 17:20:30.757813 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_truncated: 182
I1112 17:20:30.758813 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_track_lengths_in_bars:
  [7,8): 81
  [8,10): 149
  [10,20): 535
  [20,30): 300
  [30,40): 1679
  [40,50): 76
  [50,100): 19
I1112 17:20:30.763813 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_discarded_too_long: 0
I1112 17:20:30.763813 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_discarded_too_short: 4888
I1112 17:20:30.764813 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_truncated: 1722
I1112 17:20:30.765813 10640 statistics.py:141] DAGPipeline_RandomPartition_eval_drum_tracks_count: 195
I1112 17:20:30.765813 10640 statistics.py:141] DAGPipeline_RandomPartition_training_drum_tracks_count: 1805
I1112 17:21:09.138838 10640 pipeline.py:384] Processed 2500 inputs so far. Produced 3919 outputs.
I1112 17:21:09.138838 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_track_lengths_in_bars:
  [7,8): 8
  [8,10): 14
  [10,20): 54
  [20,30): 37
  [30,40): 225
  [40,50): 8
  [50,100): 1
I1112 17:21:09.141933 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_discarded_too_long: 0
I1112 17:21:09.142837 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_discarded_too_short: 678
I1112 17:21:09.143813 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_truncated: 230
I1112 17:21:09.143813 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_track_lengths_in_bars:
  [7,8): 134
  [8,10): 191
  [10,20): 647
  [20,30): 387
  [30,40): 2084
  [40,50): 103
  [50,100): 26
I1112 17:21:09.144813 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_discarded_too_long: 0
I1112 17:21:09.145813 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_discarded_too_short: 5923
I1112 17:21:09.145813 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_truncated: 2151
I1112 17:21:09.146814 10640 statistics.py:141] DAGPipeline_RandomPartition_eval_drum_tracks_count: 245
I1112 17:21:09.146814 10640 statistics.py:141] DAGPipeline_RandomPartition_training_drum_tracks_count: 2255
I1112 17:21:42.054636 10640 pipeline.py:386]

Completed.

I1112 17:21:42.056665 10640 pipeline.py:388] Processed 2920 inputs total. Produced 4634 outputs.
I1112 17:21:42.058684 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_track_lengths_in_bars:
  [7,8): 11
  [8,10): 22
  [10,20): 76
  [20,30): 47
  [30,40): 257
  [40,50): 14
  [50,100): 2
I1112 17:21:42.060669 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_discarded_too_long: 0
I1112 17:21:42.060669 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_discarded_too_short: 822
I1112 17:21:42.061636 10640 statistics.py:141] DAGPipeline_DrumsExtractor_eval_drum_tracks_truncated: 268
I1112 17:21:42.062636 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_track_lengths_in_bars:
  [7,8): 164
  [8,10): 218
  [10,20): 784
  [20,30): 456
  [30,40): 2437
  [40,50): 117
  [50,100): 29
I1112 17:21:42.063674 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_discarded_too_long: 0
I1112 17:21:42.064636 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_discarded_too_short: 6848
I1112 17:21:42.065665 10640 statistics.py:141] DAGPipeline_DrumsExtractor_training_drum_tracks_truncated: 2495
I1112 17:21:42.068684 10640 statistics.py:141] DAGPipeline_RandomPartition_eval_drum_tracks_count: 289
I1112 17:21:42.068684 10640 statistics.py:141] DAGPipeline_RandomPartition_training_drum_tracks_count: 2631
```