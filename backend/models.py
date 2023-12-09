from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """"""

    name = models.CharField(max_length=50)


class Product(models.Model):
    """model for product"""

    name = models.CharField(max_length=50, unique=True, null=False)
    about = models.TextField()
    price = models.IntegerField()


class CategoryForProduct(models.Model):
    """model for category and product (together)"""

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """control duplicates"""

        try:
            CategoryForProduct.objects.get(
                category=self.category, product=self.product)

            raise ValueError('such data exists')
        except self.DoesNotExist:
            super().save(force_insert=force_insert, force_update=force_update,
                         using=using, update_fields=update_fields)


class CartModel(models.Model):
    """model for user's cart with products"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """control duplicates"""

        try:
            CartModel.objects.get(user=self.user, product=self.product)
            raise ValueError('such data exists')

        except self.DoesNotExist:
            super().save(force_insert=force_insert, force_update=force_update,
                         using=using, update_fields=update_fields)


class OrderModel(models.Model):
    """"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ProductsInOrderModel(models.Model):
    """"""

    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
