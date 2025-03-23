# socket_handlers.py

class SocketHandlers:
    def __init__(self, sio):
        self.sio = sio
        self.users = {}
        self.username_to_sid = {}

    async def connect(self, sid, env):
        print("New Client Connected to This id :" + " " + str(sid))

    async def new_user(self, sid, username):
        self.users[sid] = username
        self.username_to_sid[username] = sid  # Update the mapping of username to SID
        print(f"User {username} connected with SID {sid}")
        await self.sio.emit("user-connected", username)

    async def send_client_message(self, sid, data):
        try:
            # Ensure that the data contains both 'recipient_username' and 'message'
            recipient_username = data.get("recipient_username")
            message = data.get("message")
            
            if not recipient_username or not message:
                raise ValueError("Missing 'recipient_username' or 'message' in data")

            # Get the sender's username
            sender_username = self.users.get(sid)
            if not sender_username:
                print(f"Sender with SID {sid} not found.")
                return

            print(f"Message from {sender_username}: {message}")
            
            # Find target_sid using recipient_username
            target_sid = self.username_to_sid.get(recipient_username)
            
            if target_sid:
                await self.sio.emit("send-server-message", {"name": sender_username, "message": message}, to=target_sid)
            else:
                print(f"Target user {recipient_username} not found.")

        except Exception as e:
            print(f"Error in send server message: {e}")

    async def disconnect(self, sid):
        if sid in self.users:  # Check if the SID exists in the users dictionary
            username = self.users[sid]
            del self.users[sid]
            del self.username_to_sid[username]  # Remove the mapping for the disconnected user
            await self.sio.emit("user-disconnected", username)
            print(f"User {username} disconnected")
        else:
            print(f"Unknown user with SID {sid} disconnected")

    def register_handlers(self):
        self.sio.on("connect")(self.connect)
        self.sio.on("new-user")(self.new_user)
        self.sio.on("send-client-message")(self.send_client_message)
        self.sio.on("disconnect")(self.disconnect)