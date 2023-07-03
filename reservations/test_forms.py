from django.test import TestCase
from django.contrib.auth.models import User
from reservations.forms import (
    UserRegisterForm, CustomerProfileUpdateForm, ReservationForm
)
from reservations.models import Customer, Reservation, Item, Table
import datetime


class TestForms(TestCase):

    # Testing the user registration form with valid data
    def test_user_register_form_valid_data(self):
        form = UserRegisterForm(data={
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })

        # Assert that the form is valid
        self.assertTrue(form.is_valid())

    # Testing the customer profile update form with valid data
    def test_customer_profile_update_form_valid_data(self):
        # Creating a test user and customer
        user = User.objects.create_user(
            'testuser', 'testemail@test.com', 'testpass123'
        )
        customer = Customer.objects.create(
            user=user, name='test', phone_number='123456789'
        )

        # Creating and testing the form with updated customer data
        form = CustomerProfileUpdateForm(
            instance=customer, data={
                'name': 'newtest',
                'phone_number': '987654321'
            }
        )

        # Assert that the form is valid
        self.assertTrue(form.is_valid())
        # Assert that the cleaned_data attribute contains the updated data
        self.assertEquals(form.cleaned_data.get('name'), 'newtest')
        self.assertEquals(
            form.cleaned_data.get('phone_number'), '987654321'
        )

    # Testing the reservation form's clean_date method with a date in the past
    def test_reservation_form_clean_date(self):
        # Creating the form with a date in the past
        form = ReservationForm(data={
            'date': datetime.date.today() - datetime.timedelta(days=1),
            'time': '12:00 AM',
            'guests': 2,
            'name': 'testname',
            'email': 'testemail@test.com',
            'phone_number': '123456789',
        })

        # Assert that the form is invalid due to the date being in the past
        self.assertFalse(form.is_valid())
        # Assert that the error message is as expected
        self.assertEquals(
            form.errors['date'], ['The date and time cannot be in the past!']
        )
