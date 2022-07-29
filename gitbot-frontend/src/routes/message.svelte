<script>
	import Graph from './graph.svelte';
	export let message;
	export let direction = 'start';
</script>

{#if typeof message.content === 'string'}
	<li class="flex justify-{direction}">
		<div class="relative max-w-xl px-4 py-2 text-gray-700 rounded shadow">
			<span class="block">{message.content}</span>
		</div>
	</li>
{:else if message.tag === 'repos'}
	<li class="flex justify-{direction}">
		<div class="relative max-w-xl px-4 py-2 text-gray-700 rounded shadow">
			<span class="block">
				You have <b class="text-sky-400">{message.content.total}</b> repos <br />
				<b class="text-sky-400">{message.content.forked}</b> forked repos <br />
				<b class="text-sky-400">{message.content.own}</b> owned repos <br />
				<br />
				Here are your top <b class="text-sky-400">three</b> recent repos:
				<br />
				<ul>
					{#each message.content.recentRepos as repo}
						<li>
							<a href={repo.url} class="text-sky-400 no-underline hover:underline">{repo.name}</a>
						</li>
					{/each}
				</ul>
			</span>
		</div>
	</li>
{:else if message.tag === 'events'}
	<li class="flex justify-{direction}">
		<div class="relative max-w-xl px-4 py-2 text-gray-700 rounded shadow">
			<span class="block">
				You have <b class="text-red-400">{message.content.total}</b> events unchecked <br />
				<b class="text-red-400">{message.content.pullRequest}</b> pull requests <br />
				<b class="text-red-400">{message.content.createEvent}</b> create events <br />
				<b class="text-red-400">{message.content.deleteEvent}</b> delete events
			</span>
		</div>
	</li>
{:else}
	<li class="flex justify-end">
		<div class="relative w-full text-gray-700 rounded shadow">
			<span class="block">
				<Graph data={message.content} />
			</span>
		</div>
	</li>
{/if}
