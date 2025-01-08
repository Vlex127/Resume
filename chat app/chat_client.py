import socket
import threading

# Client setup
HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Receive messages from server
def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Disconnected from server.")
            client_socket.close()
            break

# Send messages to server
def send():
    while True:
        message = input()
        if message.startswith('/'):
            if message == "/quit":
                client_socket.send(message.encode('utf-8'))
                client_socket.close()
                break
            else:
                client_socket.send(message.encode('utf-8'))
        else:
            client_socket.send(message.encode('utf-8'))

# Get user nickname
nickname = input("Choose your nickname: ")
client_socket.send(nickname.encode('utf-8'))

# Start threads for sending and receiving
receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
