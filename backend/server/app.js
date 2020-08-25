const path = require("path");
const express = require("express");
const bodyParser = require("body-parser");
const mongoose = require("mongoose");
const multer = require("multer");
const fs = require("fs");

const videoRoutes = require("./routes/video");
const keypointRoutes = require("./routes/keypoint");

//const User = require('./models/user');

// const MONGODB_URI =
//   "mongodb+srv://hackthon:hackthon@cluster0.hrgyr.mongodb.net/pytorch-hackthon?retryWrites=true&w=majority";
const MONGODB_URI = "mongodb://127.0.0.1/pytorch-hackthon";

const app = express();

const fileStorage = multer.diskStorage({
  destination: (req, file, cb) => {
    let path;
    if (req.path.slice(1) === "player") {
      path = `./videos/${req.path.slice(1)}`;
    } else if (req.path.slice(1).substring(0, 13) === "user/original") {
      path = `./videos/user/original`;
    } else if (req.path.slice(1).substring(0, 11) === "user/result") {
      path = `./videos/user/result`;
    }

    path.split("/").map((_, index) => {
      const checkPath = path.substring(
        0,
        path.split("/", index + 2).join("/").length
      );
      if (!fs.existsSync(checkPath)) {
        fs.mkdirSync(checkPath);
      }
    });

    cb(null, path);
  },

  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const fileFilter = (req, file, cb) => {
  if (file.mimetype === "video/mp4" || file.mimetype === "video/quicktime") {
    cb(null, true);
  } else {
    cb(null, false);
  }
};

app.set("json spaces", 2); // json prettier in browser

app.use(
  bodyParser.urlencoded({
    extended: false,
  })
);
app.use(
  "/videos",
  multer({ storage: fileStorage, fileFilter: fileFilter }).single("video")
);
app.use(express.static(path.join(__dirname, "public")));
app.use("/videos", express.static(path.join(__dirname, "videos")));

app.use("/videos", videoRoutes);
app.use("/keypoints", keypointRoutes);

mongoose
  .connect(MONGODB_URI)
  .then((result) => {
    app.listen(3000);
  })
  .catch((err) => {
    console.log(err);
  });
