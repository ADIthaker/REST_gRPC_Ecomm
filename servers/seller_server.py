import sys
sys.path.append('C:\\Users\\athak\\Desktop\\Documents\\CUB\\SEM2\\Distributed Systems\\CSCI5673_Distributed_Systems\\AssignmentOne')
# Added the above import cause I was facing ModuleImportError
import socket
import threading
from threading import local
from routes.seller_routes import SellerRoutes
# from utils.database import ProductDatabase, CustomerDatabase

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = '[DISCONNECTED]'
DELIMITER = '|'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Local thread initialization
thread_local = local()

# def get_thread_local_custdb():
#     # Function to get or create a thread-local customer database
#     if not hasattr(thread_local, "cust_db"):
#         thread_local.cust_db = CustomerDatabase()
#     return thread_local.cust_db

# def get_thread_local_proddb():
#     # Function to get or create a thread-local product database
#     if not hasattr(thread_local, "prod_db"):
#         thread_local.prod_db = ProductDatabase()
#     return thread_local.prod_db

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    username = None  # Track the logged-in user
    UserId = None

    # Get a thread-local cursor
    #api_handler = SellerAPIs(get_thread_local_custdb(), get_thread_local_proddb())
    route_handler = SellerRoutes()
    while connected:
        msg = conn.recv(1024).decode(FORMAT)

        # If the received message is empty, the client has disconnected
        if not msg:
            print(f'[CONNECTION CLOSED] {addr} disconnected.')
            break

        # Split the received message using the delimiter
        parts = msg.split(DELIMITER)
        action = parts[0]

        # Handling different actions
        if action == 'create_account':
            #seller = create_account(conn, parts[1], parts[2])
            res = route_handler.create_seller(parts)
            conn.sendall(res.encode(FORMAT))

        elif action == 'login':
            seller = login(conn, parts[1], parts[2])
            result = route_handler.get_seller_id(parts)
            print(result)
            if result != "False":
                username = seller['name']
                UserId = result
                print(f'{username} {UserId} has logged in')
                conn.sendall(f'Login successful! Welcome {username}'.encode(FORMAT))
            else:
                conn.sendall('Username or Password invalid! Re-try.'.encode(FORMAT))
                print(f'Invalid credentials entered by {addr}')
        elif action == 'logout':
            logout(conn, username)
            username = None
            UserId = None
            connected = False  #Set connected to False to terminate the connection
            return
        elif action == 'get_seller_rating':
            if UserId:
                res = route_handler.get_seller_rating(['get_seller_rating', UserId])
                conn.sendall(res.encode(FORMAT))
                print(f'Feedbacks sent to {username}')
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')
        elif action == 'put_item_for_sale':
            if UserId:
                #item = list_items_for_sale(conn, parts[1], parts[2], parts[3], parts[4], parts[5], UserId, parts[6])
                parts.insert(6, UserId)
                print(parts)
                result = route_handler.put_item_for_sale(parts)
                conn.sendall(f'Product: {parts[1]} saved. Quantity: {parts[6]}'.encode(FORMAT))
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')

        elif action == 'change_sale_price':
            if UserId:
                # print(type(prodID), type(UserId), type(price))
                parts.append(UserId)
                remove_item = route_handler.change_sale_price(parts)
                if remove_item:
                    conn.sendall(f'New price for {parts[1]}: ${parts[2]}'.encode(FORMAT))
                    print(f"Changes made to {parts[1]}")
                else:
                    conn.sendall('Failed to edit the price of the item. Provide a valid product id and price'.encode(FORMAT))
                    print("Failed change request.")
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
        elif action == 'remove_item_from_sale':
            if UserId:
                parts.append(UserId)
                # print(type(prodID), type(UserId), type(prodQuant))
                remove_item = route_handler.remove_item(parts)
                if remove_item:
                    conn.sendall(f'# {parts[2]} of {parts[1]} removed from the list'.encode(FORMAT))
                    print(f"# {parts[2]} of {parts[1]} removed from database")
                else:
                    conn.sendall('Failed to remove item. Provide a valid product id and quantity'.encode(FORMAT))
                    print("Failed remove request.")
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
        elif action == 'display_items_on_sale':
            if UserId and username:
                conn.sendall(f'\n ****{username}\'s listed products****'.encode(FORMAT))
                items = route_handler.display_items(['display_items_on_sale', UserId])
                conn.sendall(str(items).encode(FORMAT))
                print(f'Items data provided to {username} : {addr}')
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')

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
        item = {'name': Pname, 'cat': int(cat), 'keywords': keywords, 'condition': cond,
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
