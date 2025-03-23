const socket = io();

socket.on("connect", () => {
  console.log("Connected to server");
});

let username = prompt("Server Name?");
if (username) {
  console.log("You joined as:", username);

  // Inform the server about the new user
  socket.emit("new-user", username);
}

// Handle incoming chat messages
socket.on("send-server-message", (data) => {
  console.log(`${data.name}: ${data.message}`);
  if (
    data.name == karaokeserver &&
    data.message == "reloadqueuetablefunction"
  ) {
    displayqueuetable();
    initialfetchsongqueue();
  }
});

// Handle user connections
socket.on("user-connected", (name) => {
  console.log(`${name} connected`);
});

// Handle user disconnections
socket.on("user-disconnected", (username) => {
  console.log(`${username} disconnected`);
});

socket.on("disconnect", () => {
  console.log("Disconnected from server");
});

// Send message to a specific user
// document.getElementById("sendmessage").addEventListener("click", function () {
//   const recipientUsername = document.getElementById("recipientUsername").value;
//   const message = document.getElementById("inputmessage").value;

//   if (recipientUsername && message) {
//     socket.emit("send-client-message", {
//       recipient_username: recipientUsername,
//       message: message,
//     });
//   } else {
//     console.log("Recipient username or message is missing.");
//   }
// });
