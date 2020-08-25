const async = require("async");
const path = require("path");
const fs = require("fs");
const archiver = require("archiver");
const { spawn } = require("child_process");

const PlayerVideo = require("../models/playerVideo");
const UserVideo = require("../models/userVideo");

exports.getVideos = (req, res, next) => {
  res.header("Content-Type", "application/json");
  res.json({
    getUserOriginalVideoByName: {
      url: "https://<domain_name>/videos/user/original/<video_name>",
      returnName: "video_name.mp4",
      returnType: "mp4",
    },
    getUserResultVideoByName: {
      url: "https://<domain_name>/videos/user/result/<video_name>",
      returnName: "video_name.mp4",
      returnType: "mp4",
    },
    getPlayerVideoByName: {
      url: "https://<domain_name>/videos/player/<video_name>",
      returnName: "video_name.mp4",
      returnType: "mp4",
    },
    getPlayerVideos: {
      url: "https://<domain_name>/videos/player",
      returnName: "playerVideos.zip",
      returnType: "zip",
    },
    getVideoStatusByName: {
      url: "https://<domain_name>/videos/status/<video_name>",
      returnFormat: { status: "Pending / Finished" },
      returnType: "json",
    },
    postUserOriginalVideo: {
      url: "https://<domain_name>/videos/user/original",
      form: {
        video: "<video_file>",
        userId: "<user_id>",
      },
      contentType: "multipart/form-data",
    },
    postUserResultVideo: {
      url: "https://<domain_name>/videos/user/result",
      form: {
        video: "<video_file>",
        originalName: "<original_video_name>",
        keypointArray: "<keypoint_array>",
      },
      contentType: "multipart/form-data",
    },
    postPlayerVideo: {
      url: "https://<domain_name>/videos/player",
      form: {
        video: "<video_file>",
        playerName: "<player_name>",
        keypointArray: "<keypoint_array>",
      },
      contentType: "multipart/form-data",
    },
    keypointArraySchema: [
      {
        score: "number",
        keypoints: [
          {
            score: "number",
            part: "string",
            position: { x: "number", y: "number" },
          },
        ],
      },
    ],
  });
};

exports.getPlayerVideos = (req, res, next) => {
  const dirPath = path.join(__dirname, "../videos", "player");

  try {
    if (!fs.existsSync(path.join(__dirname, "../zip"))) {
      fs.mkdirSync(path.join(__dirname, "../zip"));
    }
  } catch (err) {
    res.json({ error: "server error" });
  }

  fs.readdir(dirPath, (err, filesPath) => {
    if (err) {
      res.json({ error: "no player videos to return" });
      console.log(err);
    }

    filesPath = filesPath.map((filePath) => path.join(dirPath, filePath));

    const output = fs.createWriteStream(
      path.join(__dirname, "../zip/playerVideo.zip")
    );

    const archive = archiver("zip", {
      gzip: true,
      zlib: { level: 9 }, // Sets the compression level.
    });
    archive.on("error", (err) => {
      res.json({ error: err });
    });
    archive.pipe(output);

    async.map(
      filesPath,
      (filePath, cb) => {
        let fileName;
        if (filePath.split("/")[0] !== filePath)
          fileName = filePath.split("/")[filePath.split("/").length - 1];
        if (filePath.split("\\")[0] !== filePath)
          fileName = filePath.split("\\")[filePath.split("\\").length - 1];

        archive.file(filePath, {
          name: fileName,
        });

        cb();
      },
      async (err, results) => {
        if (err) res.json({ error: err });

        await archive.finalize();

        const file = fs.createReadStream(
          path.join(__dirname, "../zip/playerVideo.zip")
        );
        res.set({
          "Content-Type": "application/zip",
          "Content-Disposition": 'attachment; filename="PlayerVideos.zip"',
        });
        file.pipe(res);
      }
    );
  });
};

