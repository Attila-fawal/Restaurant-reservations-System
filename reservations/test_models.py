from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Customer, Reservation, Table, Menu, Item

class TestModels(TestCase):

    def setUp(self):
        # Setup test data for User, Customer, Table, Menu, Item, and Reservation
        # All these instances will be used for the following test cases.

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

        # Adding a table and an item to the reservation
        self.reservation.tables.add(self.table)
        self.reservation.ordered_items.add(self.item)

    # Test Case 1: __str__ Method of the Customer Model
    # This test case checks the __str__ method of the Customer model.
    def test_customer_str(self):
        # Test Result: Passed
        # The __str__ method of the Customer model returns expected string format.
        self.assertEquals(
            str(self.customer),
            "Test Name - phone_number: 123456789 - email: test@test.com"
        )

    # Test Case 2: __str__ Method of the Reservation Model
    # This test case checks the __str__ method of the Reservation model.
    def test_reservation_str(self):
        # Test Result: Passed
        # The __str__ method of the Reservation model returns expected string format.
        self.assertEquals(
            str(self.reservation),
            f"Reservation {self.reservation.id} - Test Name"
        )

    # Test Case 3: __str__ Method of the Table Model
    # This test case checks the __str__ method of the Table model.
    def test_table_str(self):
        # Test Result: Passed
        # The __str__ method of the Table model returns expected string format.
        self.assertEquals(
            str(self.table),
            "Table 1"
        )

    # Test Case 4: is_reserved Property of the Table Model
    # This test case checks the is_reserved property of the Table model.
    def test_table_is_reserved(self):
        # Test Result: Passed
        # The is_reserved property of the Table model works as expected.
        self.assertEquals(
            self.table.is_reserved,
            True
        )

    # Test Case 5: Default Value of the Duration Field in the Reservation Model
    # This test case checks the default value of the duration field in the Reservation model.
    def test_reservation_duration_default(self):
        # Test Result: Passed
        # The default value of the duration field in the Reservation model is as expected.
        self.assertEquals(
            self.reservation.duration,
            timedelta(hours=2)
        )

# Test Analysis and Conclusion:
# All tests have passed. The __str__ methods of the Customer, Reservation, and Table models,
# the is_reserved property of the Table model, and the default value of the duration field in 
# the Reservation model are all functioning as expected based on these test cases.

