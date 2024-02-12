import sys
sys.path.append('C:\\Users\\athak\\Desktop\\Documents\\CUB\\SEM2\\Distributed Systems\\CSCI5673_Distributed_Systems\\AssignmentOne')

# Added the above import cause I was facing ModuleImportError
import socket
import threading
from threading import local
from routes.buyer_routes import BuyerRoutes

HEADER = 64
PORT = 5052
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
#     if not hasattr(thread_local, "cust_db"):
#         thread_local.cust_db = CustomerDatabase()
#     return thread_local.cust_db

# def get_thread_local_proddb():
#     if not hasattr(thread_local, "prod_db"):
#         thread_local.prod_db = ProductDatabase()
#     return thread_local.prod_db

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    username = None  # Track the logged-in user
    UserId = None
    cart = {}
    
    # Get a thread-local cursor
    route_handler = BuyerRoutes()

    while connected:
        msg = conn.recv(1024).decode(FORMAT)

        # If the received message is empty, the client has disconnected
        if not msg:
            print(f'[CONNECTION CLOSED] {addr} disconnected.')
            break

        # Split the received message using the delimiter
        parts = msg.split(DELIMITER)
        action = parts[0]

        if action == 'create_account':
            res = route_handler.create_buyer(parts)
            conn.sendall(res.encode(FORMAT))

        elif action == 'login':
            buyer = login(conn, parts[1], parts[2])
            result = route_handler.get_buyer_id(parts)
            if result:
                username = buyer['name']
                UserId = result
                print(f'{username} {UserId} has logged in')
                conn.sendall(f'Login successful! Welcome {username}'.encode(FORMAT))
            else:
                conn.sendall(f'Username or Password invalid! Re-try.'.encode(FORMAT))
                print(f'Invalid credentials entered by {conn} {addr}')

        elif action == 'logout':
            print(f'{addr} has disconnected')
            conn.sendall(f'Goodbye {username}!'.encode(FORMAT))
            logout(conn, username)
            username = None
            UserId = None
            connected = False  # Set connected to False to terminate the connection
            return
        
        elif action == 'get_seller_rating':
            if UserId:
                res = route_handler.get_seller_rating(parts)
                conn.sendall(res.encode(FORMAT))
                print(f'Feedbacks sent to {username}')
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')

        elif action == 'search_item_for_sale':
            if UserId:
                results = route_handler.get_available_items(parts)
                conn.sendall(str(results).encode(FORMAT))
                print(f'Product listings provided to {username} : {addr}')
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')

        elif action == 'add_to_cart':
            if UserId:
                cart[parts[1]] = int(parts[2])
                print(cart)
                conn.sendall(f'#{parts[2]} of Item {parts[1]} added to the cart!'.encode(FORMAT))
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')

        elif action == 'remove_item_from_cart':
            if UserId:
                if cart:
                    cart.pop(parts[1])
                    conn.sendall(f'{parts[1]} removed from the cart successfully'.encode(FORMAT))
                else:
                    conn.sendall(f'Cart for current session is empty. Add items and try again!'.encode(FORMAT))
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')

        elif action == 'display_items_in_cart': # Show cart
            if UserId:
                print(f"Displayed unsaved cart to {username}")
                if cart:
                    for key, values in cart.items():
                        conn.sendall(f'\nProduct: {key}, Quantity:{values}\n**UNSAVED ITEM**'.encode(FORMAT))
                else:
                    result = route_handler.get_cart(['display_items_in_cart', UserId])
                    if result:
                        for key, values in result.items():
                            print(f"Displayed saved cart(from db) to {username}")
                            conn.sendall(result.encode(FORMAT))
                    else:
                        print(f"No cart displayed")
                        conn.sendall('Your cart is empty! Consider adding items'.encode(FORMAT))
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')

        elif action == 'buy_cart':
            if UserId:
                if cart:
                    route_handler.make_purchase_from_cart(cart, UserId)
                    conn.sendall('Purchase made successfully'.encode(FORMAT))
                    print(f"{username} made purchase from unsaved cart!")
                else:
                    result = route_handler.get_cart(UserId)
                    if result:
                        route_handler.make_purchase_from_db(UserId)
                        conn.sendall('Purchase made successfully'.encode(FORMAT))
                        print(f"{username} made purchase from saved cart!")
                    else:
                        conn.sendall('Your cart is empty! Consider adding items'.encode(FORMAT))
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')

        elif action == 'clear_cart':
            if UserId:
                if cart:
                    cart.clear()
                    conn.sendall(f'Cart emptied!!'.encode(FORMAT))
                    print(f"{username} has cleared the unsaved cart!")
                else:
                    conn.sendall(f'Cart for current session is empty. Add items and try again!'.encode(FORMAT))
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')

        elif action == 'save_cart':
            if UserId:
                if cart:
                    print(cart, UserId)
                    route_handler.save_cart(cart, UserId)
                    conn.sendall(f'****{username}\'s cart is saved****\nCurrent cart emptied'.encode(FORMAT))
                    cart = cart.clear()
                    print(f"{username}\'s cart is emptied")
                else:
                    conn.sendall(f'Cart for current session is empty. Add items and try again!'.encode(FORMAT))
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')

        elif action == 'get_purchase_history':
            if UserId:
                results = route_handler.get_history(UserId)
                for result in results:
                    conn.sendall(f'You have bought\n***{result}***'.encode(FORMAT))
                print(f"Displayed purchase history to {username}")
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')

        elif action == 'provide_feedback':
            if UserId:
                sellers = []
                seller = {}
                seller['seller_id'] = parts[1]
                seller['feedback'] = int(parts[2])
                sellers.append(seller)
                route_handler.provide_feedback(sellers)
                conn.sendall('Thank you for providing feedback!'.encode(FORMAT))
            else:
                conn.sendall('You are not logged in!'.encode(FORMAT))
                print('User not logged in')


    conn.close()

def create_buyer_account(conn, username, password):
    buyer = {}
    buyer['name'] = username
    buyer['password'] = password
    buyer['items'] = 0
    conn.sendall('Account created successfully'.encode(FORMAT))
    return buyer

def login(conn, username, password):
    if conn:
        buyer = {}
        buyer['name'] = username
        buyer['password'] = password
        return buyer

# The logout function remains the same for both buyers and sellers
def logout(conn, username):
    if username:
        conn.sendall(f'Logout successful. Goodbye, {username}!'.encode(FORMAT))
        print(f"{username} {conn} has disconnected")
    else:
        conn.sendall('You are not logged in.'.encode(FORMAT))
        print(f"{conn} Disconnected!")

def search_available_items(conn, cat, keywords):
    if conn:
        items = {}
        items['cat'] = int(cat)
        items['keywords'] = keywords
        return items

def start():
    server.listen()
    print(f'Server started and listening on {ADDR}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

start()
