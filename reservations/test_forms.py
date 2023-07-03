from django.test import TestCase
from django.contrib.auth.models import User
from reservations.forms import UserRegisterForm, CustomerProfileUpdateForm, ReservationForm
from reservations.models import Customer, Reservation, Item, Table
import datetime


class TestForms(TestCase):

    def test_user_register_form_valid_data(self):
        form = UserRegisterForm(data={
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })

        self.assertTrue(form.is_valid())

    def test_customer_profile_update_form_valid_data(self):
        user = User.objects.create_user('testuser', 'testemail@test.com', 'testpass123')
        customer = Customer.objects.create(user=user, name='test', phone_number='123456789')

        form = CustomerProfileUpdateForm(instance=customer, data={
            'name': 'newtest',
            'phone_number': '987654321'
        })

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data.get('name'), 'newtest')
        self.assertEquals(form.cleaned_data.get('phone_number'), '987654321')

    def test_reservation_form_clean_date(self):
        form = ReservationForm(data={
            'date': datetime.date.today() - datetime.timedelta(days=1),  # date in the past
            'time': '12:00 AM',
            'guests': 2,
            'name': 'testname',
            'email': 'testemail@test.com',
            'phone_number': '123456789',
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['date'], ['The date and time cannot be in the past!'])
