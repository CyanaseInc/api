# # from rave_python import Rave, RaveExceptions
# # try:
# #     rave = Rave("FLWPUBK_TEST-955232eaa38c733225e42cee9597d1ca-X", "FLWSECK_TEST-ce0f1efc8db1d85ca89adb75bbc1a3c8-X", usingEnv = False)

# #     res = rave.Transfer.initiate({
# #     "account_bank": "UG16000",
# #     "account_number": "3202487774",
# #     "amount": 50000,
# #     "narration": "New transfer",
# #     "currency": "UGX",
# #     "beneficiary_name": "Mali Patricia"
# #     })

# #     # res2 = rave.Transfer.bulk({
# #     #     "title": "test",
# #     #     "bulk_data":[
# #         # {
# #         #     "Ban":"044",
# #         #     "Account Number": "0690000032",
# #         #     "Amount":500,
# #         #     "Currency":"NGN",
# #         #     "Narration":"Bulk transfer 1",
# #         #     "reference": "mk-82973029"
# #         # },
# #         # {
# #         #     "Bank":"044",
# #         #     "Account Number": "0690000034",
# #         #     "Amount":500,
# #         #     "Currency":"NGN",
# #         #     "Narration":"Bulk transfer 2",
# #         #     "reference": "mk-283874750"
# #         # }
# #     #     ]
# #     # })
    
    
# # #     for international transfers
# # #      "meta": [
# # #     {
# # #       "AccountNumber": "09182972BH",
# # #       "RoutingNumber": "0000000002993",
# # #       "SwiftCode": "ABJG190",
# # #       "BankName": "BANK OF AMERICA, N.A., SAN FRANCISCO, CA",
# # #       "BeneficiaryName": "Mark Cuban",
# # #       "BeneficiaryAddress": "San Francisco, 4 Newton",
# # #       "BeneficiaryCountry": "US"
# # #     }
# # # ]
# #     print(res)

# #     balanceres = rave.Transfer.getBalance("UGX")
# #     print(balanceres)

# # except RaveExceptions.IncompletePaymentDetailsError as e:
# #     print(e)

# # except RaveExceptions.InitiateTransferError as e:
# #     print(e.err)

# # except RaveExceptions.TransferFetchError as e:
# #     print(e.err)

# # except RaveExceptions.ServerError as e:
# #     print(e.err)
    
# # # {
# # #     'error': False, 
# # #     'returnedData': 
# # #     {'status': 'success', 
# # #       'message': 'Transfer retry attempts retrieved.', 
# # #       'data': [
# # #           {'id': 169681, 
# # #            'account_number': '0690000044', 
# # #            'bank_code': '044', 
# # #            'bank_name': 'ACCESS BANK NIGERIA', 
# # #            'fullname': 'Mercedes Daniel', 
# # #            'currency': 'NGN', 
# # #            'debit_currency': None, 
# # #            'amount': 500, 
# # #            'fee': 10.75, 
# # #            'status': 'FAILED', 
# # #            'reference': 'SampleTransfer4_PMCK_ST_FDU_1_RETRY_1', 
# # #            'narration': 'Test_Transfer_for_new_features', 
# # #            'complete_message': 'DISBURSE FAILED: Transfer failed. Please contact support', 
# # #            'meta': None, 
# # #            'requires_approval': 0, 
# # #            'is_approved': 1, 
# # #            'date_created': '2021-02-19T15:56:57.000Z'
# # #             }
# # #         ]
# # #     }
# # # }

# {
#     'error': False, 
#     'id': 414717, 
#     'data': {
#         'id': 414717, 
#         'account_number': '0690000044', 
#         'bank_code': 'MPS', 
#         'fullname': 'Giramia Patricia', 
#         'date_created': '2023-07-24T12:03:40.000Z', 
#         'currency': 'UGX', 
#         'amount': 3000, 
#         'fee': 500, 
#         'status': 'NEW', 
#         'reference': 'MC-1690200218443', 
#         'meta': [
#             {
#                 'MobileNumber': '254112187'
#             }
#         ], 
#         'narration': 'Withdraw', 
#         'complete_message': '', 
#         'requires_approval': 0, 
#         'is_approved': 1, 
#         'bank_name': 'Mobile Money'
#     }
# }
# {
#     'error': False, 
#     'returnedData': {
#         'status': 'success', 
#         'message': 'WALLET-BALANCE', 
#         'data': {
#             'Id': 2474774, 
#            'ShortName': 'UGX', 
#             'WalletNumber': '11241401068408', 
#             'AvailableBalance': 0
#         }
#     }
# }

# amount
# : 
# 405.6
# charge_response_code
# : 
# "00"
# charge_response_message
# : 
# "Please enter the OTP sent to your mobile number 080****** and email te**@rave**.com"
# charged_amount
# : 
# 422
# created_at
# : 
# "2023-07-24T13:01:19.000Z"
# currency
# : 
# "UGX"
# customer
# : 
# {name: 'Giramia Patricia', email: 'giramiapatricia61@gmail.com', phone_number: undefined}
# flw_ref
# : 
# "FLW-MOCK-7fee39e1065ad2a41e5b463dc23cb62c"
# redirectstatus
# : 
# undefined
# status
# : 
# "successful"
# transaction_id
# : 
# 4482404
# tx_ref
# : 
# "CYANASE-TEST-001"