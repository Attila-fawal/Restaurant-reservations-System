from django.test import TestCase
from django.contrib.auth.models import User
from reservations.forms import (
    UserRegisterForm, CustomerProfileUpdateForm, ReservationForm
)
from reservations.models import Customer, Reservation, Item, Table
import datetime


class TestForms(TestCase):
    # Test Case 1: User Registration Form with Valid Data
    # This test case checks the UserRegisterForm with valid data.
    def test_user_register_form_valid_data(self):
        form = UserRegisterForm(data={
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })

        # Test Result: Passed
        # The UserRegisterForm correctly handles valid data.
        self.assertTrue(form.is_valid())

    # Test Case 2: Customer Profile Update Form with Valid Data
    # This test case checks the CustomerProfileUpdateForm with valid data.
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

        # Test Result: Passed
        # The CustomerProfileUpdateForm correctly handles valid data and updates the customer profile.
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data.get('name'), 'newtest')
        self.assertEquals(
            form.cleaned_data.get('phone_number'), '987654321'
        )

    # Test Case 3: Reservation Form with Past Date
    # This test case checks the ReservationForm with a date in the past.
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

        # Test Result: Passed
        # The ReservationForm correctly rejects dates in the past and returns the expected error message.
        self.assertFalse(form.is_valid())
        self.assertEquals(
            form.errors['date'], ['The date and time cannot be in the past!']
        )     
# Test Analysis and Conclusion:
# All tests have passed. The UserRegisterForm, CustomerProfileUpdateForm, and ReservationForm
# are all functioning as expected based on these test cases.
