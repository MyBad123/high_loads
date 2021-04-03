from django.urls import path, include  
from .views import *
from .routers import router
from rest_framework.authtoken import views

urlpatterns = [
    path('main/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('home/', home), 
    path('create/', UserViews.as_view()), 
]


