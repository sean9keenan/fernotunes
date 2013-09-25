
var socket = io.connect('http://fernotunessocket.skeenan.com');

socket.on('returnData', function (data) {
	console.log(data);
  $('#header').html(data)
});

socket.emit('spotify', { action: '5' });

$(".play").click(function() {
  socket.emit('spotify', { action: '0' });
});
$(".pause").click(function() {
  socket.emit('spotify', { action: '0' });
});

$(".rw").click(function() {
  socket.emit('spotify', { action: '1' });
});

$(".ff").click(function() {
  socket.emit('spotify', { action: '2' });
});