# All Things related to modules
from datetime import datetime
from django.core.validators import validate_email
from django.core.paginator import Paginator
from django.utils import timezone
from pytz import country_names
from api.helper import helper
from api.config import webconfig
from api.models import  SupportedCountry, SupportedLanguage, Currency
from django.db.models import Count
from django.db.models import Q
# helper class
# master module class
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# master module class
class Locale:
    def __init__(self):
        self.help = helper.Helper()

    def getSupportedLanguages(self, request, lang):
        results = []
        languages = SupportedLanguage.objects.filter(is_disabled=False).order_by("-id")
        for language in languages:
            lang_name = getattr(language, f"{lang}_lang_name")
            lang_item = {
                "id": language.pk,
                 "lang_name": lang_name,
                 "lang_iso_code": language.lang_iso_code,
                 "is_default": language.is_default,
                 "is_disabled": language.is_disabled,
                 "has_been_modified": language.has_been_modified,
                 "last_modified": language.last_modified
            }
            results.append(lang_item)
        return results

    def loadLanguageData(self, request, lang):
        stream = open(f'media/v1/languages/{lang}_lang.yml', 'r')
        data = load(stream, Loader=Loader)
        return data

    def getDefaultLanguages(self, request, lang):
        language = SupportedLanguage.objects.filter(Q(is_disabled=False) and Q(is_default=True)).order_by("-id").get()
        lang_name = getattr(language, f"{lang}_lang_name")
        return {
                "id": language.pk,
                 "lang_name": lang_name,
                 "lang_iso_code": language.lang_iso_code,
                 "is_default": language.is_default,
                 "is_disabled": language.is_disabled,
                 "has_been_modified": language.has_been_modified,
                 "last_modified": language.last_modified
            }

    def getLanguageById(self, request, lang, langid):
        language = SupportedLanguage.objects.filter(pk=langid).get()
        lang_name = getattr(language, f"{lang}_lang_name")
        return {
                "id": language.pk,
                "lang_name": lang_name,
                "lang_iso_code": language.lang_iso_code,
                "is_default": language.is_default,
                "is_disabled": language.is_disabled,
                "has_been_modified": language.has_been_modified,
                "last_modified": language.last_modified
            }


    def UpdateDefaultLanguage(self, request, lang, langid):
        default_lang = SupportedLanguage.objects.filter(is_default=True)
        default_lang.update(is_default=False, has_been_modified=True, last_modified=self.help.getDateTime())
        newlanguage = SupportedLanguage.objects.filter(pk=langid)
        newlanguage.update(is_default=True, has_been_modified=True, last_modified=self.help.getDateTime())
        return True
    

    def detectCurrentCountry(self, request, lang):
        return self.help.getDefaultCurrency(request)

   # Countries
    def getSupportedCountry(self, request, lang):
        results = []
        countries = SupportedCountry.objects.filter(is_disabled=False)
        for country in countries:
            country_name = getattr(country, f"{lang}_coutry_name")
            country_item = {
                   "id": country.pk,
                    "country_name": country_name,
                    "country_code": country.country_code,
                    "is_default": country.is_default,
                    "is_disabled": country.is_disabled,
                    "has_been_modified": country.has_been_modified,
                    "last_modified": country.last_modified
            }
            results.append(country_item)
        return results
        
    def getDefaultCountry(self, request, lang):
        country = SupportedCountry.objects.filter(is_default=True).get()
        country_name = getattr(country, f"{lang}_coutry_name")
        return {
                "id": country.pk,
                "country_name": country_name,
                "country_code": country.country_code,
                "is_default": country.is_default,
                "is_disabled": country.is_disabled,
                "has_been_modified": country.has_been_modified,
                "last_modified": country.last_modified
                }
    
    def getCountryByISOCode(self, request, lang, isocode):
        country = SupportedCountry.objects.filter(country_code=isocode).get()
        country_name = getattr(country, f"{lang}_coutry_name")
        return {
                "id": country.pk,
                "country_name": country_name,
                "country_code": country.country_code,
                "is_default": country.is_default,
                "is_disabled": country.is_disabled,
                "has_been_modified": country.has_been_modified,
                "last_modified": country.last_modified
                }
    
    def getCountryById(self, request, lang, countryid):
        country = SupportedCountry.objects.filter(pk=countryid).get()
        country_name = getattr(country, f"{lang}_coutry_name")
        return {
                "id": country.pk,
                "country_name": country_name,
                "country_code": country.country_code,
                "is_default": country.is_default,
                "is_disabled": country.is_disabled,
                "has_been_modified": country.has_been_modified,
                "last_modified": country.last_modified
                }


    def UpdateDefaultCountry(self, request, lang, coutryid):
        default_country = SupportedCountry.objects.filter(is_default=True)
        default_country.update(is_default=False, has_been_modified=True, last_modified=self.help.getDateTime())
        newcountry = SupportedCountry.objects.filter(pk=coutryid)
        newcountry.update(is_default=True, has_been_modified=True, last_modified=self.help.getDateTime())
        return True

        # Currency
    def getSupportedCurrency(self, request, lang):
        results = []
        Currency = Currency.objects.filter(is_disabled=False).order_by("-id")
        for currency in Currency:
            # currency_locale = getattr(currency, f"{lang}_currency_locale")
            tinker_symbol =  f"{currency.currency_symbol} " if currency.is_indented else f"{currency.currency_symbol}" 
            currency_item = {
                   "id": currency.pk,
                    "currency_locale": currency.currency_locale,
                    "currency_code": currency.currency_code,
                    "currency_symbol": currency.currency_symbol,
                    "ticker_symbol": tinker_symbol,
                    "exchange_rate": currency.exchange_rate,
                    "decimal_points": currency.decimal_points,
                    "is_indented": currency.is_indented,
                    "s_infront": currency.is_infront,
                    "created": currency.created,
                    "is_default": currency.is_default,
                    "is_disabled": currency.is_disabled,
                    "has_been_modified": currency.has_been_modified,
                    "last_modified": currency.last_modified
            }
            results.append(currency_item)
        return results
        
    def getDefaultCurrrecy(self, request, lang):
        currency = Currency.objects.filter(Q(is_disabled=False) and Q(is_default=True)).order_by("-id").get()
        #country_name = getattr(currency, f"{lang}_coutry_name")
        tinker_symbol =  f"{currency.currency_symbol} " if currency.is_indented else f"{currency.currency_symbol}" 
        return {
                "id": currency.pk,
                "currency_locale": currency.currency_locale,
                "currency_code": currency.currency_code,
                "currency_symbol": currency.currency_symbol,
                "decimal_points": currency.decimal_points,
                "ticker_symbol": tinker_symbol,
                "exchange_rate": currency.exchange_rate,
                "is_indented": currency.is_indented,
                "is_infront": currency.is_infront,
                "created": currency.created,
                "is_default": currency.is_default,
                "is_disabled": currency.is_disabled,
                "has_been_modified": currency.has_been_modified,
                "last_modified": currency.last_modified
                }
    
    def getCurrrecyById(self, request, lang, currencyid):
        currency = Currency.objects.filter(pk=currencyid).get()
        tinker_symbol =  f"{currency.currency_symbol} " if currency.is_indented else f"{currency.currency_symbol}" 
        return {
                    "id": currency.pk,
                    "currency_locale": currency.currency_locale,
                    "currency_code": currency.currency_code,
                    "currency_symbol": currency.currency_symbol,
                    "ticker_symbol": tinker_symbol,
                    "exchange_rate": currency.exchange_rate,
                    "is_indented": currency.is_indented,
                    "is_infront": currency.is_infront,
                    "created": currency.created,
                    "is_default": currency.is_default,
                    "is_disabled": currency.is_disabled,
                    "has_been_modified": currency.has_been_modified,
                    "last_modified": currency.last_modified
                }
       
    def UpdateDefaultCurrency(self, request, lang, currencyid):
        default_Currency = Currency.objects.filter(is_default=True)
        default_Currency.update(is_default=False, has_been_modified=True, last_modified=self.help.getDateTime())
        newcurrency = Currency.objects.filter(pk=currencyid)
        newcurrency.update(is_default=True, has_been_modified=True,last_modified=self.help.getDateTime())
        return True

    def UpdateDefaultCurrencySettings(self, request, lang, currencyid):
        default_Currency = Currency.objects.filter(is_default=True)
        default_Currency.update(is_default=False)
        newcurrency = Currency.objects.filter(pk=currencyid)
        newcurrency.update(is_default=True)
        return True