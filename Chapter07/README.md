# Chapter 7 - Training an existing model on a specific style

## Ref

- https://elitedatascience.com/overfitting-in-machine-learning
- https://devblogs.nvidia.com/cuda-pro-tip-control-gpu-visibility-cuda_visible_devices/
- https://stackoverflow.com/questions/44796793/difference-between-tf-clip-by-value-and-tf-clip-by-global-norm-for-rnns-and-how
    - tf.clip_by_norm rescales one tensor if necessary, so that its L2 norm does not exceed a certain threshold. It's useful typically to avoid exploding gradient on one tensor, because you keep the gradient direction. For instance:
    - https://www.tensorflow.org/api_docs/python/tf/clip_by_norm

## TODO

- train / eval drumsrnn techno on full dataset extraction
- train / eval drumsrnn jazz on full dataset extraction
- train / eval melodyrnn jazz on full dataset extraction
- train drumsrnn and musicvae with comparison 

## Training

### TODO

Do increasingly better training using the rundir 

- TODO make recommandations on data and training org 
- TODO (run1) first with little data (100 samples)
- TODO (run2) then with more data (500 samples, small network 64)
- TODO (run3) try to reproduce the model diverged using drums rnn (using 128)
- TODO (run4) fix it using learning rate
- TODO (run5) fix it then using bigger network
- TODO (run6) add lots of data (1000 samples)

### Techno Drums 02 (90 threshold)

#### Run 1

- [Jazz techno drums 02 run 1 eval (17/11/2019)](docs/techno_drums_02_run1_eval.txt)
- [Jazz techno drums 02 run 2 train (17/11/2019)](docs/techno_drums_02_run1_train.txt)

```bash
convert_dir_to_note_sequences --input_dir="D:\Users\Claire\Data\datasets\jazz_dataset\drums\07" --output_file="notesequences.tfrecord" --recursive
drums_rnn_create_dataset --config="drum_kit" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
CUDA_VISIBLE_DEVICES="0" drums_rnn_train --config="drum_kit" --run_dir="logdir/run1" --sequence_example_file="sequence_examples/training_drum_tracks.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000
CUDA_VISIBLE_DEVICES=""  drums_rnn_train --config="drum_kit" --run_dir="logdir/run1" --sequence_example_file="sequence_examples/eval_drum_tracks.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000 --eval
tensorboard --logdir=logdir
```

#### Run 2

- [Jazz techno drums 02 run 2eval (17/11/2019)](docs/techno_drums_02_run1_eval.txt)
- [Jazz techno drums 02 run 2train (17/11/2019)](docs/techno_drums_02_run1_train.txt)
- https://stackoverflow.com/questions/47707793/tensorflow-cnn-loss-function-goes-up-and-down-oscilating-in-tensorboard-how-t
    - l2 weight reg: clip_norm?
    - dropout: dropout_keep_prob

```bash
convert_dir_to_note_sequences --input_dir="D:\Users\Claire\Data\datasets\jazz_dataset\drums\07" --output_file="notesequences.tfrecord" --recursive
drums_rnn_create_dataset --config="drum_kit" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
CUDA_VISIBLE_DEVICES="0" drums_rnn_train --config="drum_kit" --run_dir="logdir/run2" --sequence_example_file="sequence_examples/training_drum_tracks.tfrecord" --hparams="learning_rate=0.0001,batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000
CUDA_VISIBLE_DEVICES=""  drums_rnn_train --config="drum_kit" --run_dir="logdir/run2" --sequence_example_file="sequence_examples/eval_drum_tracks.tfrecord" --hparams="learning_rate=0.0001,batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000 --eval
tensorboard --logdir=logdir
```

### Jazz Drums 01 (jazz, blues, country)

TODO model diverged with loss NaN

- jazz_drums_02.zip
- [Jazz drums 01 training (12/11/2019)](./docs/jazz_drums_01.txt)

```bash
drums_rnn_train --config="drum_kit" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/training_drum_tracks.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128,128]" --num_training_steps=20000
```

