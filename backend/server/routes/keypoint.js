const path = require('path');
const express = require('express');
const keypointController = require('../controllers/keypoint');

const router = express.Router();

router.get('/', keypointController.getKeypoints);

router.get('/user', keypointController.getUserKeypoints);

router.get('/user/:name', keypointController.getUserKeypoint);

router.get('/player', keypointController.getPlayerKeypoints);

router.get('/player/:name', keypointController.getPlayerKeypoint);

router.post('/user/:name', keypointController.postUserKeypoint);

router.post('/player/:name', keypointController.postPlayerKeypoint);

module.exports = router;
