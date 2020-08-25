const mongoose = require('mongoose');
const KeyPoints = require('./keyPoints');

const Schema = mongoose.Schema;

const playerVideoSchema = new Schema(
  {
    name: {
      type: String,
      require: true,
    },
    playerName: {
      type: String,
      required: true,
    },
    keypointArray: {
      type: [KeyPoints],
      required: true,
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model('PlayerVideo', playerVideoSchema);
