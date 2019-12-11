const music_vae = require("@magenta/music/node/music_vae");

// These hacks below are needed because the library uses performance and fetch which
// exist in browsers but not in node. We are working on simplifying this!
const globalAny = global;
globalAny.performance = Date;
globalAny.fetch = require("node-fetch");

const model = new music_vae.MusicVAE(
    "https://storage.googleapis.com/magentadata/js/checkpoints/" +
    "music_vae/drums_2bar_lokl_small");
model
    .initialize()
    .then(() => model.sample(1))
    .then(samples => {
        console.log(samples[0])
    });
