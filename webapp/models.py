from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField()
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=5)
    registerdate = models.DateField(auto_now_add=True)




