from django.db import models
from django.contrib.auth.models import User

class Snippet(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CodeModel(models.Model):
    code_user = models.ForeignKey(User, on_delete=models.CASCADE)
    code_code = models.CharField(max_length=4)
