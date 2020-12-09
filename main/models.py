from django.db import models

class MyCity(models.Model):
    city = models.CharField(max_length=200, primary_key=True)

class MyComplects(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    price = models.IntegerField()
    about = models.TextField()
    city = models.ForeignKey('MyCity', on_delete=models.CASCADE)


