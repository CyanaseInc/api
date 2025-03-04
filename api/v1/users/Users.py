from django.shortcuts import render, HttpResponse
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.core.validators import validate_email
from django.core.paginator import Paginator
from django.utils import timezone
from api.helper import helper
from api.config import webconfig
# from ...config import webconfig
from api.v1.mailer.Mailer import Mailer
from api.v1.locale.Locale import Locale
from api.models import *
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.models import User
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from ...models import UserProfile, InvestmentOption, InvestmentPerformance
from django.urls import resolve, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from api.helper.Cryptor import Cryptor
import os
import random

# master module class
# master module class
class Users:
    def __init__(self):
        self.help = helper.Helper()
        self.locale = Locale()
        self.mailer = Mailer()
        self.cryptor = Cryptor()
        
        #Check if user email and phone exists
    def CheckMUser(self, request, lang):
        email = request.data.get("email")
        phone = request.data.get("phone")

        response = {
        "email_exists": False,
        "phone_exists": False,
        "message": "",
        }

        try:
            if email:
                if UserProfile.objects.filter(user__email=email).exists():
                    response["email_exists"] = True
                    response["message"] = "Email already exists."

            if phone:
                if UserProfile.objects.filter(phoneno=phone).exists():
                    response["phone_exists"] = True
                    response["message"] = "Phone number already exists."

            if response["email_exists"] and response["phone_exists"]:
                response["message"] = "Both email and phone number already exist."

        except Exception as e:
            response["message"] = f"An error occurred: {str(e)}"

        return response
 
     
     
    def getAuthUser(self, request, lang):
        userid = Token.objects.get(key=request.auth).user_id
        user = User.objects.get(pk=userid)
        profile = UserProfile.objects.get(user=User(pk=userid))
        return {
            "token": str(request.auth),  # None
            "user_id": user.pk,
            "username": user.username,  # `django.contrib.auth.User` instance.
            "email": user.email,
            "is_superuser": user.is_superuser,
            "last_login": user.last_login,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile": {
                "profile_id": user.pk,
                "country": profile.country,
                # "country":  None if profile.country == None else profile.country.pk,
                "language": None if profile.language is None else profile.language.pk,
                "time_zone": None if profile.tmz is None else profile.tmz.pk,
                "gender": profile.gender,
                "phoneno": profile.phoneno,
                "user_type": profile.user_type,
                "address": profile.address,
                "birth_date": profile.birth_date,
                "profile_picture": f"{webconfig.BASE_URL}media/profile/{profile.profile_picture}",
                "verification_code": profile.verification_code,
                "is_verified": profile.is_verified,
                "is_deletable": profile.is_verified,
                "is_disabled": profile.is_disabled,
                "created": profile.created,
            },
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            "date_joined": user.date_joined,
            "message": "",
            "success": True,
        }

    def getAuthUserById(self, request, lang, userid):
        user = User.objects.get(pk=userid)
        profile = UserProfile.objects.get(user=User(pk=userid))
        token, created = Token.objects.get_or_create(user=user)
        return {
            "token": str(token.key),  # None
            "user_id": user.pk,
            "username": user.username,  # `django.contrib.auth.User` instance.
            "email": user.email,
            "is_superuser": user.is_superuser,
            "last_login": user.last_login,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile": {
                "profile_id": user.pk,
                "country": profile.country,
                # "country":  None if profile.country == None else profile.country.pk,
                "language": None if profile.language is None else profile.language.pk,
                "time_zone": None if profile.tmz is None else profile.tmz.pk,
                "gender": profile.gender,
                "phoneno": profile.phoneno,
                "address": profile.address,
                "birth_date": profile.birth_date,
                "profile_picture": f"{webconfig.API_URL}media/profile/{profile.profile_picture}",
                "verification_code": profile.verification_code,
                "is_verified": profile.is_verified,
                "is_deletable": profile.is_verified,
                "is_disabled": profile.is_disabled,
                "created": profile.created,
                "passcode": profile.passcode
            },
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            "date_joined": user.date_joined,
            "message": "",
            "success": True,
        }

    def getAuthUserByEmail(self, request, lang, username):
        try:
            # Try to get the user by email
            user = User.objects.filter(email=username).first() or User.objects.filter(userprofile__phoneno=username).first()
        except User.DoesNotExist:
        # If user doesn't exist, return a failure response
            return {"success": False, "message": "User with this email does not exist."}

        try:
        # Try to get the user profile associated with the user
            profile = UserProfile.objects.get(user=User(pk=user.pk))
        except UserProfile.DoesNotExist:
        # If user profile doesn't exist, return a failure response
            return {"success": False, "message": "User profile not found."}

    # If both user and profile are found, return the data
        return {
            "token": str(request.auth),  # None
            "user_id": user.pk,
            "username": user.username,  # `django.contrib.auth.User` instance.
            "email": user.email,
            "is_superuser": user.is_superuser,
            "last_login": user.last_login,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile": {
            "profile_id": user.pk,
            "country": profile.country,
            "language": None if profile.language is None else profile.language.pk,
            "time_zone": None if profile.tmz is None else profile.tmz.pk,
            "gender": profile.gender,
            "phoneno": profile.phoneno,
            "address": profile.address,
            "birth_date": profile.birth_date,
            "profile_picture": f"{webconfig.API_URL}media/profile/{profile.profile_picture}",
            "verification_code": profile.verification_code,
            "is_verified": profile.is_verified,
            "is_deletable": profile.is_verified,
            "is_disabled": profile.is_disabled,
            "created": profile.created,
        },
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "date_joined": user.date_joined,
        "message": "",
        "success": True,
    }

    def getAuthUserByEmailReset(self, request, lang, email):
        user = User.objects.get(email=email)
        profile = UserProfile.objects.get(user=User(pk=user.pk))
        return {
            # "token": str(request.auth),  # None
            "user_id": user.pk,
            "username": user.username,  # `django.contrib.auth.User` instance.
            "email": user.email,
            "is_superuser": user.is_superuser,
            "last_login": user.last_login,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile": {
                "profile_id": user.pk,
                "country": profile.country,
                # "country":  None if profile.country == None else profile.country.pk,
                "language": None if profile.language is None else profile.language.pk,
                "time_zone": None if profile.tmz is None else profile.tmz.pk,
                "gender": profile.gender,
                "phoneno": profile.phoneno,
                "address": profile.address,
                "birth_date": profile.birth_date,
                "profile_picture": f"{webconfig.API_URL}media/profile/{profile.profile_picture}",
                "verification_code": profile.verification_code,
                "is_verified": profile.is_verified,
                "is_deletable": profile.is_verified,
                "is_disabled": profile.is_disabled,
                "created": profile.created,
            },
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            "date_joined": user.date_joined,
            "message": "",
            "success": True,
        }

    def DirectLoginUser(self, request, lang, username):
        users = User.objects.filter(Q(username=username) | Q(email=username) | 
        Q(userprofile__phoneno=username))
        if users.exists():
            user = users.get()
            return self.getAuthUserById(request, lang, user.pk)
        else:
            return {"message": "Invalid login credentials", "success": False}

    #########################################
    def getAllUsers(self, request, lang):
        results = []
        User = get_user_model()
        users = User.objects.all()
        User.objects.update(
            is_active = True
        )
        for user in users:
            userid = user.pk
            profile = UserProfile.objects.get(user=User(pk=userid))
            results.append(
                {
                    "token": str(request.auth),  # None
                    "user_id": user.pk,
                    "username": user.username,  # `django.contrib.auth.User` instance.
                    "email": user.email,
                    "is_superuser": user.is_superuser,
                    "last_login": user.last_login,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "profile": {
                        "profile_id": user.pk,
                        "country": profile.country,
                        # "country":  None if profile.country == None else profile.country.pk,
                        "language": None
                        if profile.language is None
                        else profile.language.pk,
                        "time_zone": None if profile.tmz is None else profile.tmz.pk,
                        "gender": profile.gender,
                        "phoneno": profile.phoneno,
                        "address": profile.address,
                        "birth_date": profile.birth_date,
                        "profile_picture": f"{webconfig.API_URL}media/profile/{profile.profile_picture}",
                        "verification_code": profile.verification_code,
                        "is_verified": profile.is_verified,
                        "is_deletable": profile.is_verified,
                        "is_disabled": profile.is_disabled,
                        "created": profile.created,
                    },
                    "is_staff": user.is_staff,
                    "is_active": user.is_active,
                    "date_joined": user.date_joined,
                    "message": "",
                    "success": True,
                }
            )
        return results

    def getAllFundManagers(self, request, lang):
        results = []
        User = get_user_model()
        profiles = UserProfile.objects.filter(user_type="fund")
        for profile in profiles:
            users = User.objects.filter(pk=profile.user.pk, is_active=True)
            for user in users:
                investment_options = []
                # lets get their options by id
                option = InvestmentOption.objects.filter(fund_manager_id=user.pk)
                if len(option) != 0:
                    for options in option:
                        # get performance
                        investment_performance = []
                        performance = InvestmentPerformance.objects.filter(fund_manager_id=user.pk, investment_option_id=options.pk)
                        if len(performance) != 0:
                            for item in performance:
                                investment_performance.append({
                                    "name": item.investment_option.name,
                                    "data": item.units
                                })
                        else:
                            investment_performance.append({
                                "name": "",
                                "data": 0
                            })
                        investment_options.append({
                            "name": options.name,
                            "class": options.class_type.name,
                            "description": options.description,
                            "user": user.pk,
                            "performance": investment_performance
                        })
                    results.append(
                        {
                            "user_id": user.pk,
                            "username": user.username,  # `django.contrib.auth.User` instance.
                            "email": user.email,
                            "is_superuser": user.is_superuser,
                            "last_login": user.last_login,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "profile": {
                                "profile_id": profile.pk,
                                "country": profile.country,
                                # "country":  None if profile.country == None else profile.country.pk,
                                "language": None
                                if profile.language is None
                                else profile.language.pk,
                                "time_zone": None if profile.tmz is None else profile.tmz.pk,
                                "gender": profile.gender,
                                "phoneno": profile.phoneno,
                                "company_category": profile.company_category,
                                "address": profile.address,
                                "birth_date": profile.birth_date,
                                "profile_picture": f"{webconfig.API_URL}media/profile/{profile.profile_picture}",
                                "verification_code": profile.verification_code,
                                "is_verified": profile.is_verified,
                                "is_deletable": profile.is_verified,
                                "is_disabled": profile.is_disabled,
                                "created": profile.created,
                            },
                            "is_staff": user.is_staff,
                            "is_active": user.is_active,
                            "date_joined": user.date_joined,
                            "message": "",
                            "success": True,
                            "options": investment_options
                        }
                    )
        return results

    def getAllUsersEmails(self, request, lang):
        results = []
        User = get_user_model()
        users = User.objects.all()
        for user in users:
            results.append(
                user.email
            )
        return results

    #################################################
    def accountExists(self, request, username, lang):
        user = User.objects.filter(Q(username=username) | Q(email=username))
        if user.exists():
            return True
        else:
            return False

    def userExistsById(self, request, lang, id):
        user = User.objects.filter(pk=int(id))
        if user.exists():
            return True
        else:
            return False

    def isVerificationTokenValid(self, request, lang, id, token):
        user_prof = UserProfile.objects.filter(user=User(pk=int(id))).filter(
            verification_code=token
        )
        if user_prof.exists():
            return True
        else:
            return False

    def isAccounVerified(self, request, lang, userid, token):
        user_prof = (
            UserProfile.objects.filter(user=User(pk=int(userid)))
            .filter(verification_code=token)
            .filter(is_verified=True)
        )
        if user_prof.exists():
            return True
        else:
            return False

    def isUserAccountVerified(self, request, lang, id):
        user_prof = (
            UserProfile.objects.filter(user=User(pk=int(id)))
            .filter(is_verified=True)
        )
        if user_prof.exists():
            return True
        else:
            return False

    def isAccounVerifiedByID(self, request, lang, userid):
        print(userid)
        user_prof = UserProfile.objects.filter(user=User(pk=userid)).filter(
            is_verified=True
        )
        if user_prof.exists():
            return True
        else:
            return False

    def emailExists(self, request, lang, email):
        user = User.objects.filter(email=email)
        if user:
            return True
        else:
            return False

    def emailIsVerified(self, request, lang, email):
        user = self.emailExists(request, lang, email)
        if user:
            get_user = self.getAuthUserByEmail(request, lang, email)
            user_id = get_user["user_id"]
            profile = UserProfile.objects.filter(user_id=user_id)
            for profiles in profile:
                is_verified = profiles.is_verified
                if is_verified is True:
                    return True
                else:
                    return False
        else:
            return False

    def resendVerificationEmail(self, request, lang, email):
        user = self.emailExists(request, lang, email)
        if user:
            get_user = self.getAuthUserByEmail(request, lang, email)
            userid = get_user["user_id"]
            user = self.getAuthUserById(request, lang, userid)
            current_site = get_current_site(request)
            profile = UserProfile.objects.filter(user_id=userid)
            for profiles in profile:
                verificationcode = profiles.verification_code
            ###############
            encrypted_verification_code = self.cryptor.encrypt(verificationcode)
            encrypted_userid = self.cryptor.encrypt(userid)
            content = self.mailer.getEMailTemplateContent(
                "verify_account_email_template.html",
                {
                    "user": user,
                    "encrypted_verification_code": encrypted_verification_code,
                    "encrypted_userid": encrypted_userid,
                    "verificationcode": verificationcode,
                    "domain": current_site,
                },
            )
            #######################################
            self.mailer.sendHTMLEmail(email, "Please verify your account", content)
            return {
                "message": "Verification Email sent",
                "success": True
            }
        else:
            return {
                "message": "User doesnot exist",
                "success": False
            }
            
            
    def SendVerication(self, request, lang, email):
        user = self.emailExists(request, lang, email)
        if user:
            get_user = self.getAuthUserByEmail(request, lang, email)
            userid = get_user["user_id"]
            user = self.getAuthUserById(request, lang, userid)
            current_site = get_current_site(request)
            profile = UserProfile.objects.filter(user_id=userid)
            for profiles in profile:
                verificationcode = profiles.verification_code
            ###############
            encrypted_verification_code = self.cryptor.encrypt(verificationcode)
            encrypted_userid = self.cryptor.encrypt(userid)
            content = self.mailer.getEMailTemplateContent(
                "email_verification.html",
                {
                    "user": user,
                    "encrypted_verification_code": encrypted_verification_code,
                    "encrypted_userid": encrypted_userid,
                    "verificationcode": verificationcode,
                    "domain": current_site,
                },
            )
            #######################################
            self.mailer.sendHTMLEmail(email, "Please verify your account", content)
            return {
                "message": "Verification Email sent",
                "success": True
            }
        else:
            return {
                "message": "User doesnot exist",
                "success": False
            }
    def SendSimpleEmail(self, request, lang, email):
        content = self.mailer.getEMailTemplateContent(
            "simple_verify_email_template.html",
            {
                "message": "email template"
            },
        )
        send = self.mailer.sendHTMLEmail(
            email, "Email Verification", content)
        if send:
            return {
                "message": "Email sent",
                "success": True
            }
        else:
            return {
                "message": "Email not",
                "success": False
            }
            
    def SimpleEmail(self, request, lang, email):
        content = self.mailer.getEMailTemplateContent(
            "govt.html",
            {
                "message": "invest template"
            },
        )
        send = self.mailer.sendHTMLEmail(
            email, "Invest", content)
        if send:
            return {
                "message": "Email sent",
                "success": True
            }
        else:
            return {
                "message": "Email not",
                "success": False
            }

    def phoneExists(self, request, lang, phoneno):
        user_prof = UserProfile.objects.filter(phoneno=phoneno)
        if user_prof:
            return True
        else:
            return False

    def createAuthUser(self, request, lang):
        current_datetime = datetime.datetime.now()
        # allusers = User.objects.all().count()
        ##########################
        first_name = request.data["first_name"]
        email = request.data["email"]
        if email:
            username = email
        # pkg_id = request.data["pkg_id"]
        last_name = request.data["last_name"]
        password = request.data["password"]
        # confirmpassword = request.data["confirmpassword"]
        #### profile
        # default_language = self.locale.getDefaultLanguages(request, lang)
        profile = request.data["profile"]
        gender = profile["gender"]
        birth_date = profile["birth_date"]
        country = profile["country"]
        # PROFILE
        profile = request.data["profile"]
        gender = profile["gender"]
        phoneno = profile["phone_no"]
        birth_date = profile["birth_date"] if profile["birth_date"] else None
        profile_picture = "default_picture.jpg"
        verificationcode = str(self.help.getRandom())
        # package = self.package.getPackageByCodeName(request, lang, "free")
        # defaultpkgid = package["id"]
        # defaultlangid = default_language["id"]
        # create user
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True
        user.save()
        # get saved user
        userid = user.pk
        # Get the user add update the available profile data
        uuser = User.objects.get(pk=userid)
        uuser.userprofile.gender = None if not gender else gender
        uuser.userprofile.phoneno = None if not phoneno else phoneno
        uuser.userprofile.birth_date = None if not birth_date else birth_date
        uuser.userprofile.country = None if not country else country
        # uuser.userprofile.country = None if not str(country) else SupportedCountry(pk=int(country))
        # uuser.userprofile.package = Package(pk=int(defaultpkgid))
        # uuser.userprofile.language = SupportedLanguage(pk=int(defaultlangid))
        uuser.userprofile.verification_code = verificationcode
        uuser.userprofile.profile_picture = profile_picture
        uuser.userprofile.last_modified = current_datetime
        uuser.save()
        # get Token
        #############
        user = self.getAuthUserById(request, lang, userid)
        current_site = get_current_site(request)
        ###############
        encrypted_verification_code = self.cryptor.encrypt(verificationcode)
        encrypted_userid = self.cryptor.encrypt(userid)
        content = self.mailer.getEMailTemplateContent(
            "verify_account_email_template.html",
            {
                "user": user,
                "encrypted_verification_code": encrypted_verification_code,
                "encrypted_userid": encrypted_userid,
                "verificationcode": verificationcode,
                "domain": current_site,
            },
        )
        content2 = self.mailer.getEMailTemplateContent(
            "email_verification.html",
            {
                "user": user,
                "verificationcode": verificationcode,
            },
        )
        #######################################
        self.mailer.sendHTMLEmail(email, "Please verify your account", content)
      
        return {
            "message": f"Your Account has been created successfuly, please take time and verify it with the link sent to {email} or use verification code {verificationcode}",
            "success": True,
            "user": user,
            "verificationcode": verificationcode,
        }

    def createApiUser(self, request, lang):
        current_datetime = datetime.datetime.now()
        # allusers = User.objects.all().count()
        first_name = request.data["first_name"]
        email = request.data["email"]
        if email:
            username = email
        last_name = request.data["last_name"]
        password = request.data["password"]
        company_category = request.data["company_category"]
        user_type = request.data["user_type"]
        country = request.data["country"]
        phoneno = request.data["phone"]
        logo = "default_logo.jpg"
        verificationcode = str(self.help.getRandom())
        # create user
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True
        user.save()
        # get saved user
        userid = user.pk
        moa = request.data["moa"]
        if moa:
            name = "moa"
            self.UploadProfileFiles(request, lang, userid, name, moa)
        coi = request.data["coi"]
        if coi:
            name = "coi"
            self.UploadProfileFiles(request, lang, userid, name, coi)
        # Get the user add update the available profile data
        uuser = User.objects.get(pk=userid)
        uuser.userprofile.company_category = None if not company_category else company_category
        uuser.userprofile.phoneno = None if not phoneno else phoneno
        uuser.userprofile.user_type = None if not user_type else user_type
        uuser.userprofile.country = None if not country else country
        uuser.userprofile.verification_code = verificationcode
        uuser.userprofile.logo = logo
        uuser.userprofile.last_modified = current_datetime
        uuser.userprofile.moa = moa
        uuser.userprofile.coi = coi
        uuser.userprofile.website = last_name
        uuser.save()
        # get Token
        #############
        user = self.getAuthUserById(request, lang, userid)
        current_site = get_current_site(request)
        ###############
        encrypted_verification_code = self.cryptor.encrypt(verificationcode)
        encrypted_userid = self.cryptor.encrypt(userid)
        content = self.mailer.getEMailTemplateContent(
            "verify_account_email_template.html",
            {
                "user": user,
                "encrypted_verification_code": encrypted_verification_code,
                "encrypted_userid": encrypted_userid,
                "verificationcode": verificationcode,
                "domain": current_site,
            },
        )
        #######################################
        self.mailer.sendHTMLEmail(email, "Please verify your account", content)
        return {
            "message": f"Your Account has been created successfuly, please take time and verify it with the link sent to {email} or use verification code {verificationcode}",
            "success": True,
            "user": user,
            "verificationcode": verificationcode,
        }
        ######## Upadte verification status
    def verify_user_account(self, request, lang, username, code):
    # Check if the email exists
        user_data = self.getAuthUserByEmail(request, lang, username)
    
        if not user_data or not user_data.get("success"):
            return Response({"message": "User not found", "success": False}, status=404)

    # Extract user ID from the returned dictionary
        user_id = user_data.get("user_id")

    # Fetch the UserProfile using the extracted user ID
        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"message": "User profile not found", "success": False}, status=404)

    # Validate the verification code
        if user_profile.verification_code != code:
            return Response({"message": "Invalid verification code", "success": False}, status=400)

    # Check if the account is already verified
        if user_profile.is_verified:
            return Response({"message": "Account already verified", "success": True}, status=200)

    # Mark the account as verified
        user_profile.is_verified = True
        user_profile.save()

        return Response({"message": "Account verified successfully", "success": True}, status=200)
    
    
    
    def set_passcode(self, request, lang, email, code):
    # Check if the email exists
        user_data = self.getAuthUserByEmail(request, lang, email)

        if not user_data or not user_data.get("success"):
            return Response({"message": "User not found", "success": False}, status=404)

    # Extract user ID from the returned dictionary
        user_id = user_data.get("user_id")

    # Fetch the UserProfile using the extracted user ID
        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"message": "User profile not found", "success": False}, status=404)

    # Encrypt the passcode before storing it
        hashed_passcode = make_password(code)

    # Update the passcode field in the database
        user_profile.passcode = hashed_passcode
        user_profile.save()

        return Response({"message": "Passcode updated successfully", "success": True}, status=200)


    def UpdateUserPhoneNumber(self, request, lang, userid, phone_number):
        UserProfile.objects.filter(user=User(pk=int(userid))).update(
            phoneno=phone_number
        )

    def UpdateProfilePhoto(self, request, lang, userid, filename):
        # name = filename.name
        name_id = str(random.random())
        user_id = str(userid)
        output = 'profile_picture'+user_id+name_id+'.jpg'
        #########################
        # let us first delete the other photos of
        # this user before updating a new one
        old_profile_pictures = UserProfile.objects.filter(
            user=User(pk=int(userid))).get()
        old_picture = old_profile_pictures.profile_picture
        old_picture_name = old_picture.name
        if old_picture_name != "default_picture.jpg":
            # remove old picture
            os.remove('media/profile/'+old_picture_name)
            destination = open('media/profile/'+output, 'wb+')
            for chunk in filename.chunks():
                destination.write(chunk)
            destination.close()
            UserProfile.objects.filter(user=User(pk=int(userid))).update(
                profile_picture=output
            )
        else:
            destination = open('media/profile/'+output, 'wb+')
            for chunk in filename.chunks():
                destination.write(chunk)
            destination.close()
            UserProfile.objects.filter(user=User(pk=int(userid))).update(
                profile_picture=output
            )

    def UploadProfileFiles(self, request, lang, userid, fieldname, filename):
        api_user = User.objects.get(pk=userid)
        name_id = api_user.first_name
        output = fieldname+name_id+'.pdf'
        destination = open('media/file/'+output, 'wb+')
        for chunk in filename.chunks():
            destination.write(chunk)
        destination.close()
        if fieldname == "moa":
            UserProfile.objects.filter(user=User(pk=int(userid))).update(
                moa=output
            )
        else:
            UserProfile.objects.filter(user=User(pk=int(userid))).update(
                coi=output
            )

    def ResendVerificationCode(self, request, lang, email):
        verificationcode = str(self.help.getRandom())
        user = self.getAuthUserByEmail(request, lang, email)
        userid = user["user_id"]
        verification_link = (
            f"{webconfig.WEB_APP_URL}auth/{userid}/verify/?code={verificationcode}"
        )
        content = self.mailer.getEMailTemplateContent(
            "verify_account_email_template.html",
            {
                "verification_link": verification_link,
                "user": user,
                "verificationcode": verificationcode,
            },
        )
        if self.mailer.sendHTMLEmail(email, "Please verify your account", content):
            user = UserProfile.objects.filter(user=User(pk=int(user["user_id"])))
            user.update(verificationcode=verificationcode)
            return {
                "message": f"A verification code has been send to {email}, please check your inbox or spam emails",
                "success": True,
            }
        else:
            return {
                "message": f"Something went wrong and we failed to send your emnail, please try again laiter",
                "success": False,
            }

    def InitPasswordReset(self, request, lang, email, code):
    # Check if the email exists
        user = self.getAuthUserByEmail(request, lang, email)
    
    # If the user doesn't exist, return an error message
        if not user or not user.get("success"):
            return {
                "message": "User with this email does not exist.",
                "success": False,
            }

        verificationcode = code
        
    
        content = self.mailer.getEMailTemplateContent(
            "password_reset_email_template.html",
            {
                "user": user,
                "code": verificationcode,
                "email": email
            },
        )

        if self.mailer.sendHTMLEmail(email, "Password Reset", content):
           
            return {
                "message": f"A password reset link and code has been sent to {email}, please check your email inbox or spam.",
                "success": True,
                "status": "success",
                
            }
        else:
            return {
                "message": "Something went wrong and we failed to send your email, please try again later.",
                "success": False,
            }

    def VerifyAccount(self, request, lang, id, token):
        UserProfile.objects.filter(user=User(pk=int(id))).filter(
            verification_code=token
        ).update(is_verified=True)
        return True

    def UpdateAuthUser(self, request, lang, userid, data):
        current_datetime = datetime.datetime.now()
        old_user = User.objects.filter(pk=userid).get()
        old_usergroup = UserGroup.objects.filter(user=User(pk=userid)).get()
        # print(idzerofilling)
        username = data["username"] if data["username"] else old_user.username
        first_name = data["first_name"] if data["first_name"] else old_user.first_name
        email = data["email"] if data["email"] else old_user.email
        last_name = data["last_name"] if data["last_name"] else old_user.last_name
        is_staff = data["is_staff"] if str(data["is_staff"]) else old_user.is_staff
        is_superuser = (
            data["is_superuser"] if str(data["is_superuser"]) else old_user.is_superuser
        )
        is_active = data["is_active"] if str(data["is_active"]) else old_user.is_active
        # PROFILE
        profile_id = data["profile_id"]
        gender = data["gender"] if data["gender"] else old_user.userprofile.gender
        phoneno = data["phoneno"] if data["phoneno"] else old_user.userprofile.phoneno
        title = data["title"] if data["title"] else old_user.userprofile.title
        bio = data["bio"] if data["bio"] else old_user.userprofile.bio
        location = (
            data["location"] if data["location"] else old_user.userprofile.location
        )
        birth_date = (
            data["birth_date"]
            if data["birth_date"]
            else old_user.userprofile.birth_date
        )
        profile_picture = (
            data["profile_picture"]
            if data["profile_picture"]
            else old_user.userprofile.profile_picture
        )
        usignature = (
            data["usignature"]
            if data["usignature"]
            else old_user.userprofile.usignature
        )
        security_group_id = (
            data["security_group_id"]
            if str(data["security_group_id"])
            else old_usergroup.security_group.pk
        )
        uuser = User.objects.get(pk=userid)
        uuser.username = username
        uuser.first_name = first_name
        uuser.email = email
        uuser.last_name = last_name
        uuser.is_staff = is_staff
        uuser.is_superuser = is_superuser
        uuser.is_active = is_active
        uuser.userprofile.has_been_modified = True
        uuser.userprofile.gender = gender
        uuser.userprofile.phoneno = phoneno
        uuser.userprofile.title = title
        uuser.userprofile.bio = bio
        uuser.userprofile.location = location
        uuser.userprofile.birth_date = birth_date
        uuser.userprofile.profile_picture = profile_picture
        uuser.userprofile.last_modified = current_datetime
        uuser.save()
        # create user
        usergroup = UserGroup.objects.filter(user=User(pk=userid))
        usergroup.update(
            security_group=SecurityGroup(pk=security_group_id),
            has_been_modified=True,
            last_modified=current_datetime,
        )
        return True

    def UpdateAuthUserPassword(self, request, lang, password, email):
        password = make_password(str(password))
        user = self.getAuthUserByEmail(request, lang, email)
        userid = user["user_id"]
        old_user = User.objects.filter(pk=userid)
        old_user.update(password=password)
        return True

    def DeleteAccount(self, request, lang):
        userid = Token.objects.get(key=request.auth).user_id
        user = User.objects.get(pk=userid)
        user.delete()
        return True

   

