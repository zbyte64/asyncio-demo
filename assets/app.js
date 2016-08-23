$(document).ready(function() {
var connection = new WebSocket('ws://127.0.0.1:8080/chat');

// Log messages from the server
connection.onmessage = function (e) {
  console.log('Server: ' + e.data);
  $("#responses").append("<p>"+e.data+"</p>")
};

$("#send").submit(function(event) {
  event.preventDefault()
  var message = this["text"].value
  if (!message) return;
  console.log("Sending:", message);
  connection.send(message);
})
})
