var express = require('express');
var router = express.Router();

var config = require('./config.js');
var multer  = require('multer');
var AWS = require('aws-sdk');

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null,'./Acho/data/src/yes');
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    }
})

const upload = multer({storage});

const storage1 = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null,'./Acho/data/src/no');
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    }
})
const upload1 = multer({storage1});

const storage2 = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null,'./Acho/data/src/middle');
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    }
})
const upload2 = multer({storage2});

//config.js에서 작성한 리전 정보를 설정합니다.
AWS.config.region = config.region;
var rekognition = new AWS.Rekognition(
    {
        region: config.region
    }
);

router.post('/yes', upload.single("image"),function (req, res, next) {
    console.log("asdasdasd")
    
    const spawn = require('child_process').spawn;

    const result = spawn('python3', ['Acho/main.py']); 

    result.stdout.on('data', function(data) { console.log(data.toString()); }); 

    result.stderr.on('data', function(data) { console.log(data.toString()); });
});

router.post('/no', upload1.single("image"),function (req, res, next) {
    console.log("asdasdasd")
    
    const spawn = require('child_process').spawn;

    const result = spawn('python3', ['Acho/main.py']); 

    result.stdout.on('data', function(data) { console.log(data.toString()); }); 

    result.stderr.on('data', function(data) { console.log(data.toString()); });
});

router.post('/middle', upload2.single("image"),function (req, res, next) {
    console.log("asdasdasd")
    
    const spawn = require('child_process').spawn;

    const result = spawn('python3', ['Acho/main.py']); 

    result.stdout.on('data', function(data) { console.log(data.toString()); }); 

    result.stderr.on('data', function(data) { console.log(data.toString()); });
});



module.exports = router;
