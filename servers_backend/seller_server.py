import sys
sys.path.append('C:\\Users\\athak\\Desktop\\Documents\\CUB\\SEM2\\Distributed Systems\\CSCI5673_Distributed_Systems\\AssignmentOne')
# Added the above import cause I was facing ModuleImportError
import socket
import threading
from threading import local
from apis.seller_api import SellerAPIs
from utils.database import ProductDatabase, CustomerDatabase

HEADER = 64
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = '[DISCONNECTED]'
DELIMITER = '|'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Local thread initialization
thread_local = local()

def get_thread_local_custdb():
    # Function to get or create a thread-local customer database
    if not hasattr(thread_local, "cust_db"):
        thread_local.cust_db = CustomerDatabase()
    return thread_local.cust_db

def get_thread_local_proddb():
    # Function to get or create a thread-local product database
    if not hasattr(thread_local, "prod_db"):
        thread_local.prod_db = ProductDatabase()
    return thread_local.prod_db

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    username = None  # Track the logged-in user
    UserId = None

    # Get a thread-local cursor
    api_handler = SellerAPIs(get_thread_local_custdb(), get_thread_local_proddb())

    while connected:
        msg = conn.recv(1024).decode(FORMAT)

        # If the received message is empty, the client has disconnected
        if not msg:
            print(f'[CONNECTION CLOSED] {addr} disconnected.')
            break

        # Split the received message using the delimiter
        parts = msg.split(DELIMITER)
        print(parts)
        action = parts[0]

        # Handling different actions
        if action == 'create_account':
            seller = create_account(conn, parts[1], parts[2])
            api_handler.create_seller(seller)
        elif action == 'login':
            seller = login(conn, parts[1], parts[2])
            result = api_handler.get_seller_id(seller)
            conn.sendall(str(result[0]).encode(FORMAT))
        # elif action == 'logout':
        #     logout(conn, username)
        #     username = None
        #     UserId = None
        #     connected = False  # Set connected to False to terminate the connection
        #     return
        elif action == 'get_seller_rating':
            res = api_handler.get_seller_rating(parts[1])
            if res is not None:
                conn.sendall(f'Positive Feedbacks: {res[0]}\nNegative Feedbacks: {res[1]}'.encode(FORMAT))
            else:
                conn.sendall(f'No feedback on user'.encode(FORMAT))
        elif action == 'put_item_for_sale':
            item = list_items_for_sale(conn, parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7])
            result = api_handler.put_item_for_sale(item)
            conn.sendall(f'Product: {parts[1]} saved. Quantity: {parts[7]}'.encode(FORMAT))
            #conn.sendall(result.encode(FORMAT))

        elif action == 'change_sale_price':
            prodID = parts[1]
            price = int(parts[2])
            UserId = parts[3]
            # print(type(prodID), type(UserId), type(price))
            remove_item = api_handler.change_sale_price(prodID, UserId, price)
            if remove_item:
                conn.sendall(f'New price for {parts[1]}: ${parts[2]}'.encode(FORMAT))
                print(f"Changes made to {parts[1]}")
            else:
                conn.sendall('Failed to edit the price of the item. Provide a valid product id and price'.encode(FORMAT))
                print("Failed change request.")
        elif action == 'remove_item_from_sale':
            prodID = parts[1]
            prodQuant = int(parts[2])
            UserId = parts[3]
            # print(type(prodID), type(UserId), type(prodQuant))
            remove_item = api_handler.remove_item(prodID, UserId, prodQuant)
            if remove_item:
                conn.sendall(f'# {parts[2]} of {parts[1]} removed from the list'.encode(FORMAT))
                print(f"# {parts[2]} of {parts[1]} removed from database")
            else:
                conn.sendall('Failed to remove item. Provide a valid product id and quantity'.encode(FORMAT))
                print("Failed remove request.")

        elif action == 'display_items_on_sale':
            items = api_handler.display_items(parts[1]) #UserId
            result = ""
            for item in items:
                pname = item[0]
                cat = item[1]
                pId = item[2]
                keywords = item[3]
                if item[4] == 1:
                    cond = 'NEW'
                elif item[4] == 0:
                    cond = 'OLD'
                else:
                    continue
                price = item[5]
                quantity = item[7]
                result += f'\n NAME: {pname}, CATEGORY: {cat}, PRODUCT ID: {pId}, KEYWORDS: {keywords}, CONDITION: {cond}, PRICE: {price}, QUANTITY: {quantity}'
            
            conn.sendall(result.encode(FORMAT))
            print(f'Items data provided to {username} : {addr}')

    conn.close()

def create_account(conn, username, password):
    # Function to create a seller account
    seller = {'name': username, 'password': password, 'items': 0, 'PosFb': 0, 'NegFb': 0}
    conn.sendall('Account created successfully'.encode(FORMAT))
    return seller

def login(conn, username, password):
    # Function to handle seller login
    if conn:
        seller = {'name': username, 'password': password}
        return seller

def logout(conn, username):
    # Function to handle seller logout
    if username:
        conn.sendall(f'Logout successful. Goodbye, {username}!'.encode(FORMAT))
        print(f"{username} {conn} has disconnected")
    else:
        conn.sendall('You are not logged in.'.encode(FORMAT))
        print(f"{conn} Disconnected!")

def list_items_for_sale(conn, Pname, cat, keywords, cond, sale_price, seller_id, quant):
    # Function to list items for sale
    if conn:
        item = {'name': Pname, 'cat': cat, 'keywords': keywords, 'condition': cond,
                'price': sale_price, 'seller_id': seller_id, 'quantity': quant}
        conn.sendall(f'Product: {Pname} saved. Quantity:{quant}!'.encode(FORMAT))
        return item
    else:
        conn.sendall('You are not logged in.'.encode(FORMAT))

def start():
    # Function to start the server and listen for incoming connections
    server.listen()
    print(f'Server started and listening on {ADDR}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'\n[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

start()
