from .models import CodeModel, ProductModel, ProductFavoriteModel, ReviewModel, BasketModel

import random
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.shortcuts import render 
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken

#for decorators
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

#for work with mail 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#for exept 
from django.core.exceptions import ObjectDoesNotExist

class FavouriteView(APIView):
    def post(self, request):
        try: 
            f_user = User.objects.get(username=str(request.data.get('username')))
            f_products = ProductFavoriteModel.objects.filter(favorite_user=f_user)
            products = []
            for i in f_products:
                products.append(i.favorite_product.product_name)
            return Response(data={"products": products}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_200_OK)


#for register
class CustomAuthToken(ObtainAuthToken):
    def post(self, request):
        try: 
            u_name = str(request.data.get('username'))
            u_mail = str(request.data.get('email'))
            u_pass = str(request.data.get('password'))
            user = User.objects.create_user(u_name, u_mail, u_pass)
            user.save()
            auth_user = authenticate(username=u_name, password=u_pass)
            if auth_user is not None:
                Token.objects.create(user=User.objects.get(username=u_name, email=u_mail))
                #work with code 
                your_code = str(random.randint(1000, 9999))
                your_code_data = CodeModel()
                your_code_data.code_user = User.objects.get(username=u_name, email=u_mail)
                your_code_data.code_code = your_code
                your_code_data.save()
                #work with mail 
                email_msg = MIMEMultipart()
                email_to = u_mail
                email_message = 'code is ' + your_code
                email_msg.attach(MIMEText(email_message, 'plain'))
                email_server = smtplib.SMTP('smtp.mail.ru: 25')
                email_server.starttls()
                email_server.login("gena.kuznetsov.1990@mail.ru", "")
                email_server.sendmail("gena.kuznetsov.1990@mail.ru", email_to, email_msg.as_string())
                email_server.quit()

                return Response(status=status.HTTP_200_OK)
            else: 
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
#email for new users   
@api_view(['POST'])
@permission_classes([AllowAny])
def your_email(request):
    try: 
        code = str(request.data.get('code'))
        u_name = str(request.data.get('username'))
        u_pass = str(request.data.get('password'))
        auth_user = authenticate(username=u_name, password=u_pass)
        code_get = CodeModel.objects.get(code_user=auth_user, code_code=code)
        code_get.code_code = str(random.randint(1000, 9999))
        code_get.save()
        my_token = Token.objects.get(user=auth_user)
        return Response(data={"data": my_token.key}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_304_NOT_MODIFIED)

#for old users 
@api_view(['POST'])
@permission_classes([AllowAny])
def for_uauth(request):
    try: 
        u_name = str(request.data.get('username'))
        u_pass = str(request.data.get('password'))
        auth_user = authenticate(username=u_name, password=u_pass)
        my_token = Token.objects.get(user=auth_user)

        return Response(data={"data": my_token.key}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_304_NOT_MODIFIED)











