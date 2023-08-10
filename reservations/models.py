from django.contrib.auth.models import User
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse


class Customer(models.Model):
    """
    Customer model representing a customer in the restaurant.
    It has a one-to-one relationship with the User model from Django's
    auth module, and fields for name, phone number, and email.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.name} - phone_number: {self.phone_number} - \
email: {self.email}"


class Reservation(models.Model):
    """
    Reservation model representing a reservation in the restaurant.
    It contains fields for date, time, number of guests, name, email,
    phone number, ordered items, tables, associated customer,
    and the duration of the reservation.
    """
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    ordered_items = models.ManyToManyField('Item', blank=True)
    tables = models.ManyToManyField(
        'Table',
        related_name='related_reservations',
        blank=True
    )
    customer_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    duration = models.DurationField(default=timedelta(hours=2))

    def __str__(self):
        return f"Reservation {self.id} - {self.name}"


class Table(models.Model):
    """
    Table model representing a table in the restaurant.
    It contains fields for the table number, its capacity,
    whether it's reserved, and its related reservations.
    """
    number = models.IntegerField()
    capacity = models.IntegerField()
    is_reserved = models.BooleanField(default=False)
    reservations = models.ManyToManyField(
        'Reservation',
        related_name='related_tables',
        blank=True
    )

    @property
    def is_reserved(self):
        """
        Check if the table is reserved by examining its reservations.
        The table is considered reserved if there is a reservation
        today that starts before and ends after the current time.
        """
        now = timezone.localtime()
        reservations_today = self.related_reservations.filter(
            date=now.date()
        )

        for reservation in reservations_today:
            combined_datetime = timezone.make_aware(
                timezone.datetime.combine(
                    reservation.date,
                    reservation.time
                )
            )
            reservation_end_time = combined_datetime + reservation.duration
            reservation_end_time = timezone.localtime(
                reservation_end_time
            )
            if reservation.time <= now.time() <= reservation_end_time.time():
                return True

        return False

    def __str__(self):
        return f'Table {self.number}'


class Menu(models.Model):
    """
    Menu model representing a menu in the restaurant.
    It only contains a single field for the name of the menu.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    Item model representing an item in the restaurant's menu.
    It contains fields for the item's name, price,
    and the menu it belongs to.
    """
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name} - Price: {self.price} - Menu: {self.menu}"
