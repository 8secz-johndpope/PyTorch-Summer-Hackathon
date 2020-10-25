# PyTorch Summer Hackathon

###### tags: `TryTech`

![](https://github.com/h-tamader-team/PyTorch-Summer-Hackathon/blob/master/logo.png)

## Frontend

### Device
---

Environment: Swift

**Video Requirement**

Output
- .mp4
- UUID

## Backend

### Database
---

**RESTFul API**

`schemas`

```javascript
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

// Example
keypointArray = [
  {
    "score": "number",
    "keypoints": [
      {
        "score": "number",
        "part": "string",
        "position": {
          "x": "number",
          "y": "number"
        }
      }
    ]
  }
 ];
```

`functions`
```json=
// videos
{
  getUserOriginalVideoByName: {
    url: "https://<domain_name>/videos/user/original/<video_name>",
    returnName: video_name.mp4,
    returnType: "mp4",
  },
  getUserResultVideoByName: {
    url: "https://<domain_name>/videos/user/result/<video_name>",
    returnName: video_name.mp4,
    returnType: "mp4",
  },
  getPlayerVideoByName: {
    url: "https://<domain_name>/videos/player/<video_name>",
    returnName: video_name.mp4,
    returnType: "mp4",
  },
  getPlayerVideos: {
    url: "https://<domain_name>/videos/player",
    returnName: playerVideos.zip,
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
}
```

```json=
{
  getUserKeypointByName: {
    url: "https://<domain_name>/keypoints/user/<video_name>",
    return: keypoint,
    returnType: "json",
  },
  getUserKeypoints: {
    url: "https://<domain_name>/keypoints/user",
    return: [keypoint],
    returnType: "json",
  },
  getPlayerKeypointByName: {
    url: "https://<domain_name>/keypoints/player/<video_name>",
    return: keypoint,
    returnType: "json",
  },
  getPlayerKeypoints: {
    url: "https://<domain_name>/keypoints/player",
    return: [keypoint],
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
};
```

`Video storage`
Store:
Store video to the folder named with the factors including user name and UUID to the local server.
Request:
Get video by the factors including user name and UUID from the local server.

## Backend
---
![](https://github.com/h-tamader-team/PyTorch-Summer-Hackathon/blob/master/system.png)

### Ngrok and Node.js
1. Handle requests and store videos sent from the frontend
2. Create new record of UserID and video path to mongodb
3. Trigger the video prediction and comparison program to generate result videos
4. Notify users of the video status and return the video

### Posenet
The source code originates from the repo: **https://github.com/rwightman/posenet-pytorch** and there is no modification to their scripts. Only additional scripts were wrote for calculating similarity of detected keypoints and for editting videos.

### Similarity of poses
The following steps show how to calculate the similarity between two different series of points:
1. <font color="#6b6ce6">Detect keypoints of a person in two different videos. (if there are more than one person, only the one with the biggest bounding box will be recorded)</font>
2. <font color="#6b6ce6">Resize the two series of keypoints into the same size through the key of their height of bounding boxes.</font>
3. <font color="#6b6ce6">Calculate the cosine distance between each of their keypoints as the representatino of the similarity.</font>
4. <font color="#6b6ce6">The result having the shortest distance, their corresponding frame to the source video will be used as a time key to edit these the fragment of these two videos.</font>