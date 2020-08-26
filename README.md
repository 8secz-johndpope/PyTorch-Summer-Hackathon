# PyTorch Summer Hackathon

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

`Domain`
Need to deploy api to a server with a static domain.

### Backend
---

### Model
---