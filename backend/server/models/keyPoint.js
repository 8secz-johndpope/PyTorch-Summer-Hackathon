const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const keyPointSchema = new Schema(
  {
    score: {
      type: String,
      require: true,
    },
    part: {
      type: String,
      required: true,
    },
    position: {
      x: {
        type: Number,
        required: true,
      },
      y: {
        type: Number,
        required: true,
      },
    },
  },
  { timestamps: true }
);

module.exports = keyPointSchema;
