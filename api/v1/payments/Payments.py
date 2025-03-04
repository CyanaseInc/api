# All Things related to modules
from datetime import datetime
from django.core.validators import validate_email
from django.core.paginator import Paginator
from django.utils import timezone
from api.helper import helper, webconfig
from api.config import webconfig
from api.models import *
from django.db.models import Count
from django.db.models import Q
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from api.v1.locale.Locale import Locale
import math
# helper class
# master module class
class Payments:
    #############################
    def __init__(self):
        self.help = helper.Helper()
        self.locale = Locale()
    ######################################

    def getAllSupportedPayments(self, request, lang):
        #print(keyword)
        detected_country = self.locale.detectCurrentCountry(request, lang)
        isocode = detected_country["geoplugin_countryCode"] if not (detected_country == None) and detected_country["geoplugin_countryCode"] == "UG"  else "all"
        all = self.locale.getCountryByISOCode(request, lang, "all")
        country = self.locale.getCountryByISOCode(request, lang, isocode.lower())
        all_country_id = all["id"]
        detected_country_id = country["id"]
        results = []
        payments = RegionalPaymentType.objects.filter(Q(country=SupportedCountry(pk=all_country_id)) | Q(country=SupportedCountry(pk=int(detected_country_id)))).filter(is_disabled=False).order_by("-sort_value")
        for payment in payments:
            paymenttypeid = payment.payment_type.pk
            regional_payment = self.getPaymentById(request, lang, paymenttypeid)
            option_list = []
            payment_options =  self.getSupportedPaymentOptions(request, lang, paymenttypeid, all_country_id, detected_country_id)
            for payment_option in payment_options:
                 option_list.append(payment_option["code_name"])
            regional_payment["options"] = payment_options
            regional_payment["option_list"] = option_list
            regional_payment["payment_options"] = ", ".join(option_list)
            results.append(regional_payment)
        return results
    
    def getSupportedPaymentOptions(self, request, lang, paymenttypeid, all_country_id, detected_country_id):
        #print(keyword)
        results = []
        payment_options = PaymentOptionSupport.objects.filter(payment_type=PaymentType(pk=int(paymenttypeid))).filter(Q(country=SupportedCountry(pk=all_country_id)) | Q(country=SupportedCountry(pk=int(detected_country_id)))).filter(is_disabled=False)
        for payment_option in payment_options:
            results.append(self.getPaymentOptionById(request, lang, payment_option.payment_option.pk))
        return results
    
        ##################
    def getAllPayments(self, request, lang):
        #print(keyword)
        results = []
        payments = PaymentType.objects.filter(is_disabled=False).order_by("-sort_value")
        for payment in payments:
            payment_name = getattr(payment, f"{lang}_payment_name")
            results.append({
                "id": payment.pk,
                "payment_name": payment_name,
                "code_name": payment.code_name,
                "payment_logo": payment.payment_logo,
                "settings": self.getPaymentSettings(request, lang, payment.pk),
                "sort_value": payment.sort_value,
                "has_standarded_charge": payment.has_standarded_charge,
                "payment_charge": payment.payment_charge,
                "charge_in_percentage": payment.charge_in_percentage,
                "charge_fees_on_user": payment.charge_fees_on_user,
                "is_disabled": payment.is_disabled,
                "is_default": payment.is_default,
                "created": payment.created,
                "has_been_modified": payment.has_been_modified
            })
        return results

    def getPaymentMedthodById(self, request, lang, paymentmethodid):
        #print(keyword)
        payment_method = PaymentMethod.objects.filter(pk=int(paymentmethodid)).get()
        payment_method_name = getattr(payment_method, f"{lang}_payment_method_name")
        return {
            "id": payment_method.pk,
            "payment_method_name": payment_method_name,
            "code_name": payment_method.code_name,
            "is_disabled": payment_method.is_disabled,
            "is_default": payment_method.is_default,
            "created": payment_method.created
        }
    
    def getAllPaymentMedthods(self, request, lang):
        #print(keyword)
        results = []
        payment_methods = PaymentMethod.objects.filter(is_disabled=False)
        for payment_method in payment_methods:
            payment_method_name = getattr(payment_method, f"{lang}_payment_method_name")
            results.append({
                "id": payment_method.pk,
                "payment_method_name": payment_method_name,
                "code_name": payment_method.code_name,
                "is_disabled": payment_method.is_disabled,
                "is_default": payment_method.is_default,
                "created": payment_method.created
            })
        return results
    
    def getAllPaymentOptions(self, request, lang):
        #print(keyword)
        results = []
        payment_options = PaymentOption.objects.filter(is_disabled=False)
        for payment_option in payment_options:
            payment_option_name = getattr(payment_option, f"{lang}_payment_option_name")
            results.append({
                "id": payment_option.pk,
                "payment_option_name": payment_option_name,
                "payment_option_logo": payment_option.payment_option_logo,
                "payment_method": self.getPaymentMedthodById(request, lang, payment_option.payment_method.pk),
                "fields": self.getPaymentOptionFileds(request, lang, payment_option.pk),
                "settings": self.getPaymentOptionSettings(request, lang, payment_option.pk),
                "sort_value": payment_option.sort_value,
                "code_name": payment_option.code_name,
                "has_standarded_charge": payment_option.has_standarded_charge,
                "payment_charge": payment_option.payment_charge,
                "charge_in_percentage": payment_option.charge_in_percentage,
                "charge_fees_on_user": payment_option.charge_fees_on_user,
                "has_pre_inputs": payment_option.has_pre_inputs,
                "is_default": payment_option.is_default,
                "is_disabled": payment_option.is_disabled,
                "created": payment_option.created,
            })
        return results
    

    def getPaymentOptionById(self, request, lang, paymentoptionid):
        #print(keyword)
        payment_option = PaymentOption.objects.filter(pk=int(paymentoptionid)).get()
        payment_option_name = getattr(payment_option, f"{lang}_payment_option_name")
        return {
            "id": payment_option.pk,
            "payment_option_name": payment_option_name,
            "payment_option_logo": payment_option.payment_option_logo,
            "code_name": payment_option.code_name,
            "payment_method": self.getPaymentMedthodById(request, lang, payment_option.payment_method.pk),
            "fields": self.getPaymentOptionFileds(request, lang, payment_option.pk),
            "settings": self.getPaymentOptionSettings(request, lang, payment_option.pk),
            "sort_value": payment_option.sort_value,
            "has_standarded_charge": payment_option.has_standarded_charge,
            "payment_charge": payment_option.payment_charge,
            "charge_in_percentage": payment_option.charge_in_percentage,
            "charge_fees_on_user": payment_option.charge_fees_on_user,
            "has_pre_inputs": payment_option.has_pre_inputs,
            "is_default": payment_option.is_default,
            "is_disabled": payment_option.is_disabled,
            "created": payment_option.created
        }
    
    def getPaymentOptionFileds(self, request, lang, paymentoptionid):
        fields = []
        payment_option_fields = PaymentOptionField.objects.filter(payment_option=PaymentOption(pk=int(paymentoptionid)))
        for payment_option_field in payment_option_fields:
            entry_name = getattr(payment_option_field, f"{lang}_entry_name")
            fields.append({
                "id": payment_option_field.pk,
                "entry_name": entry_name,
                "entry_code_name": payment_option_field.entry_code_name,
                "has_entry_value": payment_option_field.has_entry_value,
                "entry_value": payment_option_field.entry_value,
                "is_a_float": payment_option_field.is_a_float,
                "is_a_int": payment_option_field.is_a_int,
                "is_a_string": payment_option_field.is_a_string,
                "is_required": payment_option_field.is_required,
                "is_default": payment_option_field.is_default,
                "is_active": payment_option_field.is_active,
                "is_disabled": payment_option_field.is_disabled,
                "created": payment_option_field.created
            })
        return fields
    

    def getPaymentOptionSettings(self, request, lang, paymentoptionid):
        fields = {}
        payment_option_fields = PaymentOptionSetting.objects.filter(payment_option=PaymentOption(pk=int(paymentoptionid)))
        for payment_option_field in payment_option_fields:
            fields[payment_option_field["entry_code_name"]] = payment_option_field["entry_value"]
        return fields
        
    def getPaymentById(self, request, lang, paymentid):
        #print(keyword)
        payment = PaymentType.objects.filter(pk=int(paymentid)).get()
        payment_name = getattr(payment, f"{lang}_payment_name")
        return {
            "id": payment.pk,
            "payment_name": payment_name,
            "code_name": payment.code_name,
            "payment_logo": payment.payment_logo,
            "settings": self.getPaymentSettings(request, lang, paymentid),
            "sort_value": payment.sort_value,
            "has_standarded_charge": payment.has_standarded_charge,
            "payment_charge": payment.payment_charge,
            "charge_in_percentage": payment.charge_in_percentage,
            "charge_fees_on_user": payment.charge_fees_on_user,
            "is_disabled": payment.is_disabled,
            "is_default": payment.is_default,
            "created": payment.created,
            "has_been_modified": payment.has_been_modified
        }

    def getPaymentSettings(self, request, lang, paymentid):
        #print(keyword)
        results = {}
        payment_settings = PaymentTypeSetting.objects.filter(payment_type=PaymentType(pk=paymentid)).filter(is_disabled=False)
        for payment_setting in payment_settings:
            entry_name = getattr(payment_setting, f"{lang}_entry_name")
            results[payment_setting.entry_code_name] = payment_setting.entry_value
        return results