import socket
import keyboard
import time
from threading import Thread

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = '10.0.0.208'
ADDR = (SERVER, PORT)
DISCONNECTED_MSG = '[DISCONNECTED]'
DELIMITER = '|'
SESSION_TIMEOUT = 300
ACTIVITY_TIMEOUT = 240

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

last_activity_time = time.time()

def send_data(data):
    message = DELIMITER.join(map(str, data.values()))
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message.encode(FORMAT))
    response = client.recv(1024).decode(FORMAT)
    print(response)

def create_account():
    username = input("Enter username: ")
    password = input("Enter password: ")
    data = {'action': 'create_account', 'username': username, 'password': password}
    send_data(data)

def login():
    global last_activity_time
    username = input("Enter username: ")
    password = input("Enter password: ")
    data = {'action': 'login', 'username': username, 'password': password}
    send_data(data)
    last_activity_time = time.time()

def logout():
    data = {'action': 'logout'}
    send_data(data)

def get_seller_rating():
    data = {'action': 'get_seller_rating'}
    send_data(data)

def put_item_for_sale():
    global last_activity_time
    item_name = input("Enter item name: ")
    item_category = input("Enter item category: ")
    keywords = input("Enter keywords (comma-separated): ").split(',')
    condition = input("Enter condition (New(1)/Used(0)): ")
    sale_price = input("Enter sale price: ")
    quantity = input("Enter quantity: ")
    data = {'action': 'put_item_for_sale', 'item_name': item_name, 'item_category': item_category,
            'keywords': ','.join(keywords), 'condition': condition, 'sale_price': sale_price, 'quantity': quantity}
    send_data(data)
    last_activity_time = time.time()

def change_sale_price():
    global last_activity_time
    item_id = input("Enter item ID: ")
    new_sale_price = int(input("Enter new sale price: "))
    data = {'action': 'change_sale_price', 'item_id': item_id, 'new_sale_price': new_sale_price}
    send_data(data)
    last_activity_time = time.time()

def remove_item_from_sale():
    global last_activity_time
    item_id = input("Enter item ID: ")
    item_quant = int(input("Enter item quantity:"))
    data = {'action': 'remove_item_from_sale', 'item_id': item_id, 'item_quantity': item_quant}
    send_data(data)
    last_activity_time = time.time()

def display_items_on_sale():
    global last_activity_time
    data = {'action': 'display_items_on_sale'}
    send_data(data)
    result = client.recv(4096).decode(FORMAT)
    print(result)
    last_activity_time = time.time()

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

def interface():
    while True:
        print("\n****Welcome to the E-Market Place****")
        print("\nSeller Options:")
        print("1. Create Account")
        print("2. Login")
        print("3. Logout")
        print("4. Get Seller Rating")
        print("5. Put Item for Sale")
        print("6. Change Sale Price")
        print("7. Remove Item from Sale")
        print("8. Display Items on Sale")
        print("9. Exit")

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
            put_item_for_sale()
        elif choice == '6':
            change_sale_price()
        elif choice == '7':
            remove_item_from_sale()
        elif choice == '8':
            display_items_on_sale()
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

interface()
