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

## TODO

- techno_drums
    - batch_size=64,rnn_layer_sizes=[64,64]
    - batch_size=128,rnn_layer_sizes=[128,128,128]
    - batch_size=128,rnn_layer_sizes=[256,256,256]

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

- check prefix techno_drums_02_run1
- doesn't converge

```bash
convert_dir_to_note_sequences --input_dir="D:\Users\Claire\Data\datasets\jazz_dataset\drums\07" --output_file="notesequences.tfrecord" --recursive
drums_rnn_create_dataset --config="drum_kit" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
CUDA_VISIBLE_DEVICES="0" drums_rnn_train --config="drum_kit" --run_dir="logdir/run1" --sequence_example_file="sequence_examples/training_drum_tracks.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000
CUDA_VISIBLE_DEVICES=""  drums_rnn_train --config="drum_kit" --run_dir="logdir/run1" --sequence_example_file="sequence_examples/eval_drum_tracks.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000 --eval
tensorboard --logdir=logdir
```

#### Run 2

- check prefix techno_drums_02_run2
- converges but slight overfit
- https://stackoverflow.com/questions/47707793/tensorflow-cnn-loss-function-goes-up-and-down-oscilating-in-tensorboard-how-t
    - l2 weight reg: clip_norm?
    - dropout: dropout_keep_prob
- TODO NEXT GENERATE

```bash
convert_dir_to_note_sequences --input_dir="D:\Users\Claire\Data\datasets\jazz_dataset\drums\07" --output_file="notesequences.tfrecord" --recursive
drums_rnn_create_dataset --config="drum_kit" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
CUDA_VISIBLE_DEVICES="0" drums_rnn_train --config="drum_kit" --run_dir="logdir/run2" --sequence_example_file="sequence_examples/training_drum_tracks.tfrecord" --hparams="learning_rate=0.0001,batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000
CUDA_VISIBLE_DEVICES=""  drums_rnn_train --config="drum_kit" --run_dir="logdir/run2" --sequence_example_file="sequence_examples/eval_drum_tracks.tfrecord" --hparams="learning_rate=0.0001,batch_size=128,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000 --eval
tensorboard --logdir=logdir
```

### Jazz Drums 01 (jazz, blues, country)

- jazz_drums_02.zip
- check prefix jazz_drums_01
- doesn't converge

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
- check prefix jazz_drums_02
- TODO NEXT GENERATE

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
- match "Total records: 34" 
- `melody_rnn_train --config="attention_rnn" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/eval_melodies.tfrecord" --hparams="batch_size=34,rnn_layer_sizes=[128,128]" --num_training_steps=20000 --eval`
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

- jazz_piano_03.zip
- run2 (659 outputs)
- Overfitting: too less data

```bash
cd "/home/alex/data/training/jazz_piano_02"
conda activate magenta
convert_dir_to_note_sequences --input_dir="~/data/dataset/jazz_piano_03" --output_file="notesequences.tfrecord" --recursive
melody_rnn_create_dataset --config="attention_rnn" --input="notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
set CUDA_VISIBLE_DEVICES="0"
melody_rnn_train --config="attention_rnn" --run_dir="logdir/run2" --sequence_example_file="sequence_examples/training_melodies.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --num_training_steps=20000
set CUDA_VISIBLE_DEVICES=""
melody_rnn_train --config="attention_rnn" --run_dir="logdir/run2" --sequence_example_file="sequence_examples/eval_melodies.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --num_training_steps=20000 --eval
## Check tensorboard
tensorboard --logdir=logdir
melody_rnn_generate --config="attention_rnn" --run_dir="logdir/run2" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --output_dir="generated" --temperature=1.1
```

### Jazz Piano 04 (jazz, blues, transposed octave)

- jazz_piano_03.zip
- transpose 1 octave up and down: Produced 1973 outputs.
- run3: Overfitting: too less data

### Jazz Piano 05 (jazz, blues, transposed major scale)

- jazz_piano_03.zip
- transpose 1 major up and down: TODO
- TODO run4

### Jazz Piano 06 (jazz, blues, dropout)

- jazz_piano_03.zip
- run5: Overfitting

```bash
cd "/home/alex/data/training/jazz_piano_02"
conda activate magenta
set CUDA_VISIBLE_DEVICES="0"
melody_rnn_train --config="attention_rnn" --run_dir="logdir/run5" --sequence_example_file="sequence_examples/training_melodies.tfrecord" --hparams="dropout_keep_prob=0.3,batch_size=128,rnn_layer_sizes=[128,128]" --num_training_steps=20000
set CUDA_VISIBLE_DEVICES=""
melody_rnn_train --config="attention_rnn" --run_dir="logdir/run5" --sequence_example_file="sequence_examples/eval_melodies.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --num_training_steps=20000 --eval
## Check tensorboard
tensorboard --logdir=logdir
melody_rnn_generate --config="attention_rnn" --run_dir="logdir/run5" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --output_dir="generated" --temperature=1.1
```

### Jazz Piano 07 (jazz, blues, polyphonic true)

- python /home/alex/projects/hands-on-music-generation-with-magenta/Chapter06/melody_rnn_pipeline_example.py --config="attention_rnn" --input="/home/alex/datanew/datasets/jazz_piano/notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10
    - no transposition
    - no repeat
    - ignore_polyphonic_notes=True # ADD to previous chapter with remove transpose?

## Problems

