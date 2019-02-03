var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});
socket.on('my response', function(msg) {
  console.log(msg);
})
socket.on('user joined', function(users) {
    console.log(users);
    $("#userList").remove();
    $("#main").append(createUserListHTML(users));
})