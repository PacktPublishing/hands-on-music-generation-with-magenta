importScripts("https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@1.4.0/dist/tf.min.js");
importScripts("https://cdn.jsdelivr.net/npm/@magenta/music@^1.12.0/es6/core.js");
importScripts("https://cdn.jsdelivr.net/npm/@magenta/music@^1.12.0/es6/music_vae.js");
importScripts("https://cdn.jsdelivr.net/npm/@magenta/music@^1.12.0/es6/gansynth.js");

// Starts the MusicVAE model and initializes it. When finished, enables
// the button to start the sampling
async function startMusicVae() {
  const musicvae = new music_vae.MusicVAE("https://storage.googleapis.com/" +
      "magentadata/js/checkpoints/music_vae/trio_4bar");
  await musicvae.initialize();
  window.musicvae = musicvae;
  buttonSampleMusicVaeTrio.disabled = false;
}

// Starts the GANSynth model and initializes it
async function startGanSynth() {
  const ganSynth = new gansynth.GANSynth("https://storage.googleapis.com/" +
      "magentadata/js/checkpoints/gansynth/acoustic_only");
  await ganSynth.initialize();
  window.ganSynth = ganSynth
}

// Plots the spectrogram of the given channel
// see music/demos/gansynth.ts:28 in magenta.js source code
async function plotSpectra(spectra, channel) {
  const spectraPlot = tf.tidy(() => {
    // Slice a single example.
    let spectraPlot = tf.slice(spectra, [0, 0, 0, channel], [1, -1, -1, 1])
        .reshape([128, 1024]);
    // Scale to [0, 1].
    spectraPlot = tf.sub(spectraPlot, tf.min(spectraPlot));
    spectraPlot = tf.div(spectraPlot, tf.max(spectraPlot));
    return spectraPlot;
  });
  // Plot on canvas.
  const canvas = document.createElement("canvas");
  containerPlots.appendChild(canvas);
  await tf.browser.toPixels(spectraPlot, canvas);
  spectraPlot.dispose();
}

// Samples a trio of drum kit, bass and lead from MusicVAE and
// plays it repeatedly at 120 QPM
async function sampleMusicVaeTrio() {
  const samples = await window.musicvae.sample(1);
  const sample = samples[0];
  new mm.PianoRollCanvasVisualizer(sample, canvasMusicVaePlot,
      {"pixelsPerTimeStep": 50});

  const player = new Player();
  mm.Player.tone.Transport.loop = true;
  mm.Player.tone.Transport.loopStart = 0;
  mm.Player.tone.Transport.loopEnd = 8;
  player.start(sample, 120);
  window.player = player;
}

// Samples a single note of 4 seconds from GANSynth and plays it repeatedly
async function sampleGanNote() {
  const lengthInSeconds = 4.0;
  const sampleRate = 16000;
  const length = lengthInSeconds * sampleRate;

  // The sampling returns a spectrogram, convert that to audio in
  // a tone.js buffer
  const specgrams = await ganSynth.randomSample(60);
  const audio = await ganSynth.specgramsToAudio(specgrams);
  const audioBuffer = mm.Player.tone.context.createBuffer(
      1, length, sampleRate);
  audioBuffer.copyToChannel(audio, 0, 0);

  // Plays the sample using tone.js by using C4 as a base note,
  // since this is what we asked the model for (MIDI pitch 60).
  // If the sequence contains other notes, the pitch will be
  // changed automatically
  const volume = new mm.Player.tone.Volume(-10);
  const instrument = new mm.Player.tone.Sampler({"C4": audioBuffer});
  instrument.chain(volume, mm.Player.tone.Master);
  window.player.leadSynth = instrument;

  // Plots the resulting spectrograms
  await plotSpectra(specgrams, 0);
  await plotSpectra(specgrams, 1);
}


// Calls the initialization of MusicVAE and GanSynth
try {
  Promise.all([startMusicVae(), startGanSynth()]);
} catch (error) {
  console.error(error);
}
