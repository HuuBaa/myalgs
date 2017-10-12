from django.db import models

# Create your models here.
class User(models.Model):
    user_name=models.CharField(max_length=50)
    user_email=models.CharField(max_length=100)
    user_pass_hash=models.CharField(max_length=100)
    user_confirmed=models.BooleanField(default=0)