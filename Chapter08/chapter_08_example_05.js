importScripts("https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@1.4.0/dist/tf.min.js");
importScripts("https://cdn.jsdelivr.net/npm/@magenta/music@^1.12.0/es6/core.js");
importScripts("https://cdn.jsdelivr.net/npm/@magenta/music@^1.12.0/es6/music_vae.js");

async function initialize() {
  musicvae = new music_vae.MusicVAE("https://storage.googleapis.com/" +
      "magentadata/js/checkpoints/music_vae/trio_4bar");
  await musicvae.initialize();
  postMessage(["initialized"]);
}

onmessage = function (event) {
  Promise.all([musicvae.sample(1)])
      .then(samples => postMessage(["sample", samples[0]]));
};

try {
  Promise.all([initialize()]);
} catch (error) {
  console.error(error);
}
