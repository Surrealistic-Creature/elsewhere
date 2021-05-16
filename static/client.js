let socket = new WebSocket('ws://0.0.0.0:8000/ws');

document.forms.sender.onsubmit = function() {
	let outgoingMessage = this.message.value;

	socket.send(outgoingMessage);
	return false;
};

socket.onmessage = function(event) {
  let message = event.data;
  message = JSON.parse(message);  
  let messageElem = document.createElement('p');
  messageElem.textContent = message;
  messageElem.classList.add('ws_msg');
  document.getElementById('ws_block').prepend(messageElem);
}
