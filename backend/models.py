from django.db import models


class Product(models.Model):
    """model for product"""

    name = models.CharField(max_length=50, unique=True, null=False)
    about = models.TextField()
    price = models.IntegerField()