### Cuda error out of memory

- check prefix cuda_error_out_of_memory

### Model diverged with loss NaN

Lower learning rate

- check prefix cuda_error_out_of_memory
- https://stackoverflow.com/questions/40050397/deep-learning-nan-loss-reasons
- https://stackoverflow.com/questions/44103649/model-diverged-with-loss-nan-when-number-of-classes-increases-even-with-sm
- https://github.com/tensorflow/magenta/issues/1202

### Wrong network size

- check prefix wrong_network_size

## Google cloud platform

Recommanded from https://github.com/tensorflow/magenta/tree/master/magenta/models/onsets_frames_transcription: https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python

or

- Login https://console.cloud.google.com
- On the left, Compute Engine
- On the top, create project, "Magenta" 
- On the left menu, "Images", search for "tensorflow" and take most recent, "c3-deeplearning-tf-1-15-cu100-20191112"
    - "Create instance"
    - Take region and zone near you
    - Take N1 series, machine type n1-standard-8
    - In "CPU platform and GPU", use "Add GPU", use NVIDIA Telsa K80
    - ! TODO In Security add your key
    - Disk already chosen 50 GB ok
    - Create new VM from it, 50 GB disk
- On the left, "VM instances"
    - You should see the new VM "magenta"
    - Use "SSH" button, or use your SSH client (login is same as key login)
    - This VM requires Nvidia drivers to function correctly.   Installation takes ~1 minute.
    `Would you like to install the Nvidia driver? [y/n] y`
- Fix cudnn version
    - Download cuDNN v7.6.5 (November 5th, 2019), for CUDA 10.0
        - (easiest way is to download locally and then scp it)
        - `scp cudnn-10.0-linux-x64-v7.6.5.32.tgz alex@35.195.120.211:`
    - Extract `tar -xzvf ...`
        - `sudo cp cuda/include/cudnn.h /usr/local/cuda/include`
        - `sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64`
        - `sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*`
- Reinstall stuff
    `sudo apt install libasound2-dev libsndfile-dev`
    - Then conda install (download, exec)
    - Then `bash`
    - Then `conda create -n magenta python=3.6`
    - Then `conda activate magenta`
    - Then `pip install magenta-gpu`
- Start training
    - `scp jazz_piano.zip alex@35.205.146.121:`
    - `unzip jazz_piano.zip`
    - convert `melody_rnn_create_dataset --config="attention_rnn" --input="../../datasets/jazz_piano/notesequences.tfrecord" --output_dir="sequence_examples" --eval_ratio=0.10`
    - new term training `melody_rnn_train --config="attention_rnn" --run_dir="logdir/run1" --sequence_example_file="sequence_examples/training_melodies.tfrecord" --hparams="batch_size=128,rnn_layer_sizes=[128,128]" --num_training_steps=20000`
    - new term eval `CUDA_VISIBLE_DEVICES="" melody_rnn_train --config="attention_rnn" --run_dir="logdir/run1" --sequence_example_file="sequence_examples/eval_melodies.tfrecord" --hparams="batch_size=62,rnn_layer_sizes=[128,128]" --num_training_steps=20000 --eval`
    - htop / watch nvidia-smi
    - Remote tensorboard `ssh -L 16006:127.0.0.1:6006 alex@35.205.146.121` at http://127.0.0.1:16006
- Finish
    - `scp alex@35.205.146.121:training/melody_rnn_jazz_piano.tar melody_rnn_jazz_piano.tar`
- DONT FORGET TO CLOSE THE VM

### Train

Python 3 fix: 

```
Traceback (most recent call last):
  File "/home/alex/miniconda3/envs/magenta/bin/music_vae_train", line 8, in <module>
    sys.exit(console_entry_point())
  File "/home/alex/miniconda3/envs/magenta/lib/python3.6/site-packages/magenta/models/music_vae/music_vae_train.py", line 342, in console_entry_point
    tf.app.run(main)
  File "/home/alex/miniconda3/envs/magenta/lib/python3.6/site-packages/tensorflow_core/python/platform/app.py", line 40, in run
    _run(main=main, argv=argv, flags_parser=_parse_flags_tolerate_undef)
  File "/home/alex/miniconda3/envs/magenta/lib/python3.6/site-packages/absl/app.py", line 299, in run
    _run_main(main, args)
  File "/home/alex/miniconda3/envs/magenta/lib/python3.6/site-packages/absl/app.py", line 250, in _run_main
    sys.exit(main(argv))
  File "/home/alex/miniconda3/envs/magenta/lib/python3.6/site-packages/magenta/models/music_vae/music_vae_train.py", line 338, in main
    run(configs.CONFIG_MAP)
  File "/home/alex/miniconda3/envs/magenta/lib/python3.6/site-packages/magenta/models/music_vae/music_vae_train.py", line 333, in run
    master=FLAGS.master)
  File "/home/alex/miniconda3/envs/magenta/lib/python3.6/site-packages/magenta/models/music_vae/music_vae_train.py", line 238, in evaluate
    **_get_input_tensors(dataset_fn().take(num_batches), config))
  File "/home/alex/miniconda3/envs/magenta/lib/python3.6/site-packages/magenta/models/music_vae/base_model.py", line 331, in eval
    for n, t in scalars_to_summarize.iteritems():
AttributeError: 'dict' object has no attribute 'iteritems'
```

https://github.com/tensorflow/magenta/issues/1549
