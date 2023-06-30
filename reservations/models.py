from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.name} - phone_number: {self.phone_number} - email: {self.email}"


class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    ordered_items = models.ManyToManyField('Item', blank=True)  # using 'Item' as string
    tables = models.ManyToManyField('Table', related_name='related_reservations', blank=True)
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    duration = models.DurationField(default=timedelta(hours=2)) # default is 2 hours

    def __str__(self):
        return f"Reservation {self.id} - {self.name}"


class Table(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
    is_reserved = models.BooleanField(default=False)
    reservations = models.ManyToManyField('Reservation', related_name='related_tables', blank=True)
    
    @property
    def is_reserved(self):
        now = timezone.localtime()
        reservations_today = self.related_reservations.filter(date=now.date())

        for reservation in reservations_today:
            combined_datetime = timezone.make_aware(timezone.datetime.combine(reservation.date, reservation.time))
            reservation_end_time = combined_datetime + reservation.duration
            reservation_end_time = timezone.localtime(reservation_end_time)
            if reservation.time <= now.time() <= reservation_end_time.time():
                return True

        return False

    def __str__(self):
        return f'Table {self.number}'


class Menu(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.name} - Price: {self.price} - Menu: {self.menu}"
