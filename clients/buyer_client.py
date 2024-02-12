import socket
import keyboard
import time
from threading import Thread

# Constants
HEADER = 64
PORT = 5052
FORMAT = 'utf-8'
SERVER = '10.0.0.208'    # '10.203.15.151'
ADDR = (SERVER, PORT)
DISCONNECTED_MSG = '[DISCONNECTED]'
DELIMITER = '|'
SESSION_TIMEOUT = 300
ACTIVITY_TIMEOUT = 240

# Socket setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Global variable to track the last activity time
last_activity_time = time.time()

# Function to send data to the server
def send_data(data):
    message = DELIMITER.join(map(str, data.values()))
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message.encode(FORMAT))
    response = client.recv(1024).decode(FORMAT)
    print(response)

# Function to create a new account
def create_account():
    username = input("Enter username: ")
    password = input("Enter password: ")
    data = {'action': 'create_account', 'username': username, 'password': password}
    send_data(data)

# Function to log in
def login():
    global last_activity_time
    username = input("Enter username: ")
    password = input("Enter password: ")
    data = {'action': 'login', 'username': username, 'password': password}
    send_data(data)
    last_activity_time = time.time()

# Function to log out
def logout():
    data = {'action': 'logout'}
    send_data(data)

# Function to get seller rating
def get_seller_rating():
    sellerID = input("Enter Seller ID: ")
    data = {'action': 'get_seller_rating', 'sellerID': sellerID}
    send_data(data)

# Function to search for items for sale
def search_item_for_sale():
    global last_activity_time
    item_category = input("Enter item category: ")
    keywords = input("Enter keywords (comma-separated): ").split(',')
    data = {'action': 'search_item_for_sale', 'item_category': item_category,
            'keywords': ','.join(keywords)}
    send_data(data)
    last_activity_time = time.time()

# Function to add items to the cart
def add_to_cart():
    global last_activity_time
    prodID = input('Enter Product ID:')
    prodQuant = input('Enter Quantity to purchase:')
    data = {'action': 'add_to_cart', 'prodID': prodID, 'prodQuant': prodQuant}
    send_data(data)
    last_activity_time = time.time()

# Function to remove an item from the cart
def remove_item_from_cart():
    global last_activity_time
    item_id = input("Enter item ID: ")
    data = {'action': 'remove_item_from_cart', 'item_id': item_id}
    send_data(data)
    last_activity_time = time.time()

# Function to clear the cart
def clear_cart():
    global last_activity_time
    data = {'action': 'clear_cart'}
    send_data(data)
    last_activity_time = time.time()

# Function to display items in the cart
def display_items_in_cart():
    global last_activity_time
    data = {'action': 'display_items_in_cart'}
    send_data(data)
    last_activity_time = time.time()

# Function to provide feedback
def provide_feedback():
    global last_activity_time
    sellerID = input("Enter sellerID: ")
    feedback = input("Enter feedback (1/0): ")
    data = {'action': 'provide_feedback', 'sellerID': sellerID, 'feedback': feedback}
    send_data(data)
    last_activity_time = time.time()

# Function to get purchase history
def get_purchase_history():
    global last_activity_time
    data = {'action': 'get_purchase_history'}
    send_data(data)
    last_activity_time = time.time()

# Function to buy items in the cart
def buy_cart():
    global last_activity_time
    data = {'action': 'buy_cart'}
    send_data(data)
    last_activity_time = time.time()

# Function to save the cart
def save_cart():
    global last_activity_time
    data = {'action': 'save_cart'}
    send_data(data)
    last_activity_time = time.time()

# Function to check user activity
def check_user_activity():
    global last_activity_time
    while True:
        if keyboard.is_pressed('Enter'):
            last_activity_time = time.time()
        time.sleep(1)

# Start the user activity monitoring thread
activity_thread = Thread(target=check_user_activity)
activity_thread.daemon = True
activity_thread.start()

# Function to check session timeout
def check_session_timeout():
    global last_activity_time
    while True:
        if time.time() - last_activity_time > ACTIVITY_TIMEOUT:
            print("No activity for 4 minutes. Session will be terminated in 1 minute.")
            time.sleep(SESSION_TIMEOUT - ACTIVITY_TIMEOUT)
            print("Session terminated.")
            logout()
            break
        time.sleep(1)

# Start the session timeout monitoring thread
timeout_thread = Thread(target=check_session_timeout)
timeout_thread.daemon = True
timeout_thread.start()

# Main interface function
def interface():
    while True:
        print("****Welcome to the E-Market Place****")
        print("\nBuyer Options:")
        print("1. Create Account")
        print("2. Login")
        print("3. Logout")
        print("4. Get Seller Rating")
        print("5. Search for items")
        print("6. Add items")
        print("7. Remove items")
        print("8. Show cart")
        print("9. Buy cart")
        print("10. Clear cart")
        print("11. Save Cart")
        print("12. Display purchase history")
        print("13. Provide feedback")
        print("14. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            login()
        elif choice == '3':
            logout()
            break
        elif choice == '4':
            get_seller_rating()
        elif choice == '5':
            search_item_for_sale()
        elif choice == '6':
            add_to_cart()
        elif choice == '7':
            remove_item_from_cart()
        elif choice == '8':
            display_items_in_cart()
        elif choice == '9':
            buy_cart()
        elif choice == '10':
            clear_cart()
        elif choice == '11':
            save_cart()
        elif choice == '12':
            get_purchase_history()
        elif choice == '13':
            provide_feedback()
        elif choice == '14':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 14.")

# Run the interface function
interface()
