import { writable } from 'svelte/store';

export const messageStore = writable({
	client: "bot",
	content: "Let's start using Gitbot"
});

const sendMessage = (message, socket) => {
	if (socket.readyState <= 1) {
		socket.send(message);
	}
}

export default {
	subscribe: messageStore.subscribe,
	sendMessage
}

