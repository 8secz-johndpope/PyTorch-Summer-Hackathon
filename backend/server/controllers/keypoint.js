const userVideo = require("../models/userVideo");
const playerVideo = require("../models/playerVideo");

exports.getKeypoints = (req, res, next) => {
  res.json({
    getUserKeypointByName: {
      url: "https://<domain_name>/keypoints/user/<video_name>",
      return: "keypoint",
      returnType: "json",
    },
    getUserKeypoints: {
      url: "https://<domain_name>/keypoints/user",
      return: "[keypoint]",
      returnType: "json",
    },
    getPlayerKeypointByName: {
      url: "https://<domain_name>/keypoints/player/<video_name>",
      return: "keypoint",
      returnType: "json",
    },
    getPlayerKeypoints: {
      url: "https://<domain_name>/keypoints/player",
      return: "[keypoint]",
      returnType: "json",
    },
    postUserKeypoint: {
      url: "https://<domain_name>/keypoints/user/<video_name>",
      form: {
        status: "<status>  (optional)",
        keypointArray: "<keypoint_array>",
      },
      contentType: "x-www-form-urlencoded",
    },
    postPlayerKeypoint: {
      url: "https://<domain_name>/keypoints/player/<video_name>",
      form: {
        playerName: "<player_name>  (optional)",
        keypointArray: "<keypoint_array>",
      },
      contentType: "x-www-form-urlencoded",
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

exports.getUserKeypoint = (req, res, next) => {
  userVideo
    .findOne({ originalName: req.params.name })
    .select(
      "-_id \
      -keypointArray._id \
      -keypointArray.createdAt \
      -keypointArray.updatedAt \
      -keypointArray.keypoints._id \
      -keypointArray.keypoints.createdAt \
      -keypointArray.keypoints.updatedAt"
    )
    .then((video) => {
      if (!video) {
        res.json({ error: `no corresponding video (${req.params.name})` });
      } else {
        const result = {
          name: video.originalName,
          keypointArray: video.keypointArray,
        };
        res.json(result);
      }
    })
    .catch((err) => {
      console.log(err);
      res.json({ error: err });
    });
};

exports.getPlayerKeypoint = (req, res, next) => {
  playerVideo
    .findOne({ name: req.params.name })
    .select(
      "-_id \
      -keypointArray._id \
      -keypointArray.createdAt \
      -keypointArray.updatedAt \
      -keypointArray.keypoints._id \
      -keypointArray.keypoints.createdAt \
      -keypointArray.keypoints.updatedAt"
    )
    .then((video) => {
      if (!video) {
        res.json({ error: `no corresponding video (${req.params.name})` });
      } else {
        const result = {
          name: video.name,
          keypointArray: video.keypointArray,
        };
        res.json(result);
      }
    })
    .catch((err) => {
      console.log(err);
      res.json({ error: err });
    });
};

exports.getUserKeypoints = (req, res, next) => {
  userVideo
    .find({})
    .select(
      "-_id \
      -__v \
      -userId \
      -status \
      -resultName \
      -createdAt \
      -updatedAt \
      -keypointArray._id \
      -keypointArray.createdAt \
      -keypointArray.updatedAt \
      -keypointArray.keypoints._id \
      -keypointArray.keypoints.createdAt \
      -keypointArray.keypoints.updatedAt"
    )
    .map((videos) => {
      return videos.map((video) => ({
        name: video.originalName,
        keypointArray: video.keypointArray,
      }));
    })
    .then((result) => {
      if (!result) {
        res.json({ error: "no videos and keypoints" });
      } else {
        res.json(result);
      }
    })
    .catch((err) => {
      console.log("Fail to return user keypoints");
      res.json({ error: err });
    });
};

exports.getPlayerKeypoints = (req, res, next) => {
  playerVideo
    .find({})
    .select(
      "-_id \
      -keypointArray._id \
      -keypointArray.createdAt \
      -keypointArray.updatedAt \
      -keypointArray.keypoints._id \
      -keypointArray.keypoints.createdAt \
      -keypointArray.keypoints.updatedAt"
    )
    .map((videos) => {
      return videos.map((video) => ({
        name: video.name,
        keypointArray: video.keypointArray,
      }));
    })
    .then((result) => {
      if (!result) {
        res.json({ error: "no videos and keypoints" });
      } else {
        res.json(result);
      }
    })
    .catch((err) => {
      console.log("Fail to get player keypoints");
      res.json({ error: err });
    });
};

// application/x-www-form-urlencoded
exports.postUserKeypoint = (req, res, next) => {
  userVideo
    .findOne({ originalName: req.params.name })
    .then((video) => {
      if (!video) {
        res.json({ error: "no corresponding video" });
      } else {
        if (req.body.status) video.status = req.body.status;
        if (req.body.keypointArray) {
          try {
            video.keypointArray = JSON.parse(req.body.keypointArray);
          } catch (err) {
            res.json({
              error: "keypointArray is not in valid JSON format",
            });
          }
        } else
          res.json({
            error: "no keypointArray, please try using x-www-form-urlencoded",
          });
        return video.save();
      }
    })
    .then((reuslt) => {
      res.json({ status: "post user keypoint successful" });
    })
    .catch((err) => {
      console.log("Fail to post user keypoint");
      res.json({ error: err });
    });
};

// application/x-www-form-urlencoded
exports.postPlayerKeypoint = (req, res, next) => {
  playerVideo
    .findOne({ name: req.params.name })
    .then((video) => {
      if (!video) {
        res.json({ error: "no corresponding video" });
      } else {
        if (req.body.playerName) video.playerName = req.body.playerName;
        if (req.body.keypointArray) {
          try {
            video.keypointArray = JSON.parse(req.body.keypointArray);
          } catch (err) {
            res.json({
              error: "keypointArray is not in valid JSON format",
            });
          }
        } else
          res.json({
            error: "no keypointArray, please try using x-www-form-urlencoded",
          });
        return video.save();
      }
    })
    .then((reuslt) => {
      res.json({ status: "post player keypoint successful" });
    })
    .catch((err) => {
      console.log("Fail to post player keypoint");
      res.json({ error: err });
    });
};
