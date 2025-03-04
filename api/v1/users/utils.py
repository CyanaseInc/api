from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from ...models import *
import six

class TokenGenerator(PasswordResetTokenGenerator):
    
    # lets generate a state token
    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str:
        userid = user.pk
        user_profile = UserProfile.objects.get(pk=userid)
        return six.text_type(userid)+six.text_type(timestamp)+six.text_type(user_profile.is_verified)

generate_token = TokenGenerator()