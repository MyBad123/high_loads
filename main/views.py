from .models import Snippet
from .serializer import SnippetSerializer
from rest_framework import viewsets, status

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.shortcuts import render 
from rest_framework.response import Response
from django.contrib.auth import authenticate

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

def home(request):
    return render(request, 'hemo.html')

class UserViews(APIView):
    def post(self, request):
        u_name = str(request.data.get('username'))
        u_mail = str(request.data.get('email'))
        u_pass = str(request.data.get('password'))
        user = User.objects.create_user(u_name, u_mail, u_pass)
        user.save()
        auth_user = authenticate(username=u_name, password=u_pass)
        if auth_user is not None:
            Token.objects.create(user=User.objects.get(username=u_name, email=u_mail))
            return Response(status=status.HTTP_200_OK)
        else: 
            return Response(status=status.HTTP_400_BAD_REQUEST)




