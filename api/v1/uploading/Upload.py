# All Things related to modules
from datetime import datetime
from django.core.validators import validate_email
from django.core.paginator import Paginator
from django.utils import timezone
from api.helper import helper
from api.models import *
from django.db.models import Count
from django.db.models import Q
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import os
from ..users.Users import Users
from api.config import webconfig
# helper class
import sys
import json

_user = Users()

# master module class
class Upload:
    def __init__(self):
        self.help = helper.Helper()

    def upload(self, output, file):
        destination = open(output, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        
    ##################
 