// TODO doesn't work
const music_rnn = require("@magenta/music/node/music_rnn");
const core = require("@magenta/music/node/core");

// These hacks below are needed because the library uses performance and fetch which
// exist in browsers but not in node. We are working on simplifying this!
const globalAny = global;
globalAny.performance = Date;
globalAny.fetch = require("node-fetch");

const EMPTY_NOTE_SEQUENCE = {
    ticksPerQuarter: 220,
    totalTime: 0,
    timeSignatures: [{time: 0, numerator: 4, denominator: 4}],
    tempos: [{time: 0, qpm: 120}],
    notes: []
};

const model = new music_rnn.MusicRNN(
    "https://storage.googleapis.com/magentadata/js/checkpoints/" +
    "music_rnn/basic_rnn");
model
    .initialize()
    .then(() => {
        const emptyQuant = core.sequences.quantizeNoteSequence(
            EMPTY_NOTE_SEQUENCE, 4);
        model.continueSequence(emptyQuant, 64);
    })
    .then((sequence) => {
        console.log(sequence)
    });
