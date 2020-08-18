# PyTorch Summer Hackathon

## Frontend

### Device
---

Environment: SwiftUI

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
const PlayerVideo = new Schema({
    uuid: {type: String, require: true},
    playerName: {type: String, required: true},
    keypoints: {type: [Object], required: true},
    },
    { timestamps: true }
);

const UserVideo = new Schema({
    uuid: {type: String, require: true},
    userId: {type: String, required: true},
    keypoints: {type: [Object], required: true},
    },
    { timestamps: true }
);
```

`functions`
```javascript
GetAllKeypoints = () => {
return array();
}

PostVideo = (video, uuid) => {
}

GetResultVideoByUUID = (uuid) => {
return video;
}

GetOriginalVideoByUUID = (uuid) => {
return video;
}

GetEditStatus = (uuid) => {
return enum;
}
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