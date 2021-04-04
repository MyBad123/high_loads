from .models import CodeModel, ProductModel, ProductFavoriteModel, ReviewModel, BasketModel

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
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
                return Response(status=status.HTTP_200_OK)
            else: 
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
#for email 
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def your_email(request):
    
    my_token = Token.objects.get(user=User.objects.get(username=u_name, email=u_mail))
    return Response(data={"data": my_token.key}, status=status.HTTP_200_OK)


'''
work with mail:
 mailMsg = MIMEMultipart()
mailTo = userMail
mailMessage = 'login: ' + newINN + ' password: ' + userPass
mailMsg.attach(MIMEText(mailMessage, 'plain'))
mailServer = smtplib.SMTP('smtp.mail.ru: 25')
mailServer.starttls()
mailServer.login('gena.kuznetsov@internet.ru', 'o%pdUaeIUI12')
mailServer.sendmail('gena.kuznetsov@internet.ru', mailTo, mailMsg.as_string())
mailServer.quit()

return key: 
my_token = Token.objects.get(user=User.objects.get(username=u_name, email=u_mail))
return Response(data={"data": my_token.key}, status=status.HTTP_200_OK)
'''
