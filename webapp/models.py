from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_Detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.EmailField()
    # firstname = models.CharField(max_length=50)
    # lastname = models.CharField(max_length=50)
    # password = models.CharField(max_length=50)
    # gender = models.CharField(max_length=1)
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=5)
    # registerdate = models.DateField(auto_now_add=True)


class Hotel_Detail(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=200)


class Hotel_Room(models.Model):
    # PK: auto generated
    room_no = models.CharField(max_length=5)
    hotel = models.ForeignKey(Hotel_Detail, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    price = models.FloatField()
    description = models.CharField(max_length=200)

    class Meta:
        unique_together = (('room_no', 'hotel'),)


# class Hotel_Order(models.Model):
#     room_id = models.CharField(max_length=5)
#     hotel_id = models.ForeignKey(Hotel_Detail, on_delete=models.CASCADE)
#     date = models.DateTimeField()
#     user_id = models.ForeignKey(User_Detail, on_delete=models.CASCADE)


class Train(models.Model):
    train_no = models.CharField(max_length=10, primary_key=True)
    departure_city = models.CharField(max_length=20)
    arrival_city = models.CharField(max_length=20)
    type = models.CharField(max_length=10)
    ticket_amount = models.IntegerField()


class Train_Schedule(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    arrival_city = models.CharField(max_length=20)
    price = models.FloatField()
    arrival_time = models.DateTimeField()