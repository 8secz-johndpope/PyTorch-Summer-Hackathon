const mongoose = require('mongoose');
const KeyPoint = require('./keyPoint');

const Schema = mongoose.Schema;

const keyPointsSchema = new Schema(
  {
    score: {
      type: String,
      require: true,
    },
    keypoints: {
      type: [KeyPoint],
      required: false,
    },
  },
  { timestamps: true }
);

module.exports = keyPointsSchema;
