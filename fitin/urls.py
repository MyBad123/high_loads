from django.contrib import admin
from django.urls import path

# my imports
from backend.views.products.views import ProductList
from backend.views.cart.views import CartView

from backend.views.auth_view import AuthView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products', ProductList.as_view()),

    # for auth
    path('auth', AuthView.as_view()),
    path('cart', CartView.as_view()),
]
