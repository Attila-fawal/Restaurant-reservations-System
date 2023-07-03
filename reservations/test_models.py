from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Customer, Reservation, Table, Menu, Item


class TestModels(TestCase):

    def setUp(self):
        # Create test instances of User, Customer, Table, Menu, Item,
        # and Reservation
        self.user = User.objects.create_user(
            'testuser', 'test@test.com', 'testpassword'
        )

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
        # Add a table and an item to the reservation
        self.reservation.tables.add(self.table)
        self.reservation.ordered_items.add(self.item)

    # Test the __str__ method of the Customer model
    def test_customer_str(self):
        self.assertEquals(
            str(self.customer),
            "Test Name - phone_number: 123456789 - email: test@test.com"
        )

    # Test the __str__ method of the Reservation model
    def test_reservation_str(self):
        self.assertEquals(
            str(self.reservation),
            f"Reservation {self.reservation.id} - Test Name"
        )

    # Test the __str__ method of the Table model
    def test_table_str(self):
        self.assertEquals(
            str(self.table),
            "Table 1"
        )

    # Test the is_reserved property of the Table model
    def test_table_is_reserved(self):
        self.assertEquals(
            self.table.is_reserved,
            True
        )

    # Test the default value of the duration field in the Reservation model
    def test_reservation_duration_default(self):
        self.assertEquals(
            self.reservation.duration,
            timedelta(hours=2)
        )
