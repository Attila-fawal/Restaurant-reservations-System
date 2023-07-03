from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Customer, Reservation, Table, Menu, Item


class TestModels(TestCase):

    def setUp(self):
        # Create instances for testing
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpassword')

        self.customer = Customer.objects.create(
            user=self.user,
            name='Test Name',
            phone_number='123456789',
            email='test@test.com',
        )

        self.table = Table.objects.create(
            number=1,
            capacity=4,
        )

        self.menu = Menu.objects.create(
            name='Test Menu'
        )

        self.item = Item.objects.create(
            name='Test Item',
            price=10.99,
            menu=self.menu,
        )

        self.reservation = Reservation.objects.create(
            date=datetime.now().date(),
            time=datetime.now().time(),
            guests=2,
            name='Test Name',
            email='test@test.com',
            phone_number='123456789',
            customer_user=self.user,
        )
        self.reservation.tables.add(self.table)
        self.reservation.ordered_items.add(self.item)

    def test_customer_str(self):
        self.assertEquals(str(self.customer), "Test Name - phone_number: 123456789 - email: test@test.com")

    def test_reservation_str(self):
        self.assertEquals(str(self.reservation), f"Reservation {self.reservation.id} - Test Name")

    def test_table_str(self):
        self.assertEquals(str(self.table), "Table 1")

    def test_table_is_reserved(self):
        self.assertEquals(self.table.is_reserved, True)

    def test_reservation_duration_default(self):
        self.assertEquals(self.reservation.duration, timedelta(hours=2))
