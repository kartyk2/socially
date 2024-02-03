function getOnline() {
  const user_id = document.getElementById('user-id-input');
  const user = user_id.value;
  console.log(user);

  const socket = new WebSocket(`ws://localhost:8000/ws/${user}`);

  socket.onopen = () => {
    socket.send("Hello, WebSocket Server!");
  };

  socket.onmessage = (event) => {
    console.log("Server says: " + event.data);
  };

  // Close the WebSocket connection when done
  socket.onclose = () => {
    console.log("WebSocket connection closed.");
  };

  socket.onerror = (error) => {
    console.log(error);
  };
}
