# Chapter 7 - Training an existing model on a specific style

## Ref

- https://elitedatascience.com/overfitting-in-machine-learning
- https://devblogs.nvidia.com/cuda-pro-tip-control-gpu-visibility-cuda_visible_devices/

## TODO

- train / eval drumsrnn techno on full dataset extraction
- train / eval drumsrnn jazz on full dataset extraction
- train / eval melodyrnn jazz on full dataset extraction
- train drumsrnn and musicvae with comparison 

## Training

### Jazz Drums 01

TODO model diverged with loss NaN

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
```

### Jazz Drums 02

- [Jazz drums 02 training (13/11/2019)](./docs/jazz_drums_02_training.txt)
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
```

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

### Output

- [Jazz drums 01 (13/11/2019)](./docs/jazz_drums_02_eval.txt)

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
