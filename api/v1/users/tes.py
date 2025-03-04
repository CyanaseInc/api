from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .mailer import Mailer  # Assuming you have a Mailer class for sending emails
from .models import User  # Assuming your User model is in the same app
from .utils import encrypt_data  # Utility function to encrypt data

class LoginUserAuthToken(APIView):
    def post(self, request, lang):
        lang = DEFAULT_LANG if lang is None else lang
        data = request.data

        if not data:
            return Response({"message": "Invalid request method", "success": False}, status=400)

        username = data.get("username")
        password = data.get("password")

        if not username:
            return Response({"message": "Username is required", "success": False})
        elif not password:
            return Response({"message": "Password is required", "success": False})

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"message": "Invalid login credentials", "success": False})

        # Check if the user is verified
        if not user.profile.is_verified:
            # Generate a new verification code
            verification_code = self._generate_verification_code()
            user.profile.verification_code = verification_code
            user.profile.save()

            # Encrypt the verification code and user ID
            encrypted_verification_code = encrypt_data(verification_code)
            encrypted_userid = encrypt_data(str(user.pk))

            # Send verification email
            self._send_verification_email(user, encrypted_verification_code, encrypted_userid)

            return Response({
                "message": "Your account is not verified. A verification email has been sent.",
                "success": False,
                "user_id": user.pk,
            })

        # If the user is verified, generate and return the token
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.pk,
            "user": {
                "username": user.username,
                "email": user.email,
                "profile": {
                    "profile_id": user.profile.profile_id,
                    "is_verified": user.profile.is_verified,
                    # Add other profile fields as needed
                },
            },
            "message": "You are logged in",
            "success": True,
        })

    def _generate_verification_code(self):
        """
        Generate a random 6-digit verification code.
        """
        import random
        return str(random.randint(100000, 999999))

    def _send_verification_email(self, user, encrypted_verification_code, encrypted_userid):
        """
        Send a verification email to the user.
        """
        mailer = Mailer()  # Initialize your Mailer class
        current_site = "example.com"  # Replace with your domain

        # Prepare email content
        content = mailer.getEMailTemplateContent(
            "verify_account_email_template.html",
            {
                "user": user,
                "encrypted_verification_code": encrypted_verification_code,
                "encrypted_userid": encrypted_userid,
                "verificationcode": user.profile.verification_code,
                "domain": current_site,
            },
        )
        content2 = mailer.getEMailTemplateContent(
            "email_verification.html",
            {
                "user": user,
                "verificationcode": user.profile.verification_code,
            },
        )

        # Send the email
        mailer.sendHTMLEmail(user.email, "Please verify your account", content)