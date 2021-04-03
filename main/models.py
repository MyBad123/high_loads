from django.db import models
from django.contrib.auth.models import User

class CodeModel(models.Model):
    code_user = models.ForeignKey(User, on_delete=models.CASCADE)
    code_code = models.CharField(max_length=4)


#work with shop 
class ProductModel(models.Model):
    product_name = models.CharField(max_length=100, primary_key=True)
    product_category = models.CharField(max_length=20)
    product_price = models.IntegerField()
    product_sale = models.IntegerField()
    prouct_rating = models.IntegerField()
    prouct_description = models.TextField()
    prouct_sales = models.IntegerField()

class ProductFavoriteModel(models.Model):
    favorite_user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

class ReviewModel(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    review_rating = models.IntegerField()
    review_description = models.TextField()
    review_time = models.DateField(auto_now_add=True)

class BasketModel(models.Model):
    basket_user = models.ForeignKey(User, on_delete=models.CASCADE)
    basket_product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    basket_quantity = models.IntegerField()








