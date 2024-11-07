import socket

# Step 1: Create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 2: Connect to the server
server_host = 'localhost'  # Same as in server.py
server_port = 12345
client_socket.connect((server_host, server_port))

print("Connected to the server!")

# Step 3: Close the client after connecting for testing purposes
client_socket.close()
