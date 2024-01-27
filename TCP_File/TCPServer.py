import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []  # List of all currently connected users

def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                final_msg = f"{username}~{message}"
                send_messages_to_all(final_msg)
            else:
                print(f"The message sent from client {username} is empty")
        except ConnectionResetError:
            remove_client(username)
            break

def send_message_to_client(client, message):
    try:
        client.sendall(message.encode())
    except ConnectionError:
        print("Failed to send message.")

def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

def remove_client(username):
    for user in active_clients:
        if user[0] == username:
            active_clients.remove(user)
            prompt_message = f"SERVER~{username} left the chat"
            send_messages_to_all(prompt_message)
            break

def client_handler(client):
    try:
        username = client.recv(2048).decode('utf-8')
        if username:
            active_clients.append((username, client))
            prompt_message = f"SERVER~{username} joined the chat"
            send_messages_to_all(prompt_message)
            threading.Thread(target=listen_for_messages, args=(client, username)).start()
        else:
            print("Client username is empty")
    except ConnectionResetError:
        print("Connection reset by client.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Server is running on {HOST}:{PORT}")
    except OSError:
        print(f"Unable to bind to {HOST}:{PORT}")
        return
    
    server.listen(LISTENER_LIMIT)
    print("Waiting for incoming connections...")

    while True:
        client, address = server.accept()
        print(f"Connected to client {address[0]}:{address[1]}")
        threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    main()
