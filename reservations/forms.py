from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'table', 'capacity', 'customer_name', 'customer_email', 'customer_phone_number']
