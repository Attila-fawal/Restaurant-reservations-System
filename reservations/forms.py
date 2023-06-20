from django import forms
from .models import Reservation, Table


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer', 'date', 'time', 'guests', 'tables']

    def clean(self):
        cleaned_data = super().clean()
        guests = cleaned_data.get('guests')

        # Access the tables related to the reservation
        tables = cleaned_data.get('tables')

        if tables:
            # Calculate the total capacity of the tables
            total_capacity = sum(table.capacity for table in tables)

            if guests > total_capacity:
                raise forms.ValidationError("The number of guests exceeds the tables' capacity.")

        # Check for double booking
        if any(table.reservation_set.filter(date=cleaned_data.get('date'), time=cleaned_data.get('time')).exists() for table in tables):
            raise forms.ValidationError("One or more of the selected tables is already booked at this time.")

        return cleaned_data
