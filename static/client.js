let socket = new WebSocket('ws://' + location.host + '/ws');

document.forms.sender.onsubmit = function() {
	let outgoingMessage = this.message.value;

	socket.send(outgoingMessage);
	return false;
};

socket.onmessage = function(event) {
  let message = event.data;
  message = JSON.stringify(message);  
  let messageElem = document.createElement('p');
  messageElem.textContent = message;
  messageElem.classList.add('ws_msg');
  document.getElementById('ws_block').prepend(messageElem);
}
