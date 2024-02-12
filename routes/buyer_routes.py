import socket

FORMAT = 'utf-8'
DISCONNECT_MSG = '[DISCONNECTED]'
DELIMITER = '|'

class BuyerRoutes:
    def __init__(self):
        self.PORT = 5053
        self.SERVER = '10.0.0.208'
        self.ADDR = (self.SERVER, self.PORT)
    
    def connect(self):
        back_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        back_conn.connect(self.ADDR)
        return back_conn
    
    def _send_data(self, data):
        ssock = self.connect()
        message = DELIMITER.join(data)
        print("from frontend", message)
        #self.back_conn.send(send_len)
        ssock.send(message.encode(FORMAT))
        response = ssock.recv(1024).decode(FORMAT)
        #ssock.sendall(str(response).encode(FORMAT))
        #ssock.close()
        return response, ssock
    
    def create_buyer(self, buyer): #create account checked
        response, ssock = self._send_data(buyer)
        ssock.close()
        return response

    def get_buyer_id(self, buyer):
        response, ssock = self._send_data(buyer)
        ssock.close()
        return response

    def get_seller_rating(self, Id): #checked
        response, ssock = self._send_data(Id)
        ssock.close()
        return response
    
    # provide feedback takes in a list of items, and updates the feedback of each items sellers individually after grouping by seller id
    def provide_feedback(self, items): #checked
        pass
                
    def add_items_cart(self, items, buyer_id): # items must be a list of dicts where each dict has {'id': quantity} checked
        pass

    def remove_items_cart(self, items, buyer_id): #checked
        pass

    def get_available_items(self, search): 
        response, ssock = self._send_data(search)
        ssock.close()
        return response
    
    def get_cart(self, buyer_id): #checked
        pass
        
    def save_cart(self, cart, buyer_id): # cart is a list of product id strings checked
        pass
    
    def delete_cart(self, cartId): #checked
        self.cust_db.delete_cart(cartId)
    
    def make_purchase_from_db(self, buyerID): #checked
        pass
        
    def make_purchase_from_cart(self, cart, buyer_id): #checked
        pass

    def get_history(self, BuyerId): #checked
        pass