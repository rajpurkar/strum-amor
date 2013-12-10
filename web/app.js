/**
 * Module dependencies.
 */
var express = require('express');
var https = require('https');
var path = require('path');
var fs = require('fs');
var http = require('http');
var exec = require('child_process').exec;

var options = {
	key : fs.readFileSync('./keys/key.pem'),
	cert : fs.readFileSync('./keys/key-cert.pem')
};
var app = express();

// all environments
app.set('port', process.env.PORT || 3000);
app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
//app.use(require('stylus').middleware(__dirname + '/public'));
app.use(express.static(path.join(__dirname, 'public')));

// When in development mode, use the error handler
if ('development' == app.get('env')) {
	app.use(express.errorHandler());
}

//app.router should always be last
app.use(app.router);

//Logins
app.get('/main', function(req, res) {
	res.render('new');
});

app.get('/', function(req, res) {
	res.redirect('main');
});

//get predictions
app.post('/main', function(req, res) {
	var str = req.body.data.split(",")[1]
	var buf = new Buffer(str, 'base64');
	fs.writeFile("hello.wav", buf, function(err) {
		if (err)
			res.send(500, {
				error : 'something blew up'
			})
		var child = exec("./recog", function(error, stdout, stderr) {
			console.log('stdout: ' + stdout);
			res.send(stdout);
		});
	});
});

//app specific gets here
var executeTests = false;

if (executeTests) {
	//tests only during development only
	if ('development' == app.get('env')) {
	}
	//tests during production require a password
	else if ('production' == app.get('env')) {
		var auth = express.basicAuth(function(user, pass, callback) {
			var result = (user === 'psr' && pass === 'psr2');
			callback(null/* error */, result);
		});
		app.get('/testusers', auth, tests.testUser);
	}
}

//if the page does not exist
app.get("*", function(req, res) {
	res.status(404).send('Not found dude');
});

// Create an HTTPS service identical to the HTTP service.
var server = https.createServer(options, app)
//var server = http.createServer(app)
server.listen(app.get('port'));
var io = require('socket.io').listen(server);

io.sockets.on('connection', function(socket) {
	console.log("hey! " + socket.id)
	socket.emit('ready', "Yay");
	socket.on('set nickname', function(name) {
		socket.set('nickname', name, function() {
			socket.emit('news', {
				hello : 'world'
			});
		});
	});
	socket.on('disconnect', function () {
    	console.log("left! " + socket.id)
  	});

	socket.on('msg', function() {
		socket.get('nickname', function(err, name) {
			console.log('Chat message by ', name);
		});
	});
});
