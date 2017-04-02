var express = require('express');
var app = express();
var port = 8080;

app.use(express.static(__dirname + "/public"));

app.listen(port, function() {
   console.log('Server running');
});

app.get('/', function(req, res) {
   res.sendfile('./public/index.html');
});
