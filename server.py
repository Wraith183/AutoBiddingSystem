import socket
import threading

def handle_client(client_socket):
    print(f"Handling client {client_socket.getpeername()}")
    client_socket.send("Welcome to the server!".encode())  # Optional: Send a welcome message to the client
    client_socket.close()

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen()
print("Server is listening for client connections...")

# Accept multiple clients
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connected to client at {client_address}")
    # Start a new thread to handle each client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
