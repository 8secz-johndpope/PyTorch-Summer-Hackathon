const path = require("path");
const express = require("express");
const videoController = require("../controllers/video");

const router = express.Router();

router.get("/", videoController.getVideos);

router.get("/player", videoController.getPlayerVideos);

router.post("/user/original", videoController.postUserOriginalVideo);

router.post("/user/result", videoController.postUserResultVideo);

router.post("/player", videoController.postPlayerVideo);

router.get("/status/:name", videoController.getVideoStatus);

// router.post('/videos', videoController.postVideos);

// router.post('/video-delete', shopController.postCartDeleteProduct);

// router.post('/video', isAuth, shopController.postCart);

module.exports = router;
