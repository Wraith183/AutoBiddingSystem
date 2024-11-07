import socket
import threading
import random
import json

# Function to initialize items
def initialize_items():
    items = {}
    for i in range(1, 11):  # Create 10 items
        items[f'Item{i}'] = {
            'units': random.randint(10, 100),  # Random units between 10 and 100
            'price': random.randint(50, 800),  # Random price between 50 and 800
            'highest_bid': 0,
            'highest_bidder': None
        }
    return items

# Initialize items when the server starts
items = initialize_items()
print("Initial Items:", items)

# Handle client connections and bidding
def handle_client(client_socket):
    print(f"Handling client {client_socket.getpeername()}")
    
    # Send the items to the client
    client_socket.send(json.dumps(items).encode())
    
    while True:
        # Receive bid from client
        try:
            bid_data = client_socket.recv(1024).decode()
            if not bid_data:
                break
            
            bid = json.loads(bid_data)
            item = bid['item']
            bid_amount = bid['bid']
            print(f"Received bid of {bid_amount} on {item} from {client_socket.getpeername()}")

            # Check if bid is higher than the current highest bid
            if bid_amount > items[item]['highest_bid']:
                items[item]['highest_bid'] = bid_amount
                items[item]['highest_bidder'] = client_socket.getpeername()
                
                # Inform client that they are the highest bidder
                response = {"status": "won", "item": item, "amount": bid_amount}
                client_socket.send(json.dumps(response).encode())
                print(f"{client_socket.getpeername()} won {item} for {bid_amount}")
                
                # Reduce item quantity
                items[item]['units'] -= 1
                if items[item]['units'] <= 0:
                    print(f"{item} is sold out")
                    del items[item]  # Remove sold-out item
            else:
                # Inform client that they did not win
                response = {"status": "outbid", "item": item, "amount": bid_amount}
                client_socket.send(json.dumps(response).encode())
        
        except Exception as e:
            print(f"Error handling bid from {client_socket.getpeername()}: {e}")
            break
    
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

"""
TO DO
- Create a max timer for each item
- Ensure we can connect clients from different laptops on the same server

"""