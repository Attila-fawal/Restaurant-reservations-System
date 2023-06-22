from django.contrib import admin
from .models import Customer, Table, Reservation

admin.site.register(Customer)
admin.site.register(Table)
admin.site.register(Reservation)