Try fix it with:

```bash
cd "D:\Users\Claire\Data\training\jazz_drums_02"
conda activate dreambank2
convert_dir_to_note_sequences --input_dir="D:\Users\Claire\Data\datasets\jazz_dataset\drums\07" --output_file="notesequences.tfrecord" --recursive
drums_rnn_create_dataset --config="drum_kit" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
set CUDA_VISIBLE_DEVICES="0"
drums_rnn_train --config="drum_kit" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/training_drum_tracks.tfrecord" --hparams="learning_rate=0.0001,batch_size=128,rnn_layer_sizes=[128,128,128]" --num_training_steps=20000
set CUDA_VISIBLE_DEVICES=""
drums_rnn_train --config="drum_kit" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/eval_drum_tracks.tfrecord" --hparams="learning_rate=0.0001,batch_size=128,rnn_layer_sizes=[128,128,128]" --num_training_steps=20000 --eval
## Check tensorboard
tensorboard --logdir=logdir
```

### Jazz Drums 02 (jazz, blues, country)

- jazz_drums_02.zip
- [Jazz drums 02 training (13/11/2019)](docs/jazz_drums_02_train.txt)
- [Jazz drums 02 eval (13/11/2019)](./docs/jazz_drums_02_eval.txt)

```bash
cd "D:\Users\Claire\Data\training\jazz_drums_02"
conda activate dreambank2
convert_dir_to_note_sequences --input_dir="D:\Users\Claire\Data\datasets\jazz_dataset\drums\07" --output_file="notesequences.tfrecord" --recursive
drums_rnn_create_dataset --config="drum_kit" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
set CUDA_VISIBLE_DEVICES="0"
drums_rnn_train --config="drum_kit" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/training_drum_tracks.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000
set CUDA_VISIBLE_DEVICES=""
drums_rnn_train --config="drum_kit" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/eval_drum_tracks.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000 --eval
## Check tensorboard
tensorboard --logdir=logdir
drums_rnn_generate --config="drum_kit" --run_dir="logdir\run1" --hparams="batch_size=128,rnn_layer_sizes=[256,256,256]" --output_dir="generated" --temperature=1.1
```

### Jazz Drums 03 (jazz)

TODO 

### Jazz Drums 04 (jazz, blues)

TODO 

### Jazz Piano 01 (jazz, blues, country)

TODO 

### Jazz Piano 02 (jazz)

- jazz_piano_02.zip
- [Jazz piano 02 data (13/11/2019)](./docs/jazz_piano_02_data.txt) 
- [Jazz piano 02 eval error (13/11/2019)](./docs/jazz_piano_02_eval_error.txt)
    - match "Total records: 34" 
    - `melody_rnn_train --config="attention_rnn" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/eval_melodies.tfrecord" --hparams="batch_size=34,rnn_layer_sizes=[128,128]" --num_training_steps=20000 --eval`
- [Jazz piano 02 eval (13/11/2019)](./docs/jazz_piano_02_eval.txt)
- [Jazz piano 02 traning (13/11/2019)](docs/jazz_piano_02_train.txt)
- Overfitting: too less data
- Trained on CPU (error starting cuda)

```bash
cd "D:\Users\Claire\Data\training\jazz_piano_02"
conda activate dreambank2
convert_dir_to_note_sequences --input_dir="D:\Users\Claire\Data\datasets\jazz_dataset\piano\08-jazz" --output_file="notesequences.tfrecord" --recursive
melody_rnn_create_dataset --config="attention_rnn" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
set CUDA_VISIBLE_DEVICES="0"
melody_rnn_train --config="attention_rnn" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/training_melodies.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --num_training_steps=20000
set CUDA_VISIBLE_DEVICES=""
melody_rnn_train --config="attention_rnn" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/eval_melodies.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --num_training_steps=20000 --eval
## Check tensorboard
tensorboard --logdir=logdir
melody_rnn_generate --config="attention_rnn" --run_dir="logdir\run1" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --output_dir="generated" --temperature=1.1
```

