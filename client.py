import socket
import json
import random
import time

# Set up client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = 'localhost'
server_port = 12345
client_socket.connect((server_host, server_port))

print("Connected to the server!")

# Receive items from the server
items_data = client_socket.recv(1024).decode()
items = json.loads(items_data)
print("Received items from server:", items)

# Each client will have a maximum acceptable price for each item
max_prices = {item: random.randint(item_data['price'] + 100, item_data['price'] + 500) for item, item_data in items.items()}
print("Client maximum prices:", max_prices)

# Bidding process
while True:
    # Randomly decide to bid or skip (70% chance to bid)
    if random.random() > 0.3:
        # Randomly select an item to bid on
        item_to_bid = random.choice(list(items.keys()))
        current_price = items[item_to_bid]['price']
        
        # Only bid if the current price is below the maximum acceptable price
        if current_price < max_prices[item_to_bid]:
            # Increase the bid by a random amount
            bid_amount = current_price + random.randint(1, 50)
            bid_data = {'item': item_to_bid, 'bid': bid_amount}
            
            # Send bid to server
            client_socket.send(json.dumps(bid_data).encode())
            print(f"Client bids {bid_amount} on {item_to_bid}")
            
            # Wait for server response
            server_response = client_socket.recv(1024).decode()
            response_data = json.loads(server_response)
            print("Server response:", response_data)
            
            # If the item is won, stop bidding for that item
            if response_data.get("status") == "won":
                print(f"Client won {item_to_bid} for {bid_amount}!")
                items[item_to_bid]['units'] -= 1
                if items[item_to_bid]['units'] <= 0:
                    del items[item_to_bid]  # Remove sold-out item
        else:
            print(f"Client skips bidding on {item_to_bid} (price too high)")
    
    # Small delay to simulate real-time bidding
    time.sleep(random.uniform(0.5, 1.5))
    
    # Break loop if no items remain
    if not items:
        print("All items sold out. Ending bidding.")
        break

client_socket.close()
