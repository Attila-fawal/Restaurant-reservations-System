from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from .models import Reservation, Item, Table
import datetime


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
    tables = forms.ModelMultipleChoiceField(
        queryset=Table.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    time = forms.TimeField(input_formats=['%I:%M %p'])

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'guests', 'name', 'email', 'phone_number', 'ordered_items', 'tables']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'time': forms.TimeInput(format='%I:%M %p', attrs={'class': 'timepicker'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and timezone.localtime() > timezone.make_aware(datetime.datetime.combine(date, datetime.time())):
            raise forms.ValidationError("The date and time cannot be in the past!")
        return date

    def clean(self):
        cleaned_data = super().clean()
        tables = cleaned_data.get('tables')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if tables:
            for table in tables:
                overlapping_reservations = Reservation.objects.filter(
                    Q(date=date) & Q(time=time) & Q(tables=table)
                )
                if overlapping_reservations.exists():
                    self.add_error(None, f"Table {table.number} is already reserved at this time.")
        else:
            self.add_error(None, "No tables associated with this reservation.")

        return cleaned_data
