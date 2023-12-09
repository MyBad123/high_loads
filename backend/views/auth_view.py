import jwt
import time
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.conf import settings


class AuthView(APIView):
    """api method for auth"""

    permission_classes = [permissions.AllowAny]

    def get(self, request: Request):
        user = User.objects.create(username=str(int(time.time())))

        return Response(data={
            'token': jwt.encode({'username': user.username}, settings.SECRET_KEY, algorithm="HS256")
        })
