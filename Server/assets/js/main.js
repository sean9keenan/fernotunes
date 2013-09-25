
var socket = io.connect('http://fernotunessocket.skeenan.com');

socket.on('returnData', function (data) {
	console.log(data);
	$('#header').html(data)
	if (data == "Nothing is playing"){
		$("#playpause").addClass("play").removeClass("pause")
	} else {
		$("#playpause").removeClass("play").addClass("pause")
	}
});

socket.emit('spotify', { action: '5' });

$("#playpause").click(function() {
  socket.emit('spotify', { action: '0' });
});

$(".rw").click(function() {
  socket.emit('spotify', { action: '1' });
});

$(".ff").click(function() {
  socket.emit('spotify', { action: '2' });
});