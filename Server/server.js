var portListen = 9000;
var clientPort = 9001;
var httpServer = 9002;

var http    = require('http'),
    express = require('express'),
    fs      = require('fs'),
    jQuery  = require('jquery'),
    stache  = require('stache'),
    app     = module.exports = express.createServer(),
    io      = require('socket.io').listen(portListen), // for npm, otherwise use require('./path/to/socket.io')
    ws      = require("ws"),
// Constants
    max_n   = 50;

// This is how often we have to ping the Arduino in order to keep the websocket
// connection open and fast
var pingMinutes = 1;

app.set('_title', 'Inferno Tunes');
app.set('max_n', max_n);

app.configure(function(){
  app.set('views', __dirname + '/views');
  app.set('view engine', 'mustache');
  app.use(express.bodyParser());
  app.use(express.cookieParser());
  app.use(express.static(__dirname + '/assets'));
  app.use(express.methodOverride());
  //app.use(express.csrf());

  //For debugging
  // app.use(express.logger({format: ':method :url'}));

  app.use(express.errorHandler());
  app.use(app.router);
});


// Routes

app.get('/', function(req, res){
  res.sendfile('./assets/index.html');
});



app.get('/action/*', function(req, res){

  var performAction = "/action/"

  if (req.url.length > performAction.length){
    try {
      var msgSend = req.url.substr(performAction.length);
      if (clientCallback != null){
        clientCallback(msgSend)
      }
    } catch (err){
      console.log("Invalid URL request: " + err);
    }
  }

  res.redirect('/');

})

app.get('/*', function(req, res){
  res.redirect('/');
});




app.listen(httpServer);


function generatePerformAction(jsonIn){
  var output = "http://link.skeenan.com/action/" + encodeURIComponent(JSON.stringify(jsonIn));
}


try{

var clientCallback = [];

io.sockets.on('connection', function (socket) {

  console.log(socket.handshake.headers["x-forwarded-for"])

  socket.on('spotify', function (data, callback) {

    console.log(data);

    unique = socket.handshake.headers["x-forwarded-for"].replace(/,/g, '')

    // if (clientCallback != null){
    //   clientCallback(data.action + "," + unique)
    // }

    // if (clientCallback != []) {
    //   for (var i = clientCallback.length - 1; i >= 0; i--) {
    //     clientCallback[i](data.action + "," + unique, i)
    //   };
    // }

    wss.broadcast(data.action + "," + unique)

    // socket.emit('devices:create', json);
    // socket.broadcast.emit('devices:create', json);

  });

});


var WebSocketServer = ws.Server
  , wss = new WebSocketServer({port: clientPort, protocolVersion: 8});

wss.on('connection', function(socket) {
  console.log('connect!')
  socket.valid = true

  socket.on('message', function(message) {
    console.log('received: %s', message);
    io.sockets.emit('returnData', message)
  });

  socket.send('something');

  socket.on('close', function(reason) {
    console.log('connection closed')
    socket.valid = false
  });

  clientCallback.push(function(msg, index) {
    console.log("sending: " + msg)
    if (socket.valid) {
      socket.send(msg)
    } else if (index != -1) {
      clientCallback.splice(i, 1)
    }
  });

});

wss.broadcast = function(data) {
    for(var i in this.clients)
        this.clients[i].send(data);
};

// setInterval(function() {
//   if (clientCallback != null) {
//     clientCallback('ping');
//   }
// }, pingMinutes*60*1000);

// var server = socket.createServer();

// server.addListener("connection", function(connection){
//   console.log('connect!')

//   clientCallback = function(msg) {
//     server.send(connection.id, msg);
//     console.log("\n\nSending to client:\n" + msg)
//   };

//   connection.addListener("message", function(msg){
//     console.log("msg!" + msg)
//     io.sockets.broadcast.emit(msg)

//   });

//   // Crappy fix to make sure that client maintains a constant
//   // connection for low latency
//   setInterval(function() {
//     clientCallback('ping');
//   }, pingMinutes*60*1000);
// });

// server.listen(clientPort);
} catch(err){
  console.log(err);
}
