from django.shortcuts import render
# Create your views here.
from .Users import Users
from django.urls import reverse,resolve
from django.shortcuts import render, HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from api.helper.helper import Helper
import json
from django.db.models import Q
from api.v1.mailer.Mailer import Mailer
from django.contrib.sites.shortcuts import get_current_site
from ...models import UserProfile, User 
from django.contrib.auth.hashers import check_password
DEFAULT_LANG = "en"
# init module class
_user = Users()
_helper = Helper()
mailer = Mailer()

class GetAuthUser(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang is None else lang
        user = _user.getAuthUser(request, lang)
        return Response(user)


class GetAllUsers(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang is None else lang
        user = _user.getAllUsers(request, lang)
        return Response(user)


class GetAllFundManagers(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang is None else lang
        user = _user.getAllFundManagers(request, lang)
        return Response(user)


class GetAllUsersEmails(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, lang, format=None):
        lang = DEFAULT_LANG if lang is None else lang
        user = _user.getAllUsersEmails(request, lang)
        return Response(user)


class GetAuthUserById(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, lang, userid):
        if not str(userid):
            return Response({
                'message': "Incomplete data request",
                'success': False
            })
        lang = DEFAULT_LANG if lang == None else lang
        user = _user.getAuthUserById(request, lang, userid)
        return Response(user)


class IsVerified(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, lang, userid):
        if not str(userid):
            return Response({
                'message': "Incomplete data request",
                'success': False
            })
        lang = DEFAULT_LANG if lang is None else lang
        user = _user.isUserAccountVerified(request, lang, userid)
        return Response(user)


class GetAuthUserByEmail(ObtainAuthToken):
    def post(self, request, lang):
        email = request.data
        if not str(email):
            return Response({
                'message': "Incomplete data request",
                'success': False
            })
        lang = DEFAULT_LANG if lang == None else lang
        user = _user.emailExists(request,lang,email)
        if user:
            return Response(True)
        else:
            return Response(False)


class IsUserVerified(ObtainAuthToken):
    def post(self, request, lang):
        email = request.data
        if not str(email):
            return Response({
                'message': "Incomplete data request",
                'success': False
            })
        lang = DEFAULT_LANG if lang is None else lang
        is_verified = _user.emailIsVerified(request, lang, email)
        if is_verified is True:
            return Response({
                "message": "User is verified",
                "success": True
            })
        else:
            return Response({
                "message": "User is not verified",
                "success": False
            })


class ResendVerificationEmail(ObtainAuthToken):
    def post(self, request, lang):
        email = request.data
        if not str(email):
            return Response({
                'message': "Incomplete data request",
                'success': False
            })
        lang = DEFAULT_LANG if lang is None else lang
        email_sent = _user.resendVerificationEmail(request, lang, email)
        if email_sent["success"] is True:
            return Response({
                "message": "verification email sent",
                "success": True
            })
        else:
            return Response({
                "message": "verification email not sent",
                "success": False
            })

class SendSimpleEmail(ObtainAuthToken):
    def post(self, request, lang):
        email = request.data
        if not str(email):
            return Response({
                'message': "Incomplete data request",
                'success': False
            })
        lang = DEFAULT_LANG if lang is None else lang
        email_sent = _user.SendSimpleEmail(request, lang, email)
        if email_sent["success"] is True:
            return Response({
                "message": "verification email sent",
                "success": True
            })
        else:
            return Response({
                "message": "verification email not sent",
                "success": False
            })


class SimpleEmail(ObtainAuthToken):
    def post(self, request, lang):
        email = request.data
        if not str(email):
            return Response({
                'message': "Incomplete data request",
                'success': False
            })
        lang = DEFAULT_LANG if lang is None else lang
        email_sent = _user.SimpleEmail(request, lang, email)
        if email_sent["success"] is True:
            return Response({
                "message": "invest email sent",
                "success": True
            })
        else:
            return Response({
                "message": "invest email not sent",
                "success": False
            })


class CreateUserAuthToken(ObtainAuthToken):
    def post(self, request, lang, *args, **kwargs):
        lang = DEFAULT_LANG if lang == None else lang
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


# Login User
class LoginUserAuthToken(ObtainAuthToken):
    def post(self, request, lang):
        lang = DEFAULT_LANG if lang is None else lang
        data = request.data
        if data:
            username = data["username"]
            password = data["password"]
            # print(username)
            # print(password)
            if not username:
                return Response({
                    'message': "Username is required",
                    'success': False
                })
            elif not password:
                return Response({
                    'message': "Password is required",
                    'success': False
                })
            else:
                unilogin = _user.DirectLoginUser(request, lang, username)
                ########
                if not unilogin["success"]:
                    return Response(unilogin)
                else:
                    username = unilogin["username"]
                    user = authenticate(username=username, password=password)
                   
                    if user:
                        token, created = Token.objects.get_or_create(user=user)
                        user_data = unilogin  # `unilogin` contains the user dictionary
                        profile = user_data.get("profile", {})  # Safely get the profile
                        is_verified = profile.get("is_verified", False)
                        
                        if not is_verified:
                         verification_code = profile.get("verification_code", None)
                         current_site = get_current_site(request)
                         content = mailer.getEMailTemplateContent(
                         "verify_account_email_template.html",
                          {
                           "user": user,
                           "verificationcode": verification_code,
                           "domain": current_site,
                          },
            )
                         mailer.sendHTMLEmail(user.email, "Please verify your account", content)

                        return Response(
                            {
                            'token': token.key,
                            'user_id': user.pk,
                            "user": unilogin,
                            'message': "You are logged in",
                            'success': True
                        })
                    else:
                        return Response({
                            'message': "Invalid login credentials",
                            'success': False
                        })

        else:
            return Response({"message": "Invalid request method", "status": "failed"}, status=400)

# login with passcode
                                        
class LoginWithPasscode(ObtainAuthToken):
    def post(self, request, lang):
        lang = DEFAULT_LANG if lang is None else lang
        data = request.data

        if not data:
            return Response({"message": "Invalid request method", "status": "failed"}, status=400)

        username = data.get("username")
        passcode = data.get("password")  # Assuming the passcode is sent as "password"

        if not username:
            return Response({
                'message': "Username is required",
                'success': False
            })

        if not passcode:
            return Response({
                'message': "Passcode is required",
                'success': False
            })

        # Fetch the user and user profile
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
        except User.DoesNotExist:
            return Response({
                'message': "User not found",
                'success': False
            })
        except UserProfile.DoesNotExist:
            return Response({
                'message': "User profile not found",
                'success': False
            })

        # Compare the provided passcode with the hashed passcode in the user profile
        if not check_password(passcode, user_profile.passcode):
            return Response({
                'message': "Invalid passcode",
                'success': False
            })

        # Generate or retrieve the token
        token, created = Token.objects.get_or_create(user=user)

        # Fetch user data
        unilogin = _user.DirectLoginUser(request, lang, username)
        if not unilogin["success"]:
            return Response(unilogin)

        profile = unilogin.get("profile", {})
        is_verified = profile.get("is_verified", False)

        # Handle unverified users
        if not is_verified:
            verification_code = profile.get("verification_code", None)
            current_site = get_current_site(request)
            content = getEMailTemplateContent(
                "verify_account_email_template.html",
                {
                    "user": user,
                    "verificationcode": verification_code,
                    "domain": current_site,
                },
            )
            sendHTMLEmail(user.email, "Please verify your account", content)

        # Return success response
        return Response({
            'token': token.key,
            'user_id': user.pk,
            "user": unilogin,
            'message': "You are logged in",
            'success': True
        })
# Generate custom AUTH Token
class CreateUserAuthToken(ObtainAuthToken):
    def post(self, request, lang, *args, **kwargs):
        lang = DEFAULT_LANG if lang == None else lang
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

# Create Auth User


class CreateAuthUser(ObtainAuthToken):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ['post']

    def post(self, request, lang, *args, **kwargs):
        lang = DEFAULT_LANG if lang is None else lang
        first_name = request.data["first_name"]
        email = request.data["email"]
        if email:
            username = email
        # pkg_id = request.data["pkg_id"]
        last_name = request.data["last_name"]
        password = request.data["password"]
        confirmpassword = request.data["confirmpassword"]
        # profile
        profile = request.data["profile"]
        gender = profile["gender"]
        birth_date = profile["birth_date"]
        phone_no = profile["phone_no"]
        country = profile["country"]
        ##########################
        if not username:
            return Response({
                'message': "Email is required",
                "type": "username",
                'success': False
            })
        elif len(str(username)) < 3:
            return Response({
                'message': "Email must be greater than 3 characters",
                "type": "username",
                'success': False
            })
        elif _user.accountExists(request, username, lang):
            return Response({
                'message': "User already exists, please enter a unique email",
                "type": "username",
                'success': False
            })
        elif not email:
            return Response({
                'message': "Email is required",
                "type": "email",
                'success': False
            })
        elif not _helper.isEmailValid(email):
            return Response({
                'message': "Invalid email address",
                "type": "email",
                'success': False
            })
        elif _user.emailExists(request, lang, email):
            return Response({
                'message': f"Account with email address {email} already exists",
                "type": "email",
                'success': False
            })
        elif str(phone_no) and _user.phoneExists(request, lang, phone_no):
            return Response({
                'message': "Phone number already exists",
                "type": "phone",
                'success': False
            })
        elif not first_name:
            return Response({
                'message': "First name is required",
                "type": "first_name",
                'success': False
            })
        elif not last_name:
            return Response({
                'message': "Last name is required",
                "type": "last_name",
                'success': False
            })
        elif not password:
            return Response({
                'message': "Password is required",
                "type": "password",
                'success': False
            })
        elif password and len(password) < 6:
            return Response({
                'message': "Password is too short, must atleast 6 characters or above",
                "type": "password",
                'success': False
            })
        elif password and not confirmpassword:
            return Response({
                'message': "Please confirm your password",
                "type": "confirm_password",
                'success': False
            })
        elif password and not (confirmpassword == password):
            return Response({
                'message': "Passwords don't match",
                "type": "password_1_2",
                'success': False
            })
        elif not gender:
            return Response({
                'message': "Gender is required",
                "type": "gender",
                'success': False
            })
        elif not country:
            return Response({
                'message': "Country is required",
                "type": "country",
                'success': False
            })
        elif not birth_date:
            return Response({
                'message': "date of birth is required",
                "type": "birth_date",
                'success': False
            })
        else:
            user = _user.createAuthUser(request, lang)
            return Response(user)
#Check if user details exists
class CheckUser (ObtainAuthToken):
    def post(self, request, lang, *args, **kwargs):
        lang = DEFAULT_LANG if lang == None else lang
        user = _user.CheckMUser(request, lang)
        return Response(user)
class CreateApiUser(ObtainAuthToken):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ['post']

    def post(self, request, lang, *args, **kwargs):
        lang = DEFAULT_LANG if lang is None else lang
        first_name = request.data["first_name"]
        email = request.data["email"]
        if email:
            username = email
        last_name = request.data["last_name"]
        password = request.data["password"]
        confirmpassword = request.data["confirmpassword"]
        company_category = request.data["company_category"]
        user_type = request.data["user_type"]
        phone_no = request.data["phone"]
        country = request.data["country"]
        moa = request.data["moa"]
        coi = request.data["coi"]
        ##########################
        if not username:
            return Response({
                'message': "Email is required",
                "type": "username",
                'success': False
            })
        elif len(str(username)) < 3:
            return Response({
                'message': "Email must be greater than 3 characters",
                "type": "username",
                'success': False
            })
        elif _user.accountExists(request, username, lang):
            return Response({
                'message': "User already exists, please enter a unique email",
                "type": "username",
                'success': False
            })
        elif not email:
            return Response({
                'message': "Email is required",
                "type": "email",
                'success': False
            })
        elif not _helper.isEmailValid(email):
            return Response({
                'message': "Invalid email address",
                "type": "email",
                'success': False
            })
        elif _user.emailExists(request, lang, email):
            return Response({
                'message': f"Account with email address {email} already exists",
                "type": "email",
                'success': False
            })
        elif str(phone_no) and _user.phoneExists(request, lang, phone_no):
            return Response({
                'message': "Phone number already exists",
                "type": "phone",
                'success': False
            })
        elif not first_name:
            return Response({
                'message': "First name is required",
                "type": "first_name",
                'success': False
            })
        elif not last_name:
            return Response({
                'message': "Last name is required",
                "type": "last_name",
                'success': False
            })
        elif not password:
            return Response({
                'message': "Password is required",
                "type": "password",
                'success': False
            })
        elif password and len(password) < 6:
            return Response({
                'message': "Password is too short, must atleast 6 characters or above",
                "type": "password",
                'success': False
            })
        elif password and not confirmpassword:
            return Response({
                'message': "Please confirm your password",
                "type": "confirm_password",
                'success': False
            })
        elif password and not (confirmpassword == password):
            return Response({
                'message': "Passwords don't match",
                "type": "password_1_2",
                'success': False
            })
        elif not company_category:
            return Response({
                'message': "Company category is required",
                "type": "gender",
                'success': False
            })
        elif not country:
            return Response({
                'message': "Country is required",
                "type": "country",
                'success': False
            })
        elif not user_type:
            return Response({
                'message': "user type is required",
                "type": "user_type",
                'success': False
            })
        elif not moa:
            return Response({
                'message': "moa is required",
                "type": "moa",
                'success': False
            })
        elif not coi:
            return Response({
                'message': "coi is required",
                "type": "coi",
                'success': False
            })
        else:
            user = _user.createApiUser(request, lang)
            return Response(user)


# Create Auth User
class UpdateAuthUserPassword(APIView):
   
    http_method_names = ['post']

    def post(self, request, lang):
        password = request.data["password"]
        confirmpassword = request.data["confirmpassword"]
        email = request.data["email"]
        if not str(email):
            return Response({"message": "Incomplete data request", "success": False})
        if not password:
            return Response({
                'message': "Password is required",
                'success': False
            })
        elif not confirmpassword:
            return Response({
                'message': "Confirmation password is also required",
                'success': False
            })
        elif len(password) < 6:
            return Response({
                'message': "Password is too short, must atleast 6 characters or above",
                'success': False
            })
        elif not confirmpassword:
            return Response({
                'message': "Please confirm your password",
                'success': False
            })
        elif not (confirmpassword == password):
            return Response({
                'message': "Passwords don't match",
                'success': False
            })
        else:
            user = _user.UpdateAuthUserPassword(request, lang, password, email)
            return Response({"message": "Password updated successfully", "success": True, "status":"success"}, status=200)

class ChangeForgotPassword(APIView):
    authentication_classes = []  # No authentication required
    permission_classes = []      # No permissions required

    http_method_names = ['post']

    def post(self, request, lang):
        password = request.data["password"]
        confirmpassword = request.data["confirmpassword"]
        email = request.data["email"]
        if not str(email):
            return Response({"message": "Incomplete data request", "success": False})
        if not password:
            return Response({
                'message': "Password is required",
                'success': False
            })
        elif not confirmpassword:
            return Response({
                'message': "Confirmation password is also required",
                'success': False
            })
        elif len(password) < 6:
            return Response({
                'message': "Password is too short, must atleast 6 characters or above",
                'success': False
            })
        elif not confirmpassword:
            return Response({
                'message': "Please confirm your password",
                'success': False
            })
        elif not (confirmpassword == password):
            return Response({
                'message': "Passwords don't match",
                'success': False
            })
        else:
            user = _user.UpdateAuthUserPassword(request, lang, password, email)
            return Response({"message": "Password updated successfully", "success": True, "status":"success"}, status=200)


class DeleteUserAccount(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, lang):
        user = _user.DeleteAccount(request, lang)
        if user:
            return Response({"message": "Account deleted successfuly", "success": True}, status=200)


class UpdateAuthUser(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    # Request

    def get(self, request, lang, userid):
        lang = DEFAULT_LANG if lang == None else lang
        return Response({
            'message': "Username already exists, please choose another name",
            'success': False
        }
        # , status = 400 alters the response format
        )

    def post(self, request, lang, userid):
        lang = DEFAULT_LANG if lang == None else lang
        if not userid:
            return Response({"message": "Incomplete data request", "success": False})

        request_object = request.body.decode("utf-8")
        if request_object:
            data = json.loads(request_object)
            if len(data) > 0:
                if "username" in data or "email" in data or "is_superuser" in data or "security_group_id" in data or "first_name" in data or "last_name" in data or "profile_id" in data or "gender" in data or "phoneno" in data or "title" in data or "id_number" in data or "bio" in data or "location" in data or "location" in data or "birth_date" in data or "profile_picture" in data or "usignature" in data or "is_staff" in data or "is_active" in data:
                    if not data["username"] and not data["email"] and not str(data["is_superuser"]) and not str(data["security_group_id"]) and not data["first_name"] and not data["last_name"] and not str(data["profile_id"]) and not data["gender"] and not str(data["phoneno"]) and not data["title"] and not data["id_number"] and not data["bio"] and not data["location"] and not data["location"] and not str(data["birth_date"]) and not data["profile_picture"] and not data["usignature"] and not str(data["is_staff"]) and not str(data["is_active"]):
                        return Response({"message": "Can't update when all fields are missing", "success": False})
                    else:
                        email = data["email"]
                        if email and not _helper.isEmailValid(email):
                            return Response({
                                'message': "Email is invalid",
                                'success': False
                            })
                        elif email and _user.emailExists(request, lang, email):
                            return Response({
                                'message': "Email already exists",
                                'success': False
                            })
                        else:
                            results = _user.UpdateAuthUser(
                                request, lang, userid, data)
                            return Response({"message": "User updated successfuly", "success": True}, status=200)
            else:
                return Response({"message": "Incomplete data request", "success": False}, status=400)
        else:
            return Response({"message": "Incomplete data request", "success": False}, status=400)
# Generate custom AUTH Token


class ResendVerificationCode(ObtainAuthToken):
    def get(self, request, lang, *args, **kwargs):
        lang = DEFAULT_LANG if lang == None else lang
        if not ("email" in request.GET):
            return Response({
                'message': "Incomplete data request",
                'success': False
            })
        elif not _helper.isEmailValid(request.GET["email"]):
            return Response({
                'message': "Invalid email address",
                'success': False
            })
        elif not _user.emailExists(request, lang, request.GET["email"]):
            return Response({
                'message': f"Account with email {request.GET['email']} doesn't exist",
                'success': False
            })
        else:
            response = _user.ResendVerificationCode(
                request, lang, request.GET["email"])
            if response["success"]:
                return Response(response)
            else:
                return Response(response, status=400)


# Create Auth User
class verifyAccount(ObtainAuthToken):
    http_method_names = ['post']

    def post(self, request, lang, *args, **kwargs):
        username = request.data.get('username')
        code = request.data.get('code')

        # Validate input fields
        if not username or not code:
            return Response({"message": "Email and verification code are required", "success": False}, status=400)

        # Call the second function to process the verification
        return _user.verify_user_account(request, lang, username, code)
class setPassCode(ObtainAuthToken):
    http_method_names = ['post']

    def post(self, request, lang, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')

        # Validate input fields
        if not email or not code:
            return Response({"message": "passcode is required", "success": False}, status=400)

        # Call the second function to process the verification
        return _user.set_passcode(request, lang, email, code)    
class InitPasswordReset(ObtainAuthToken):
    http_method_names = ['post']
    
    def post(self, request, lang, *args, **kwargs):
        lang = DEFAULT_LANG if lang == None else lang
        email = request.data["email"]
        code = request.data["code"]
        if not email:
            return Response({
                'message': "Incomplete data request",
                'success': False
            })
        else:
            response = _user.InitPasswordReset(
                request, lang, email, code)
            if response["success"]==True:
                return Response(response)
            else:
                return Response(response)

# Generate custom AUTH Token
# class InitPasswordReset(ObtainAuthToken):
#     def get(self, request, lang, *args, **kwargs):
#         lang = DEFAULT_LANG if lang == None else lang
#         if not ("email" in request.GET):
#             return Response({
#                 'message': "Incomplete data request",
#                 'success': False
#             }, status=400)
#         elif not request.GET["email"]:
#             return Response({
#                 'message': "Email field is required",
#                 'success': False
#             })
#         elif not _helper.isEmailValid(request.GET["email"]):
#             return Response({
#                 'message': "Invalid email address",
#                 'success': False
#             })
#         elif not _user.emailExists(request, lang, request.GET["email"]):
#             return Response({
#                 'message': f"Account with email {request.GET['email']} doesn't exist",
#                 'success': False
#             }, status=400)
#         else:
#             response = _user.InitPasswordReset(
#                 request, lang, request.GET["email"])
#             if response["success"]:
#                 return Response(response)
#             else:
#                 return Response(response, status=400)


# Login User
class NewPasswordReset(ObtainAuthToken):
    def post(self, request, lang, userid):
        lang = DEFAULT_LANG if lang == None else lang
        if not str(userid):
            return Response({"message": "Incomplete data request", "success": False})
        #############################################
        data = request.data
        if data:
            ################################
            new_password = data["new_password"]
            confirm_password = data["confirm_password"]
            token = request.data["token"]
            # print(username)
            # print(password)
            if not new_password:
                return Response({
                    'message': "Password is required",
                    'success': False
                })
            elif len(new_password) < 6:
                return Response({
                    'message': "Password is too short, must atleast 6 characters or above",
                    'success': False
                })
            elif not confirm_password:
                return Response({
                    'message': "Confirmation password is required",
                    'success': False
                })
            elif not (confirm_password == new_password):
                return Response({
                    'message': "Passwords don't match",
                    'success': False
                })
            elif not _user.isVerificationTokenValid(request, lang, userid, token):
                return Response({"message": "Invalid verification code, either your code already expired or it is invalid", "success": False}, status=400)
            else:
                _user.UpdateAuthUserPassword(
                    request, lang, new_password, userid)
                _user.updateUserVerificationToken(request, lang, userid)
                return Response({"message": "Password updated successfully", "success": True})
        else:
            return Response({
                'message': "Incomplete data request",
                'success': False
            }, status=400)


class OnboardAuthUsers(ObtainAuthToken):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ['post']

    def post(self, request, lang):
        users = request.data
        if len(users) <= 0:
            return Response({
                "message": "No users in this databse",
                "success": False
            })
        else:
            for user in users:
                if not user["email"] or not user["first_name"] or not user["last_name"] or not user["password"] or not user["profile"]["created"] or not user["profile"]["birth_date"]:
                    return Response({
                        'message': "Something is missing",
                        "type": "required",
                        'success': False
                    })
                elif not user["profile"]["gender"]:
                    return Response({
                        'message': "gender is missing",
                        "type": "required",
                        'success': False
                    })
                elif not user["profile"]["country"]:
                    return Response({
                        'message': "country is missing",
                        "type": "required",
                        'success': False
                    })
                elif not user["profile"]["phoneno"]:
                    return Response({
                        'message': "phone is missing",
                        "type": "required",
                        'success': False
                    })
                else:
                    _user.onboardUsers(request, lang, user)
            number = len(users)
            return Response({
                "users": number,
                "message": "These users are now on board",
                "success": True
            })


class OnboardOrtusUsers(ObtainAuthToken):
    # need OTP created
    # need OTP emailed
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ['post']

    def post(self, request, lang):
        # dict array
        users = request.data
        if len(users) <= 0:
            return Response({
                "message": "No users in this database",
                "success": False
            })
        else:
            for user in users:
                if not user["email"] or not user["first_name"] or not user["last_name"] or not user["gender"] or not user["phone_no"] or not user["birth_date"]:
                    return Response({
                        'message': "Something is missing",
                        "type": "required",
                        'success': False
                    })
                elif not user["gender"]:
                    return Response({
                        'message': "gender is missing",
                        "type": "required",
                        'success': False
                    })
                elif not user["phone_no"]:
                    return Response({
                        'message': "phone is missing",
                        "type": "required",
                        'success': False
                    })
                else:
                    _user.onboardOrtusUsers(request, lang, user)
            number = len(users)
            return Response({
                "users": number,
                "message": "These users are now on board",
                "success": True
            })