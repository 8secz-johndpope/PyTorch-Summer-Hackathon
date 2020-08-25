const mongoose = require("mongoose");
const KeyPoints = require("./keyPoints");

const Schema = mongoose.Schema;

const userVideoSchema = new Schema(
  {
    originalName: {
      type: String,
      require: true,
    },
    resultName: {
      type: String,
      require: true,
    },
    userId: {
      type: String,
      required: true,
    },
    status: {
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

module.exports = mongoose.model("UserVideo", userVideoSchema);
