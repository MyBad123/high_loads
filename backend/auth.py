import jwt
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.request import Request
from django.conf import settings


class TokenAuthentication(authentication.BaseAuthentication):
    """custom authentication by token"""

    def authenticate(self, request: Request):
        token_header: str = request.META.get('HTTP_AUTHORIZATION')

        if token_header:
            if len(token_header.split()) == 2:
                try:
                    user_data = jwt.decode(token_header.split()[1], settings.SECRET_KEY, algorithms=["HS256"])
                    user = User.objects.get(username=user_data.get('username'))

                    return user, None
                except (User.DoesNotExist, jwt.exceptions.PyJWTError):
                    pass

        return None
