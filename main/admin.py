from django.contrib import admin
from .models import CodeModel, ProductModel, ProductFavoriteModel, ReviewModel, BasketModel



admin.site.register(CodeModel)
admin.site.register(ProductModel)
admin.site.register(ProductFavoriteModel)
admin.site.register(ReviewModel)
admin.site.register(BasketModel)


