<script>
  export let name;
  import { onMount } from "svelte";
  let messageInput;
  let messages = [];
  let inputText = "";
  let numUsers = 0;

  onMount(() => {
    messageInput.focus();
  });

  const ws = new WebSocket("ws://127.0.0.1:6789");

  ws.onopen = function () {
    console.log("Websocket client connected");
  };

  ws.onmessage = function (e) {
    try{
		let data = JSON.parse(e.data);
    	if (data.type == "users") {
    		numUsers = data.count;
		}
	}catch (SyntaxError){
		console.log("Received: " + e.data);
		messages = [...messages, e.data];
		inputText = "";
	}
	
  };
  function handleClick() {
    ws.send(JSON.stringify(inputText));
  }
</script>

<style>
* {
    box-sizing: border-box;
  }
  
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }
  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }
  .chatbox {
    width: 100%;
    height: 50vh;
    padding: 0 1em;
    text-align: left;
    background-color: #eee;
    overflow-y: scroll;
    overscroll-behavior-y: contain;
    scroll-snap-type: y proximity;
  }
  .chatbox p {
    margin-top: 0.5em;
    margin-bottom: 0;
    padding-bottom: 0.5em;
  }
  .chatbox > p:last-child {
    scroll-snap-align: end;
  }
  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>

<main>
  <h1>Chat</h1>
  <p>
    Para enviar uma mensagem privada digite a mensagem seguida de " para " e o destinatario.
  </p>
  <div class="chatbox">
    {#each messages as message}
      <p>{message}</p>
    {/each}
  </div>
  <form class="inputbox">
    <input type="text" bind:this={messageInput} bind:value={inputText} />
    <button type="submit" on:click|preventDefault={handleClick}>Send</button>
  </form>
  <div class="state">
    <span class="users">{numUsers} {numUsers > 1 ? 'users' : 'user'}</span>
    online
  </div>
</main>