const axios = require("axios");
const fs = require("fs");
const path = require("path");
const FormData = require("form-data");

const uploadVideo = async () => {
  const formData = new FormData();
  formData.append(
    "video",
    fs.createReadStream(path.join(__dirname, "test.mp4"))
  );
  formData.append("playerName", "Kobe");
  formData.append(
    "keypointArray",
    JSON.stringify([
      {
        score: 20.1344,
        keypoints: [
          {
            score: 12.1344,
            part: "nose",
            position: { x: 1257.3241, y: 2314.3333 },
          },
        ],
      },
    ])
  );

  axios({
    method: "post",
    url: "https://7245b8eb0baa.ngrok.io/videos/player",
    data: formData,
    headers: {
      "Content-Type": `multipart/form-data; boundary=${formData._boundary}`,
    },
    maxContentLength: Infinity,
    maxBodyLength: Infinity,
  })
    .then((result) => {
      console.log("upload successful");
    })
    .catch((err) => {
      //console.log(err);
      throw err;
    });

  //   axios({
  //     method: "get",
  //     url: "https://e836dddb6ded.ngrok.io/videos/",
  //     maxContentLength: Infinity,
  //     maxBodyLength: Infinity,
  //   })
  //     .then((result) => {
  //       console.log(result.data);
  //     })
  //     .catch((err) => {
  //       //console.log(err);
  //       throw err;
  //     });
};

uploadVideo();
