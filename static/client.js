let socket = new WebSocket('ws://0.0.0.0:8000/ws');

document.forms.sender.onsubmit = function() {
	let outgoingMessage = this.message.value;

	socket.send(outgoingMessage);
	return false;
};

//socket.onmessage = function(event) {
//	var incomingMessage = event.data;
//	showMessage(incomingMessage);
//};

socket.onmessage = function(event) {
  let message = event.data;

//function showMessage(message) {
//  var messageElem = document.createElement('div');
//  messageElem.appendChild(document.createTextNode(message));
//  document.getElementById('subscribe').appendChild(messageElem);
//}

  let messageElem = document.createElement('div');
  messageElem.textContent = message;
  document.getElementById('messages').prepend(messageElem);
}
