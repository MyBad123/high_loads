from django.contrib import admin
from django.urls import path

# my imports
from backend.views.products.views import ProductList, ProductSingleView, CategoryTreeView
from backend.views.cart.views import CartView, OrderingView

from backend.views.auth_view import AuthView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products', ProductList.as_view()),
    path('product', ProductSingleView.as_view()),
    path('categories', CategoryTreeView.as_view()),

    # for auth
    path('auth', AuthView.as_view()),
    path('cart', CartView.as_view()),
    path('order', OrderingView.as_view())
]