### Jazz Piano 03 (jazz, blues)


### Training global

```bash
# Jazz drums
## Create dataset
cd "D:\Users\Claire\Data\training\jazz_drums"
conda activate dreambank2
convert_dir_to_note_sequences --input_dir="D:\Users\Claire\Data\datasets\jazz_dataset\drums\07" --output_file="notesequences.tfrecord" --recursive
drums_rnn_create_dataset --config="drum_kit" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
## Train (windows)
set CUDA_VISIBLE_DEVICES="0"
drums_rnn_train --config="drum_kit" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/training_drum_tracks.tfrecord" --hparams="learning_rate=0.0001,batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000
set CUDA_VISIBLE_DEVICES=""
drums_rnn_train --config="drum_kit" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/eval_drum_tracks.tfrecord" --hparams="learning_rate=0.0001,batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000 --eval
## Train (unix)
CUDA_VISIBLE_DEVICES="0" drums_rnn_train --config="drum_kit" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/training_drum_tracks.tfrecord" --hparams="learning_rate=0.0001,batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000
CUDA_VISIBLE_DEVICES=""  drums_rnn_train --config="drum_kit" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/eval_drum_tracks.tfrecord" --hparams="learning_rate=0.0001,batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000 --eval
## Check tensorboard
tensorboard --logdir=logdir
## Generate
drums_rnn_generate --config="drum_kit" --run_dir="logdir\run1" --hparams="batch_size=128,rnn_layer_sizes=[256,256,256]" --output_dir="generated" --num_outputs=10 --num_steps=128 --primer_drums="[(36,)]"

# Jazz piano
cd "D:\Users\Claire\Data\training\melody_rnn"
convert_dir_to_note_sequences --input_dir="D:\Users\Claire\Data\datasets\jazz_dataset\piano\08" --output_file="notesequences.tfrecord" --recursive
melody_rnn_create_dataset --config="attention_rnn" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
melody_rnn_train --config="attention_rnn" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/training_melodies.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --num_training_steps=20000
melody_rnn_train --config="attention_rnn" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/eval_melodies.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --eval
melody_rnn_generate --config="attention_rnn" --run_dir="logdir\run1" --output_dir="generated" --num_outputs=10 --num_steps=128 --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --primer_melody="[60]"

# Techno drums
# TODO
```

## Problems

### [Cuda error out of memory](./docs/cuda_error_out_of_memory.md)

TODO

### [Model diverged with loss NaN](./docs/model_diverged_with_loss_nan.md)

Lower learning rate

- https://stackoverflow.com/questions/40050397/deep-learning-nan-loss-reasons
- https://stackoverflow.com/questions/44103649/model-diverged-with-loss-nan-when-number-of-classes-increases-even-with-sm
- https://github.com/tensorflow/magenta/issues/1202

### [Wrong network size](./docs/wrong_network_size.md)

TODO

## Google cloud platform

Recommanded from https://github.com/tensorflow/magenta/tree/master/magenta/models/onsets_frames_transcription: https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python

or

- Go to images, seach for "tensorflow" and take most recent, "c3-deeplearning-tf-1-15-cu100-20191112"
- Create new VM from it, 50 GB disk
- Login ssh
    - This VM requires Nvidia drivers to function correctly.   Installation takes ~1 minute.
    Would you like to install the Nvidia driver? [y/n] y
- Then conda install
    - then `bash`
- ? Install tensorflow-gpu using `pip install /opt/deeplearning/binaries/tensorflow/tensorflow_gpu-1.15.0-cp36-cp36m-linux_x86_64.whl`
- `fatal error: alsa/asoundlib.h: No such file or directory`
    - maybe install `sudo apt install libasound2-dev`
- `OSError: sndfile library not found`
    - `sudo apt install libsndfile-dev` 
- test
    - `wget http://download.magenta.tensorflow.org/models/drum_kit_rnn.mag`
    - `drums_rnn_generate --config="drum_kit" --bundle_file="drum_kit_rnn.mag"`
- save images for book?
