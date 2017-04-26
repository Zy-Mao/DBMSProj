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
    room_no = models.CharField(max_length=5, primary_key=True)
    hotel = models.ForeignKey(Hotel_Detail, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    price = models.FloatField()
    description = models.CharField(max_length=200)

    class Meta:
        unique_together = (('room_no', 'hotel'),)

class Order(models.Model):
    order_type = models.CharField(max_length=1)
    total_amount = models.FloatField()
    user_id = models.ForeignKey(User_Detail, on_delete=models.CASCADE)
    order_date = models.DateField()

class Hotel_Order(models.Model):
    # PK: auto generated
    hotel_room = models.ForeignKey(Hotel_Room, on_delete=models.CASCADE)
    indate = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.IntegerField()


class Train(models.Model):
    train_no = models.CharField(max_length=10, primary_key=True)
    departure_city = models.CharField(max_length=20)
    arrival_city = models.CharField(max_length=20)
    departure_time = models.DateField(null=True)
    type = models.CharField(max_length=10)
    ticket_amount = models.IntegerField()

    def __str__(self):
        return self.train_no + ", From " + self.departure_city + ", To " + self.arrival_city


class Train_Schedule(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    arrival_city = models.CharField(max_length=20)
    price = models.FloatField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return self.train.train_no + ", To " + self.arrival_city


class Train_Order(models.Model):
    user = models.ForeignKey(User_Detail, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField()


class Train_Sub_Order(models.Model):
    order_no = models.AutoField(primary_key=True)
    departure_city = models.ForeignKey(Train_Schedule, on_delete=models.CASCADE, related_name="departure_train_schedule")
    arrival_city = models.ForeignKey(Train_Schedule, on_delete=models.CASCADE, related_name="arrival_train_schedule")
    train = models.ForeignKey(Train, on_delete=models.CASCADE)


class City(models.Model):
    cid = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    abb_state = models.CharField(max_length=10)

    def __str__(self):
        return self.city + ", " + self.state + ", " + self.abb_state

