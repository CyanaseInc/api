# from rave_python import Rave, RaveExceptions, Misc
# rave = Rave("ENTER_YOUR_PUBLIC_KEY", "ENTER_YOUR_SECRET_KEY", usingEnv = False)

# # mobile payload
# payload = {
#   "amount": "50",
#   "email": "",
#   "phonenumber": "xxxxxxxx",
#   "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
#   "IP":""
# }

# try:
#   res = rave.UGMobile.charge(payload)
#   res = rave.UGMobile.verify(res["txRef"])
#   print(res)

# except RaveExceptions.TransactionChargeError as e:
#   print(e.err)
#   print(e.err["flwRef"])

# except RaveExceptions.TransactionVerificationError as e:
#   print(e.err["errMsg"])
#   print(e.err["txRef"])