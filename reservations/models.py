from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)


class Table(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()


class Booking(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
