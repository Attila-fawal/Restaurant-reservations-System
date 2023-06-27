from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Reservation, Item
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
    time = forms.TimeField(input_formats=['%I:%M %p'])
    
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'guests', 'name', 'email', 'phone_number', 'ordered_items']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'time': forms.TimeInput(format='%I:%M %p', attrs={'class': 'timepicker'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and timezone.localtime() > timezone.make_aware(datetime.datetime.combine(date, datetime.time())):
            raise forms.ValidationError("The date and time cannot be in the past!")
        return date

