var express = require('express');
var path = require('path');
var mysql = require('mysql');
var app = express();
var port = 8080;

var connection = mysql.createConnection({
   host: 'localhost',
   user: 'user??',
   password: 'password??',
   database: 'database??'
});
connection.connect(function(err) {
   if(!err) {
      console.log("Database Connected");
   } else {
      console.log("Error in creating database");
   }
});

app.use(express.static('public'));

app.listen(port, function() {
   console.log('Server running on ' + port);
});

app.get('/', function(req, res) {
   res.sendFile(path.join(__dirname + '/public/index.html'));
});

app.get('/api/data', function(req, res) {
   connection.query("query string", function(err, rows, fields) {
      connection.end();
      if(!err) {
         res.json(rows);
      } else {
         res.status(500);
         res.send("Connection fucked up");
      }
   });
});
