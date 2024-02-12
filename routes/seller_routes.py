import socket

FORMAT = 'utf-8'
DISCONNECT_MSG = '[DISCONNECTED]'
DELIMITER = '|'

class SellerRoutes:
    def __init__(self):
        self.PORT = 5051
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

    def create_seller(self, seller): #create account checked
        response, ssock = self._send_data(seller)
        ssock.close()
        return response

    def get_seller_id(self, seller):
        response, ssock = self._send_data(seller)
        ssock.close()
        return response
        
    # def is_seller(self, Id): #login checked
    #     seller = self.cust_db.get_seller(Id)
    #     if seller is not None and len(seller)!=0:
    #         print(seller)
    #         return seller[0][1]
    #     else:
    #         return False

    def get_seller_rating(self, Id): #checked
        response, ssock = self._send_data(Id)
        ssock.close()
        return response
    
    def put_item_for_sale(self, item): #checked
        response, ssock = self._send_data(item)
        res = ssock.recv(1024).decode(FORMAT)
        ssock.close()
        return response
    
    def change_sale_price(self, parts): #checked
        response, ssock = self._send_data(parts)
        ssock.close()
        return response
    
    def remove_item(self, parts): #checked
        response, ssock = self._send_data(parts)
        ssock.close()
        return response
        
    def display_items(self, parts): #checked
        response, ssock = self._send_data(parts)
        ssock.close()
        return response.split(DELIMITER)
 