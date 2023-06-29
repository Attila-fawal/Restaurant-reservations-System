from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from .models import Reservation, Item, Table
from datetime import timedelta
import datetime
import re
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ReservationForm(forms.ModelForm):
    ordered_items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    time = forms.TimeField(input_formats=['%I:%M %p'])
    guests = forms.IntegerField(min_value=1, max_value=40)

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'guests', 'name', 'email', 'phone_number', 'ordered_items']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'time': forms.TimeInput(format='%I:%M %p', attrs={'class': 'timepicker'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise ValidationError("Phone number can only contain digits.")
        return phone_number

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and bool(re.search(r'\d', name)):
            raise ValidationError("Name cannot contain numbers.")
        return name

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and timezone.localtime() > timezone.make_aware(datetime.datetime.combine(date, datetime.time())):
            raise forms.ValidationError("The date and time cannot be in the past!")
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        guests = cleaned_data.get('guests')

        # Determine the number of tables needed based on guests number
        tables_needed = (guests + 1) // 2

        # Convert time to datetime, add two hours, and convert back to time
        now = timezone.localtime()
        time_datetime = datetime.datetime.combine(now, time)
        new_time_datetime = time_datetime + timedelta(hours=2)
        new_time = new_time_datetime.time()

        # Fetch all tables that are available during the desired reservation time
        available_tables = Table.objects.exclude(
            reservations__date=date,
            reservations__time__range=(time, new_time)
        )

        # Check if enough tables are available
        if available_tables.count() < tables_needed:
            self.add_error(None, f"There are not enough tables available at this time.")
            return cleaned_data

        # Select the necessary number of tables and assign them to the reservation
        selected_tables = available_tables[:tables_needed]
        cleaned_data['tables'] = selected_tables

        return cleaned_data