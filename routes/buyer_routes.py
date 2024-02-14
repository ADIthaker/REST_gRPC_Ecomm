import sys
import os
from dotenv import load_dotenv
load_dotenv(override=True)

sys.path.append(os.environ.get("DIR"))
import grpc_pb2.buyer_pb2_grpc as buyer_pb2_grpc
import grpc_pb2.buyer_pb2 as buyer_pb2
import time
import grpc

class BuyerRoutes:
    def __init__(self, connection="localhost:5053"):
        self.channel = grpc.insecure_channel(connection)
        self.stub = buyer_pb2_grpc.BuyStub(self.channel)
    
    def create_buyer(self, buyer): #create account checked
        create_buyer_request = buyer_pb2.Buyer(
            username = buyer['name'], 
            pwd = buyer['password'],
            id = "",
            items = buyer["items"],
            )
        reply = self.stub.CreateAccount(create_buyer_request)
        return reply

    def get_buyer_id(self, buyer):
        getId_request = buyer_pb2.Login(name=buyer['name'], password=buyer['pwd'])
        reply = self.stub.GetUserID(getId_request)
        return reply

    def get_seller_rating(self, id): #checked
        getId_request = buyer_pb2.UserID(id=id)
        reply = self.stub.GetSellerRating(getId_request)
        #grpc does not send values with 0, so reduce the count of both feedback by 1
        return reply
    
    def get_available_items(self, search): 
        display_items_request = buyer_pb2.Search(category = search['category'], keywords=search["keywords"])
        reply = self.stub.GetAvailableItems(display_items_request)
        return reply

    def add_items_cart(self, items, buyer_id): # items must be a list of dicts where each dict has {'id': quantity} checked
        cart_req = buyer_pb2.Cart()
        cart_req.buyerId = buyer_id
        for i in items.keys():
            cart_req.ids.append(buyer_pb2.ItemId(id=i))
        for i in items.values():
            cart_req.quantities.append(buyer_pb2.Quantity(q=i))
        reply = self.stub.AddItems(cart_req)
        return reply

    def remove_items_cart(self, items, buyer_id): #checked
        cart_req = buyer_pb2.Cart()
        cart_req.buyerId = buyer_id
        for i in items.keys():
            cart_req.ids.append(buyer_pb2.ItemId(id=i))
        for i in items.values():
            cart_req.quantities.append(buyer_pb2.Quantity(q=i))
        reply = self.stub.RemoveItems(cart_req)
        return reply
    
    def get_cart(self, buyer_id): #checked
        get_cart_req = buyer_pb2.UserID(id=buyer_id)
        reply = self.stub.GetCart(get_cart_req)
        return reply

    def save_cart(self, cart, buyer_id): # cart is a list of product id strings checked
        cart_req = buyer_pb2.Cart()
        cart_req.buyerId = buyer_id
        for i in cart.keys():
            cart_req.ids.append(buyer_pb2.ItemId(id=i))
        for i in cart.values():
            cart_req.quantities.append(buyer_pb2.Quantity(q=i))
        reply = self.stub.SaveCart(cart_req)
        return reply
    
    def delete_cart(self, buyerId): #checked
        del_cart_req = buyer_pb2.UserID(id=buyerId)
        reply = self.stub.DeleteCart(del_cart_req)
        return reply
    
    # provide feedback takes in a list of items, and updates the feedback of each items sellers individually after grouping by seller id
    def provide_feedback(self, feedbacks): #checked
        ser_feedbacks = buyer_pb2.Feedbacks()
        for f in feedbacks:
            ser_feedbacks.fb.append(buyer_pb2.Feedback(sellerId=f['sellerId'], feedback=f['feedback']))
        reply = self.stub.ProvideFeedback(ser_feedbacks)
        return reply
                
    def get_history(self, BuyerId): #checked
        pass
 
if __name__ == '__main__':
    routes = BuyerRoutes()
    item = {
        "name": "grpc_bat",
        "price": 120,
        "quantity": 35,
        "category": 2,
        "keywords": "cricket",
        "cond": 1,
        "sellerId": "9ed08f75cb5911eeba0ad5a73ad3607d"
    }
    remove_item = {
        'id': "d83cf3aecb5e11eea0e7d5a73ad3607d2",
        'sellerId': "9ed08f75cb5911eeba0ad5a73ad3607d",
        'quantity': 20
    }
    #print(routes.create_buyer({"name": "grpc_A","password":"213","items": 0}))
    #print(routes.get_buyer_id({"name":"grpc_A", "pwd": "213"}))
    #print("Output", routes.get_seller_rating("9ed08f75cb5911eeba0ad5a73ad3607d"))
    #print(routes.get_available_items({"category":2, "keywords":"crick"}))
    #print(routes.save_cart({"d83cf3aecb5e11eea0e7d5a73ad3607d2": 20, "54f3e2c9cb6111eea788d5a73ad3607d2": 20}, "0977a40ccb7011eeaeecd5a73ad3607d"))
    #print(routes.add_items_cart({"d83cf3aecb5e11eea0e7d5a73ad3607d2": 10, "54f3e2c9cb6111eea788d5a73ad3607d2": 10}, "0977a40ccb7011eeaeecd5a73ad3607d"))
    #print(routes.remove_items_cart({"d83cf3aecb5e11eea0e7d5a73ad3607d2": 15, "54f3e2c9cb6111eea788d5a73ad3607d2": 15}, "0977a40ccb7011eeaeecd5a73ad3607d"))
    #print(routes.get_cart("0977a40ccb7011eeaeecd5a73ad3607d"))
    #print(routes.delete_cart("0977a40ccb7011eeaeecd5a73ad3607d"))
    #print(routes.get_purchase_history("0977a40ccb7011eeaeecd5a73ad3607d"))
    '''
    print(routes.provide_feedback([{
        "name": "grpc_bat",
        "price": 120,
        "quantity": 35,
        "category": 2,
        "keywords": "cricket",
        "cond": 1,
        "sellerId": "9ed08f75cb5911eeba0ad5a73ad3607d",
        "feedback":1,
    }, {
        "name": "grpc_bat",
        "price": 120,
        "quantity": 35,
        "category": 2,
        "keywords": "cricket",
        "cond": 1,
        "sellerId": "9ed08f75cb5911eeba0ad5a73ad3607d",
        "feedback":0,
    }]))
    '''
    
    
  