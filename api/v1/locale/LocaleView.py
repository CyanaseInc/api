from django.shortcuts import render
# Create your views here.
from .Locale import  Locale
from django.shortcuts import render, HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate  

DEFAULT_LANG = "en"

# init locale class
_locale = Locale()

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class SupportedLanguages(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        content =  _locale.getSupportedLanguages(request, lang)
        return Response(content)

class DefaultLanguage(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        content =  _locale.getDefaultLanguages(request, lang)
        return Response(content)


class LanguageData(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        content =  _locale.loadLanguageData(request, lang)
        return Response(content, status=200)

class UpdateDefaultLanguage(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        if not ("langid" in  request.GET):
            return Response({"message": "Incomplete data request", "status": "failed"}, status=400)
        elif not request.GET["langid"]:
            return Response({"message": "Language Id is required", "status": "failed"}, status=400)
        else:
            langid = request.GET["langid"]
            _locale.UpdateDefaultLanguage(request, lang, langid)
            return Response({"message": "Language updated succesfully", "status": "success"})


class SupportedCountries(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        content =  _locale.getSupportedCountry(request, lang)
        return Response(content)

class DefaultCountry(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        content =  _locale.getDefaultCountry(request, lang)
        return Response(content)


class UpdateDefaultCountry(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        if not ("countryid" in  request.GET):
            return Response({"message": "Incomplete data request", "status": "failed"}, status=400)
        elif not request.GET["countryid"]:
            return Response({"message": "Incomplete is required", "status": "failed"}, status=400)
        else:
            countryid = request.GET["countryid"]
            _locale.UpdateDefaultCountry(request, lang, countryid)
            return Response({"message": "Country updated succesfully", "status": "success"})

class SupportedCurrencies(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        content =  _locale.getSupportedCurrencies(request, lang)
        return Response(content)


class getCountryById(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, countryid):
        lang = DEFAULT_LANG if lang == None else lang 
        content =  _locale.getCountryById(request, lang, countryid)
        return Response(content)

class DefaultCurrency(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        content =  _locale.getDefaultCurrrecy(request, lang)
        return Response(content)

class UpdateDefaultCurrency(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        if not ("currencyid" in  request.GET):
            return Response({"message": "Incomplete data request", "status": "failed"}, status=400)
        elif not request.GET["currencyid"]:
            return Response({"message": "Incomplete is required", "status": "failed"}, status=400)
        else:
            currencyid = request.GET["currencyid"]
            _locale.UpdateDefaultCurrency(request, lang, currencyid);
            return Response({"message": "Country updated succesfully", "status": "success"})

class UpdateCurrencySettings(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        if not ("currencyid" in  request.GET):
            return Response({"message": "Incomplete data request", "status": "failed"}, status=400)
        elif not request.GET["currencyid"]:
            return Response({"message": "Incomplete is required", "status": "failed"}, status=400)
        else:
            currencyid = request.GET["currencyid"]
            _locale.UpdateDefaultCurrency(request, lang, currencyid)
            return Response({"message": "Country updated succesfully", "status": "success"})


class SupportedLanguages(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        content =  _locale.getSupportedLanguages(request, lang)
        return Response(content)


class getSupportedLanguageById(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, langid):
        lang = DEFAULT_LANG if lang == None else lang 
        content =  _locale.getLanguageById(request, lang, langid)
        return Response(content)



class DetectCountry(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        content =  _locale.detectCurrentCountry(request, lang)
        return Response(content)

class DefaultLanguage(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]
    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang == None else lang 
        content =  _locale.getDefaultLanguages(request, lang)
        return Response(content)