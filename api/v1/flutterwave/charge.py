# from rave_python import Rave, RaveExceptions, Misc
# rave = Rave("YOUR_PUBLIC_KEY", "YOUR_SECRET_KEY", usingEnv = False)

# # Payload with pin
# payload = {
#   "cardno": "5438898014560229",
#   "cvv": "890",
#   "expirymonth": "09",
#   "expiryyear": "19",
#   "amount": "10",
#   "email": "user@gmail.com",
#   "phonenumber": "0902620185",
#   "firstname": "temi",
#   "lastname": "desola",
#   "IP": "355426087298442",
# }

# try:
#     res = rave.Card.charge(payload)

#     if res["suggestedAuth"]:
#         arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

#         if arg == "pin":
#             Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
#         if arg == "address":
#             Misc.updatePayload(res["suggestedAuth"], payload, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})
        
#         res = rave.Card.charge(payload)

#     if res["validationRequired"]:
#         rave.Card.validate(res["flwRef"], "")

#     res = rave.Card.verify(res["txRef"])
#     print(res["transactionComplete"])

# except RaveExceptions.CardChargeError as e:
#     print(e.err["errMsg"])
#     print(e.err["flwRef"])

# except RaveExceptions.TransactionValidationError as e:
#     print(e.err)
#     print(e.err["flwRef"])

# except RaveExceptions.TransactionVerificationError as e:
#     print(e.err["errMsg"])
#     print(e.err["txRef"])
    
    
# (True, {'settlement_id': 'NEW', 'id': 36071, 'AccountId': 49278, 'TransactionId': 1664979, 'FlwRef': 'FLW-MOCK-62986ef948d6dd127102cdb58813d216', 'walletId': 50309, 'AmountRefunded': '5000', 'status': 'completed', 'destination': 'payment_source', 'meta': '{"source":"ledgerbalance","uniquereference":"62472228710"}', 'updatedAt': '2021-01-23T01:27:11.969Z', 'createdAt': '2021-01-23T01:27:08.672Z'})