const express = require('express');
const router = express.Router();
module.exports = router;

router.get("/", function(req,res) {
    res.redirect("/index.html");
});

router.get(["/","/index.html","/index"], function(req, res) {
    res.render("index");
});