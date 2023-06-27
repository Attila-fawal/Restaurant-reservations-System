from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15,)
    email = models.EmailField(max_length=200)

    def __str__(self):
       return self.name

class Table(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
    is_reserved = models.BooleanField(default=False)


class Menu(models.Model):
    name = models.CharField(max_length=200)


default_menu = Menu.objects.create(name="Default Menu")


class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)


class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    ordered_items = models.ManyToManyField(Item, blank=True)

    def cancel(self):
        self.reservationtable_set.all().update(table__is_reserved=False)
        self.delete()


class ReservationTable(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
