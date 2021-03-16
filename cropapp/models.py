from django.db import models

# Create your models here.
class userregister(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    uname=models.CharField(max_length=100,unique=True)
    pwd=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=13,unique=True)