def onboardUsers(self, request, lang, user):
    try:
        current_datetime = user["profile"]["created"]
        first_name = user["first_name"]
        email = user["email"]
        username = user["email"]
        last_name = user["last_name"]
        password = user["password"]
        is_deleted = False
        is_verified = user["profile"]["is_verified"]
        gender = user["profile"]["gender"]
        birth_date = user["profile"]["birth_date"]
        country = user["profile"]["country"]
        phoneno = user["profile"]["phoneno"]
        profile_picture = "photo.png"
        
        # Create the user
        users = User.objects.create_user(username, email, password)
        users.first_name = first_name
        users.last_name = last_name
        users.is_superuser = False
        users.is_staff = False
        users.is_active = True
        users.save()
        
        # Set profile information
        userid = users.pk
        uuser = User.objects.get(pk=userid)
        uuser.userprofile.gender = None if not gender else gender
        uuser.userprofile.phoneno = None if not phoneno else phoneno
        uuser.userprofile.birth_date = None if not birth_date else birth_date
        uuser.userprofile.country = None if not country else country
        uuser.userprofile.profile_picture = profile_picture
        uuser.userprofile.last_modified = current_datetime
        uuser.userprofile.is_verified = is_verified
        uuser.userprofile.is_deleted = is_deleted
        uuser.save()
        
        userss = self.getAuthUserById(request, lang, userid)
        
        return {
            "message": "User has been added",
            "success": True,
            "user": userss
        }
    
    except IntegrityError:
        return {
            "message": "Email or phone already exists",
            "success": False
        }


    def onboardOrtusUsers(self, request, lang, user):
        first_name = user["first_name"]
        email = user["email"]
        username = user["email"]
        last_name = user["last_name"]
        password = str(random.randint(1000, 9999))
        gender = user["gender"]
        birth_date = user["birth_date"]
        # country update when necessary
        country = "UG"
        phoneno = user["phone_no"]
        profile_picture = "photo.png"
        users = User.objects.create_user(username, email, password)
        users.first_name = first_name
        users.last_name = last_name
        users.is_superuser = False
        users.is_staff = False
        users.is_active = True
        users.save()
        userid = users.pk
        uuser = User.objects.get(pk=userid)
        uuser.userprofile.gender = None if not gender else gender
        uuser.userprofile.phoneno = None if not phoneno else phoneno
        uuser.userprofile.birth_date = None if not birth_date else birth_date
        uuser.userprofile.country = None if not country else country
        uuser.userprofile.profile_picture = profile_picture
        uuser.userprofile.is_verified = True
        uuser.userprofile.is_deleted = False
        uuser.save()
        current_site = get_current_site(request)
        encrypted_userid = self.cryptor.encrypt(userid)
        # email user their otp
        content = self.mailer.getEMailTemplateContent(
            "otp_template.html",
            {
                    "user": user,
                    "email": email,
                    "otp": password,
                    "encrypted_userid": encrypted_userid,
                    "domain": current_site,
                },
        )
        #######################################
        self.mailer.sendHTMLEmail(email, "Cyanase OTP", content)
        return {
                "message": "Verification Email sent",
                "success": True
            }
