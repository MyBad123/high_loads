from django.urls import path, include  
from .views import *
#from .routers import router
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', CustomAuthToken.as_view()),
    path('favorite/', FavouriteView.as_view()),
    path('mail/', your_email),
    path('authorization/', for_uauth),
    path('products/', all_products),
    path('products/<int:pk>/', one_product),
    path('categories/', all_categories),
    path('categories/<str:pk>', one_categories),
]


