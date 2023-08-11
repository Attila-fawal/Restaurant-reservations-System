from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm
)
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from .models import (
    Reservation,
    Item,
    Table,
    Customer
)
from datetime import timedelta
import datetime
import re
from django.core.exceptions import ValidationError


class ProfileUpdateForm(forms.ModelForm):
    """
    Form to update the profile of an existing User instance.
    Includes 'username' and 'email' fields from the User model.
    """
    class Meta:
        model = User
        fields = ['username', 'email']


class UserRegisterForm(UserCreationForm):
    """
    Form used for registering a new user.
    Extends the UserCreationForm with an 'email' field.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerProfileUpdateForm(forms.ModelForm):
    """
    Form to update the profile of an existing Customer instance.
    Includes 'name' and 'phone_number' fields from the Customer model.
    """
    class Meta:
        model = Customer
        fields = ['name', 'phone_number']


class ReservationForm(forms.ModelForm):
    """
    Form to create or update a Reservation instance.
    Includes validation for 'phone_number', 'name' and 'date' fields.
    Also includes a method to determine table availability
    and assign tables to the reservation.
    """
    ordered_items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    time = forms.TimeField(input_formats=['%I:%M %p'])
    guests = forms.IntegerField(min_value=1, max_value=40)

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'guests', 'name', 'email',
                  'phone_number', 'ordered_items']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'time': forms.TimeInput(
                format='%I:%M %p',
                attrs={'class': 'timepicker'}
            ),
        }

    def clean_phone_number(self):
        """
        Validate 'phone_number' field.
        Ensure phone number contains only digits.
        """
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise ValidationError("Phone number can only contain digits.")
        return phone_number

    def clean_name(self):
        """
        Validate 'name' field.
        Ensure the name does not contain numbers.
        """
        name = self.cleaned_data.get('name')
        if name and bool(re.search(r'\d', name)):
            raise ValidationError("Name cannot contain numbers.")
        return name

    def clean_date(self):
        """
        Validate 'date' field.
        Ensure the reservation date is not in the past.
        """
        date = self.cleaned_data.get('date')
        if date and timezone.localtime() > timezone.make_aware(
            datetime.datetime.combine(date, datetime.time())
        ):
            raise forms.ValidationError(
                "The date and time cannot be in the past!"
            )
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        guests = cleaned_data.get('guests')

        if not date or not time:
            return cleaned_data

        tables_needed = (guests + 1) // 2

        now = timezone.localtime()
        time_datetime = datetime.datetime.combine(now, time)
        new_time_datetime = time_datetime + timedelta(hours=2)
        new_time = new_time_datetime.time()

        available_tables = Table.objects.exclude(
            reservations__date=date,
            reservations__time__range=(time, new_time)
        )

        if self.instance.pk:
            available_tables = available_tables.exclude(reservations=self.instance)

        if available_tables.count() < tables_needed:
            self.add_error(
                None,
                "Not enough tables available at this time."
            )
            return cleaned_data

        selected_tables = available_tables[:tables_needed]
        cleaned_data['tables'] = selected_tables

        return cleaned_data
