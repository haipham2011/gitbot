<script>
	import { onMount } from 'svelte';
	import store, { messageStore } from './store.js';
	import Message from './message.svelte';

    const { VITE_BACKEND_HOST, VITE_BACKEND_PORT, VITE_API, VITE_API_VERSION } = import.meta.env
    const API_URL = `http://${VITE_BACKEND_HOST}:${VITE_BACKEND_PORT}/${VITE_API}/${VITE_API_VERSION}`
	const botName = 'Gitbot';
	let message;
	let messages = [];
	let socket;

	onMount(() => {
		socket = new WebSocket(`ws://${VITE_BACKEND_HOST}:${VITE_BACKEND_PORT}/ws/${1234}`);

		// Connection opened
		socket.addEventListener('open', function (event) {
			console.log("It's open");
		});

		// Listen for messages
		socket.addEventListener('message', function (event) {
			messageStore.set(JSON.parse(event.data));
		});
	});

	onMount(() => {
		store.subscribe((currentMessage) => {
			messages = [...messages, currentMessage];
		});
	});

	function onSendMessage() {
		if (message.length > 0) {
			store.sendMessage(message, socket);
			message = '';
		}
	}

	$: if (messages.at(-1)?.action === 'get') {
		console.log('Get repos info');
		switch (messages.at(-1)?.tag) {
			case 'repos':
				getRepos();
				break;
			case 'events':
				getEvents();
				break;
			case 'Statistics':
				getStatistics();
				break;
			default:
				break;
		}
	}

	async function getRepos() {
		const res = await fetch(`${API_URL}/repos`, {
			method: 'GET'
		});

		const json = await res.json();
		messages = [
			...messages,
			{
				client: 'bot',
				content: json,
				tag: 'repos'
			}
		];
	}

	async function getEvents() {
		const res = await fetch(`${API_URL}/events`, {
			method: 'GET'
		});

		const json = await res.json();
		messages = [
			...messages,
			{
				client: 'bot',
				content: json,
				tag: 'events'
			}
		];
	}

	async function getStatistics() {
		const res = await fetch(`${API_URL}/statistics`, {
			method: 'GET'
		});

		const json = await res.json();
		messages = [
			...messages,
			{
				client: 'bot',
				content: json,
				tag: 'Statistics'
			}
		];
	}
</script>

<div class="md:container md:mx-auto p-10">
	<div class="border rounded">
		<div>
			<div class="w-full h-full">
				<div class="relative flex items-center p-3 border-b border-gray-300">
					<img
						class="object-cover w-10 h-10 rounded-full"
						src="data:image/png;base64,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"
						alt="username"
					/>
					<span class="block ml-2 font-bold text-gray-600">{botName}</span>
					<span class="absolute w-3 h-3 bg-green-600 rounded-full left-10 top-3" />
				</div>
				<div class="relative w-full p-6 overflow-y-auto h-[60rem]">
					<ul class="space-y-2">
						{#each messages as message, i}
							<Message {message} direction={message.client !== 'bot' ? 'start' : 'end'} />
						{/each}
					</ul>
				</div>

				<form
					on:submit|preventDefault={onSendMessage}
					class="flex items-center justify-between w-full p-3 border-t border-gray-300"
				>
					<button>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-6 h-6 text-gray-500"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
							/>
						</svg>
					</button>
					<button>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-5 h-5 text-gray-500"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
							/>
						</svg>
					</button>

					<input
						type="text"
						placeholder="Message"
						class="block w-full py-2 pl-4 mx-3 bg-gray-100 rounded-full outline-none focus:text-gray-700"
						name="message"
						required
						bind:value={message}
					/>
					<button>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="w-5 h-5 text-gray-500"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
							/>
						</svg>
					</button>
					<button type="submit">
						<svg
							class="w-5 h-5 text-gray-500 origin-center transform rotate-90"
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 20 20"
							fill="currentColor"
						>
							<path
								d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"
							/>
						</svg>
					</button>
				</form>
			</div>
		</div>
	</div>
</div>
