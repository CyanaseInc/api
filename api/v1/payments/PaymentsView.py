from django.shortcuts import render
# Create your views here.
from .Payments import Payments
from django.shortcuts import render, HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from api.v1.helper.helper import Helper
import json

DEFAULT_LANG = "en"

# init module class
_payments = Payments()
_helper = Helper()

class getAllPayments(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        payments = _payments.getAllSupportedPayments(request, lang)
        return Response(payments)


class getPaymentsById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    # Request
    def get(self, request, lang, paymentid):
        lang = DEFAULT_LANG if lang == None else lang 
        if not str(paymentid):
            return Response({
                'message': "Incomplete data request",
                'success': False
                }, status=400)
        response = _payments.getPaymentById(request, lang, paymentid)
        return Response(response)