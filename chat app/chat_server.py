import socket
import threading

# Server setup
HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

clients = []
nicknames = []
message_history = []  # To store chat history
# Broadcast messages to all clients
def broadcast(message, sender=None):
    if sender:
        message = f"{sender}: {message}".encode('utf-8')  # Encode message as bytes
        message_history.append(message)  # Save message history
    elif isinstance(message, str):
        message = message.encode('utf-8')  # Ensure non-sender messages are encoded
    for client in clients:
        client.send(message)

# Handle private messaging
def private_message(sender, recipient_nick, message):
    if recipient_nick in nicknames:
        recipient_index = nicknames.index(recipient_nick)
        recipient_client = clients[recipient_index]
        sender_message = f"[PRIVATE] {sender}: {message}".encode('utf-8')
        recipient_client.send(sender_message)
    else:
        sender_index = nicknames.index(sender)
        clients[sender_index].send("User not found.".encode('utf-8'))

# Handle individual client
def handle_client(client):
    index = clients.index(client)
    nickname = nicknames[index]
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            # Handle commands
            if message.startswith('/'):
                command = message.split()[0]
                if command == "/list":
                    client.send(f"Active users: {', '.join(nicknames)}".encode('utf-8'))
                elif command.startswith("/msg"):
                    parts = message.split(" ", 2)
                    if len(parts) >= 3:
                        recipient = parts[1]
                        private_message(nickname, recipient, parts[2])
                    else:
                        client.send("Usage: /msg <nickname> <message>".encode('utf-8'))
                elif command == "/quit":
                    broadcast(f"{nickname} has left the chat.", None)
                    clients.remove(client)
                    nicknames.remove(nickname)
                    client.close()
                    break
                else:
                    client.send("Unknown command.".encode('utf-8'))
            else:
                broadcast(message, sender=nickname)

        except:
            clients.remove(client)
            nicknames.remove(nickname)
            client.close()
            broadcast(f"{nickname} has left the chat.", None)
            break

# Accept new connections
def accept_connections():
    while True:
        client, address = server_socket.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname: {nickname}")
        broadcast(f"{nickname} joined the chat!", None)

        # Send chat history to the new client
        for msg in message_history:
            client.send(msg)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Server is running...")
accept_connections()
