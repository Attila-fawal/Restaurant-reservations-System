from django import forms
from django.utils import timezone
from .models import Reservation
import datetime
from django.utils import timezone


class ReservationForm(forms.ModelForm):
    time = forms.TimeField(input_formats=['%I:%M %p'], widget=forms.TimeInput(format='%I:%M %p', attrs={'class': 'timepicker'}))

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'name', 'email', 'phone_number']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
        }


    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and timezone.localtime() > timezone.make_aware(datetime.datetime.combine(date, datetime.time())):
            raise forms.ValidationError("The date and time cannot be in the past!")
        return date
