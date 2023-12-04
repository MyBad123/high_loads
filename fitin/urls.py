from django.contrib import admin
from django.urls import path

# my imports
from backend.views.products.views import ProductList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products', ProductList.as_view())
]