exports.postPlayerVideo = (req, res, next) => {
  const uploadedVideo = req.file;
  const playerName = req.body.playerName;
  let keypointArray;

  if (!uploadedVideo) {
    res.json({ error: "video is null or invalid" });
  }

  try {
    keypointArray = JSON.parse(req.body.keypointArray.toString());
  } catch (err) {
    res.json({ error: "keypointArray is not in valid JSON format" });
  }

  PlayerVideo.findOne({ name: uploadedVideo.originalname })
    .then((video) => {
      if (!video) {
        newVideo = new PlayerVideo({
          name: uploadedVideo.originalname,
          playerName: playerName,
          keypointArray: keypointArray,
        });

        return newVideo.save();
      } else {
        video.name = uploadedVideo.originalname;
        video.playerName = playerName;
        video.keypointArray = keypointArray;

        return video.save();
      }
    })
    .then((reuslt) => {
      res.json({ status: "upload player video successful" });
    })
    .catch((err) => {
      console.log(err);
      res.json({ status: "upload player video failed" });
    });
};

exports.postUserOriginalVideo = (req, res, next) => {
  const uploadedVideo = req.file;
  const userId = req.body.userId;

  if (!uploadedVideo) {
    res.json({ error: "video is null or invalid" });
  }

  if (!userId) {
    res.json({ error: "userId is null or invalid" });
  }

  UserVideo.findOne({ originalName: uploadedVideo.originalname })
    .then((video) => {
      if (!video) {
        newVideo = new UserVideo({
          originalName: uploadedVideo.originalname,
          resultName: "",
          userId: userId,
          status: "pending",
        });
        return newVideo.save();
      } else {
        video.originalName = uploadedVideo.originalname;
        video.resultName = "";
        video.userId = userId;
        video.status = "pending";
        return video.save();
      }
    })
    .then((reuslt) => {
      runPythonScript(uploadedVideo.originalname);
      res.json({ status: "upload user original video successful" });
    })
    .catch((err) => {
      console.log(err);
      res.json({ status: "upload user original video failed" });
    });
};

exports.postUserResultVideo = (req, res, next) => {
  const uploadedVideo = req.file;
  let keypointArray;

  if (!uploadedVideo) {
    res.json({ error: "video is null or invalid" });
  }

  if (!req.body.originalName) {
    res.json({ error: "originalName is null" });
  }

  try {
    keypointArray = JSON.parse(req.body.keypointArray.toString());
  } catch (err) {
    res.json({ error: "keypointArray is not in valid JSON format" });
  }

  UserVideo.findOne({
    originalName: req.body.originalName,
  })
    .then((video) => {
      if (!video) {
        res.json({
          error: `no corresponding original video (${req.body.originalName})`,
        });
      } else {
        video.resultName = uploadedVideo.originalname;
        video.status = "Finished";
        video.keypointArray = keypointArray;
        return video.save();
      }
    })
    .then((reuslt) => {
      res.json({ status: "upload user result video successful" });
    })
    .catch((err) => {
      console.log(err);
      res.json({ status: "upload user result video failed" });
    });
};

exports.getVideoStatus = (req, res, next) => {
  UserVideo.findOne({ originalName: req.params.name }).then((video) => {
    if (!video)
      res.json({ error: `no corresponding video (${req.params.name})` });
    else res.json({ status: video.status });
  });
};

runPythonScript = async (originalVideoName) => {
  let result;
  const python = spawn("/home/hteam/anaconda3/envs/hackthon/bin/python", [
    path.join(__dirname, `../../posenet-pytorch/image_demo.py`),
    path.join(__dirname, `../videos/user/original/${originalVideoName}`),
    path.join(__dirname, `../videos/user/result/`),
  ]);

  python.stdout.on("data", function (data) {
    // console.log("Pipe data from python script ...");
    // result = JSON.parse(
    //   data.toString().split("weitingsplitme")[1].replace(/'/g, '"')
    // );
    console.log(data.toString());
    result = data.toString().split("weitingsplitme")[1].replace("\r\n", "");
  });

  python.on("close", (code) => {
    // console.log(`child process close all stdio with code ${code}`);
    console.log("Result Video Uploaded");

    UserVideo.findOne({
      originalName: originalVideoName,
    })
      .then((video) => {
        if (!video) {
          console.log(`no corresponding original video (${originalVideoName})`);
        } else {
          video.resultName = result.replace("\n", "");
          video.status = "Finished";
          video.keypointArray = {};
          return video.save();
        }
      })
      .then((reuslt) => {
        console.log({
          originalVideoName: originalVideoName,
          resultVideoName: result.replace("\n", ""),
          status: "upload user result video successful",
        });
      })
      .catch((err) => {
        console.log(err);
        console.log({
          originalVideoName: originalVideoName,
          resultVideoName: result,
          status: "upload user result video failed",
        });
      });
  });
};
