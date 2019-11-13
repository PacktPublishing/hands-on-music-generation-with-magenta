# Out of memory

```bash
drums_rnn_train --config="drum_kit" --run_dir="logdir\run1" --sequence_example_file="sequence_examples/training_drum_tracks.tfrecord" --hparams="batch_size=256,rnn_layer_sizes=[256,256,256]" --num_training_steps=20000
```

```
2019-11-12 17:24:15.355880: E tensorflow/stream_executor/cuda/cuda_driver.cc:890] failed to alloc 8589934592 bytes on host: CUDA_ERROR_OUT_OF_MEMORY: out of memory
2019-11-12 17:24:15.359932: W .\tensorflow/core/common_runtime/gpu/gpu_host_allocator.h:44] could not allocate pinned host memory of size: 8589934592
2019-11-12 17:24:15.417160: E tensorflow/stream_executor/cuda/cuda_driver.cc:890] failed to alloc 7730940928 bytes on host: CUDA_ERROR_OUT_OF_MEMORY: out of memory
2019-11-12 17:24:15.421444: W .\tensorflow/core/common_runtime/gpu/gpu_host_allocator.h:44] could not allocate pinned host memory of size: 7730940928
2019-11-12 17:24:15.473095: E tensorflow/stream_executor/cuda/cuda_driver.cc:890] failed to alloc 6957846528 bytes on host: CUDA_ERROR_OUT_OF_MEMORY: out of memory
2019-11-12 17:24:15.477100: W .\tensorflow/core/common_runtime/gpu/gpu_host_allocator.h:44] could not allocate pinned host memory of size: 6957846528
2019-11-12 17:24:17.029468: W tensorflow/core/common_runtime/bfc_allocator.cc:237] Allocator (GPU_0_bfc) ran out of memory trying to allocate 1.07GiB with freed_by_count=0. The caller indicates that this is not a failure, but may mean that there could be performance gains if more memory were available.
2019-11-12 17:24:17.037476: W tensorflow/core/common_runtime/bfc_allocator.cc:237] Allocator (GPU_0_bfc) ran out of memory trying to allocate 1.07GiB with freed_by_count=0. The caller indicates that this is not a failure, but may mean that there could be performance gains if more memory were available.
2019-11-12 17:24:17.050700: W tensorflow/core/common_runtime/bfc_allocator.cc:237] Allocator (GPU_0_bfc) ran out of memory trying to allocate 1.06GiB with freed_by_count=0. The caller indicates that this is not a failure, but may mean that there could be performance gains if more memory were available.
2019-11-12 17:24:17.057641: W tensorflow/core/common_runtime/bfc_allocator.cc:237] Allocator (GPU_0_bfc) ran out of memory trying to allocate 1.06GiB with freed_by_count=0. The caller indicates that this is not a failure, but may mean that there could be performance gains if more memory were available.
I1112 17:24:19.894078  1268 basic_session_run_hooks.py:262] Accuracy = 0.00060747896, Global Step = 0, Loss = 6.2650876, Perplexity = 525.8877
```