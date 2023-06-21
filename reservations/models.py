from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime


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
    tables = models.ManyToManyField(Table)  # Many-to-many relationship
    cancelled = models.BooleanField(default=False)

    def clean(self):
        # Check for double bookings
        if self.tables.filter(reservation__date=self.date, reservation__time=self.time).exists():
            raise ValidationError(_('The table is already booked at this time.'))

        # Check for over capacity
        if self.guests > self.tables.aggregate(models.Sum('capacity'))['capacity__sum']:
            raise ValidationError(_('The number of guests exceeds the tables\' capacity.'))

    def cancel(self):
        self.cancelled = True
        self.save()


class Booking(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    time_slot = models.DateTimeField(default=datetime.now)
