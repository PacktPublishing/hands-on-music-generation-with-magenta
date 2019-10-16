
import os
import numpy as np
import matplotlib.pyplot as plt
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen
from IPython.display import Audio


def unused():
    # from https://www.freesound.org/people/MustardPlug/sounds/395058/
    fname = '395058__mustardplug__breakbeat-hiphop-a4-4bar-96bpm.wav'
    sr = 16000
    audio = utils.load_audio(fname, sample_length=40000, sr=sr)
    sample_length = audio.shape[0]
    print('{} samples, {} seconds'.format(sample_length, sample_length / float(sr)))


    encoding = fastgen.encode(audio, 'model.ckpt-200000', sample_length)
    print(encoding.shape)

    np.save(fname + '.npy', encoding)

    fig, axs = plt.subplots(2, 1, figsize=(10, 5))
    axs[0].plot(audio);
    axs[0].set_title('Audio Signal')
    axs[1].plot(encoding[0]);
    axs[1].set_title('NSynth Encoding')

    fastgen.synthesize(encoding, save_paths=['gen_' + fname], samples_per_save=sample_length)

    sr = 16000
    synthesis = utils.load_audio('gen_' + fname, sample_length=sample_length, sr=sr)

    def load_encoding(fname, sample_length=None, sr=16000, ckpt='model.ckpt-200000'):
        audio = utils.load_audio(fname, sample_length=sample_length, sr=sr)
        encoding = fastgen.encode(audio, ckpt, sample_length)
        return audio, encoding

    # from https://www.freesound.org/people/maurolupo/sounds/213259/
    fname = '213259__maurolupo__girl-sings-laa.wav'
    sample_length = 32000
    audio, encoding = load_encoding(fname, sample_length)
    fastgen.synthesize(
        encoding,
        save_paths=['gen_' + fname],
        samples_per_save=sample_length)
    synthesis = utils.load_audio('gen_' + fname,
                                 sample_length=sample_length,
                                 sr=sr)

    # use image interpolation to stretch the encoding: (pip install scikit-image)
    from skimage.transform import resize

    def timestretch(encodings, factor):
        min_encoding, max_encoding = encoding.min(), encoding.max()
        encodings_norm = (encodings - min_encoding) / (max_encoding - min_encoding)
        timestretches = []
        for encoding_i in encodings_norm:
            stretched = resize(encoding_i, (int(encoding_i.shape[0] * factor), encoding_i.shape[1]), mode='reflect')
            stretched = (stretched * (max_encoding - min_encoding)) + min_encoding
            timestretches.append(stretched)
        return np.array(timestretches)

    # from https://www.freesound.org/people/MustardPlug/sounds/395058/
    fname = '395058__mustardplug__breakbeat-hiphop-a4-4bar-96bpm.wav'
    sample_length = 40000
    audio, encoding = load_encoding(fname, sample_length)

    audio = utils.load_audio('gen_slower_' + fname, sample_length=None, sr=sr)
    Audio(audio, rate=sr)

    encoding_slower = timestretch(encoding, 1.5)
    encoding_faster = timestretch(encoding, 0.5)

    fig, axs = plt.subplots(3, 1, figsize=(10, 7), sharex=True, sharey=True)
    axs[0].plot(encoding[0]);
    axs[0].set_title('Encoding (Normal Speed)')
    axs[1].plot(encoding_faster[0]);
    axs[1].set_title('Encoding (Faster))')
    axs[2].plot(encoding_slower[0]);
    axs[2].set_title('Encoding (Slower)')


    fastgen.synthesize(encoding_faster, save_paths=['gen_faster_' + fname])
    fastgen.synthesize(encoding_slower, save_paths=['gen_slower_' + fname])

    sample_length = 80000

    # from https://www.freesound.org/people/MustardPlug/sounds/395058/
    aud1, enc1 = load_encoding('395058__mustardplug__breakbeat-hiphop-a4-4bar-96bpm.wav', sample_length)

    # from https://www.freesound.org/people/xserra/sounds/176098/
    aud2, enc2 = load_encoding('176098__xserra__cello-cant-dels-ocells.wav', sample_length)

    enc_mix = (enc1 + enc2) / 2.0

    fig, axs = plt.subplots(3, 1, figsize=(10, 7))
    axs[0].plot(enc1[0]);
    axs[0].set_title('Encoding 1')
    axs[1].plot(enc2[0]);
    axs[1].set_title('Encoding 2')
    axs[2].plot(enc_mix[0]);
    axs[2].set_title('Average')

    fastgen.synthesize(enc_mix, save_paths='mix.wav')

    def fade(encoding, mode='in'):
        length = encoding.shape[1]
        fadein = (0.5 * (1.0 - np.cos(3.1415 * np.arange(length) /
                                      float(length)))).reshape(1, -1, 1)
        if mode == 'in':
            return fadein * encoding
        else:
            return (1.0 - fadein) * encoding

    fig, axs = plt.subplots(3, 1, figsize=(10, 7))
    axs[0].plot(enc1[0]);
    axs[0].set_title('Original Encoding')
    axs[1].plot(fade(enc1, 'in')[0]);
    axs[1].set_title('Fade In')
    axs[2].plot(fade(enc1, 'out')[0]);
    axs[2].set_title('Fade Out')

    def crossfade(encoding1, encoding2):
        return fade(encoding1, 'out') + fade(encoding2, 'in')


    fig, axs = plt.subplots(3, 1, figsize=(10, 7))
    axs[0].plot(enc1[0]);
    axs[0].set_title('Encoding 1')
    axs[1].plot(enc2[0]);
    axs[1].set_title('Encoding 2')
    axs[2].plot(crossfade(enc1, enc2)[0]);
    axs[2].set_title('Crossfade')

    fastgen.synthesize(crossfade(enc1, enc2), save_paths=['crossfade.wav'])
