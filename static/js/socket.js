$(document).ready(function() {
    let socket_chat = io.connect(location.protocol + "//" + document.domain + ":" + location.port + "/chat");

    socket_chat.on('connect', function() {
        socket.emit('chat', 1)
    });
    
    so

});