# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: buyer.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x62uyer.proto\x12\x03\x62uy\"U\n\x0cPurchaseCart\x12\x17\n\x04\x63\x61rt\x18\x01 \x01(\x0b\x32\t.buy.Cart\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06\x63\x61rdNo\x18\x03 \x01(\t\x12\x0e\n\x06\x65xpiry\x18\x04 \x01(\t\"K\n\nPurchaseDB\x12\x0f\n\x07\x62uyerId\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06\x63\x61rdNo\x18\x03 \x01(\t\x12\x0e\n\x06\x65xpiry\x18\x04 \x01(\t\"\'\n\x07History\x12\x1c\n\tpurchases\x18\x01 \x03(\x0b\x32\t.buy.Cart\".\n\x08\x46\x65\x65\x64\x62\x61\x63k\x12\x10\n\x08\x66\x65\x65\x64\x62\x61\x63k\x18\x01 \x01(\x05\x12\x10\n\x08sellerId\x18\x02 \x01(\t\"&\n\tFeedbacks\x12\x19\n\x02\x66\x62\x18\x01 \x03(\x0b\x32\r.buy.Feedback\"X\n\x08Purchase\x12\x0f\n\x07\x62uyerId\x18\x01 \x01(\t\x12\x18\n\x03ids\x18\x02 \x03(\x0b\x32\x0b.buy.ItemId\x12!\n\nquantities\x18\x03 \x03(\x0b\x32\r.buy.Quantity\"+\n\tPurchases\x12\x1e\n\x07history\x18\x01 \x03(\x0b\x32\r.buy.Purchase\"\'\n\x05Login\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x14\n\x06UserID\x12\n\n\x02id\x18\x01 \x01(\t\",\n\x0cSellerRating\x12\r\n\x05posFb\x18\x01 \x01(\x05\x12\r\n\x05negFb\x18\x02 \x01(\x05\"\x16\n\x08SellerId\x12\n\n\x02id\x18\x01 \x01(\t\"\x85\x01\n\x04Item\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x02 \x01(\x05\x12\r\n\x05price\x18\x03 \x01(\x05\x12\n\n\x02id\x18\x04 \x01(\t\x12\x10\n\x08keywords\x18\x05 \x01(\t\x12\x0c\n\x04\x63ond\x18\x06 \x01(\x05\x12\x10\n\x08quantity\x18\x07 \x01(\x05\x12\x10\n\x08sellerId\x18\x08 \x01(\t\"\x14\n\x06ItemId\x12\n\n\x02id\x18\x01 \x01(\t\"4\n\x07ItemIds\x12\x18\n\x03ids\x18\x01 \x03(\x0b\x32\x0b.buy.ItemId\x12\x0f\n\x07\x62uyerId\x18\x02 \x01(\t\"!\n\x05Items\x12\x18\n\x05items\x18\x01 \x03(\x0b\x32\t.buy.Item\",\n\x06Search\x12\x10\n\x08\x63\x61tegory\x18\x01 \x01(\x05\x12\x10\n\x08keywords\x18\x02 \x01(\t\"\x15\n\x08Quantity\x12\t\n\x01q\x18\x01 \x01(\x05\"T\n\x04\x43\x61rt\x12\x0f\n\x07\x62uyerId\x18\x01 \x01(\t\x12\x18\n\x03ids\x18\x02 \x03(\x0b\x32\x0b.buy.ItemId\x12!\n\nquantities\x18\x03 \x03(\x0b\x32\r.buy.Quantity\"A\n\x05\x42uyer\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0b\n\x03pwd\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12\r\n\x05items\x18\x04 \x01(\x05\",\n\x0eUpdateResponse\x12\r\n\x05\x65rror\x18\x01 \x01(\x08\x12\x0b\n\x03msg\x18\x02 \x01(\t\"-\n\x11\x44isplayItemsReply\x12\x18\n\x05items\x18\x01 \x03(\x0b\x32\t.buy.Item2\xf7\x04\n\x03\x42uy\x12\x30\n\rCreateAccount\x12\n.buy.Buyer\x1a\x13.buy.UpdateResponse\x12,\n\tGetUserID\x12\n.buy.Login\x1a\x13.buy.UpdateResponse\x12\x33\n\x0fGetSellerRating\x12\r.buy.SellerId\x1a\x11.buy.SellerRating\x12,\n\x11GetAvailableItems\x12\x0b.buy.Search\x1a\n.buy.Items\x12*\n\x08\x41\x64\x64Items\x12\t.buy.Cart\x1a\x13.buy.UpdateResponse\x12-\n\x0bRemoveItems\x12\t.buy.Cart\x1a\x13.buy.UpdateResponse\x12!\n\x07GetCart\x12\x0b.buy.UserID\x1a\t.buy.Cart\x12.\n\nDeleteCart\x12\x0b.buy.UserID\x1a\x13.buy.UpdateResponse\x12*\n\x08SaveCart\x12\t.buy.Cart\x1a\x13.buy.UpdateResponse\x12\x36\n\x0fProvideFeedback\x12\x0e.buy.Feedbacks\x1a\x13.buy.UpdateResponse\x12:\n\x10MakePurchaseCart\x12\x11.buy.PurchaseCart\x1a\x13.buy.UpdateResponse\x12\x36\n\x0eMakePurchaseDB\x12\x0f.buy.PurchaseDB\x1a\x13.buy.UpdateResponse\x12\'\n\nGetHistory\x12\x0b.buy.UserID\x1a\x0c.buy.Historyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'buyer_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PURCHASECART']._serialized_start=20
  _globals['_PURCHASECART']._serialized_end=105
  _globals['_PURCHASEDB']._serialized_start=107
  _globals['_PURCHASEDB']._serialized_end=182
  _globals['_HISTORY']._serialized_start=184
  _globals['_HISTORY']._serialized_end=223
  _globals['_FEEDBACK']._serialized_start=225
  _globals['_FEEDBACK']._serialized_end=271
  _globals['_FEEDBACKS']._serialized_start=273
  _globals['_FEEDBACKS']._serialized_end=311
  _globals['_PURCHASE']._serialized_start=313
  _globals['_PURCHASE']._serialized_end=401
  _globals['_PURCHASES']._serialized_start=403
  _globals['_PURCHASES']._serialized_end=446
  _globals['_LOGIN']._serialized_start=448
  _globals['_LOGIN']._serialized_end=487
  _globals['_USERID']._serialized_start=489
  _globals['_USERID']._serialized_end=509
  _globals['_SELLERRATING']._serialized_start=511
  _globals['_SELLERRATING']._serialized_end=555
  _globals['_SELLERID']._serialized_start=557
  _globals['_SELLERID']._serialized_end=579
  _globals['_ITEM']._serialized_start=582
  _globals['_ITEM']._serialized_end=715
  _globals['_ITEMID']._serialized_start=717
  _globals['_ITEMID']._serialized_end=737
  _globals['_ITEMIDS']._serialized_start=739
  _globals['_ITEMIDS']._serialized_end=791
  _globals['_ITEMS']._serialized_start=793
  _globals['_ITEMS']._serialized_end=826
  _globals['_SEARCH']._serialized_start=828
  _globals['_SEARCH']._serialized_end=872
  _globals['_QUANTITY']._serialized_start=874
  _globals['_QUANTITY']._serialized_end=895
  _globals['_CART']._serialized_start=897
  _globals['_CART']._serialized_end=981
  _globals['_BUYER']._serialized_start=983
  _globals['_BUYER']._serialized_end=1048
  _globals['_UPDATERESPONSE']._serialized_start=1050
  _globals['_UPDATERESPONSE']._serialized_end=1094
  _globals['_DISPLAYITEMSREPLY']._serialized_start=1096
  _globals['_DISPLAYITEMSREPLY']._serialized_end=1141
  _globals['_BUY']._serialized_start=1144
  _globals['_BUY']._serialized_end=1775
# @@protoc_insertion_point(module_scope)
