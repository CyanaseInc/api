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