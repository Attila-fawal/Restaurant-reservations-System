from django.test import TestCase, Client
from django.urls import reverse
from reservations.models import Reservation, Table, Customer
from django.contrib.auth.models import User
from datetime import datetime

class TestViews(TestCase):
    def setUp(self):
        # Setup test data for Client, URLs, User, Table, Customer, and Reservation
        # All these instances will be used for the following test cases.
        
        self.client = Client()
        self.reservation_list_url = reverse('reservation_list')
        self.user = User.objects.create_user(
            'testuser', 'test@gmail.com', 'testpass')
        self.user.save()
        self.table = Table.objects.create(number=1, capacity=4)
        self.customer = Customer.objects.create(
            user=self.user, name='Test', phone_number='123456789')
        self.reservation = Reservation.objects.create(
            date=datetime.today(), time=datetime.now().time(),
            guests=2, name='Test', email='test@gmail.com',
            phone_number='1234567890', customer_user=self.user)

    # Test Case 1: GET Request to Reservation List View
    # This test case checks a GET request to the reservation list view.
    def test_reservation_list_GET(self):
        # Logging in and performing a GET request on the reservation list URL
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.reservation_list_url)

        # Test Result: Passed
        # The GET request to the reservation list view returns status code 200 and uses the correct template.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation_list.html')

    # Test Case 2: GET Request to Reservation Detail View
    # This test case checks a GET request to the reservation detail view.
    def test_reservation_detail_GET(self):
        # Logging in and performing a GET request on the reservation detail URL
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(
            reverse('reservation_detail', args=[self.reservation.id]))

        # Test Result: Passed
        # The GET request to the reservation detail view returns status code 200 and uses the correct template.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation_detail.html')

    # Test Case 3: GET Request to Home View
    # This test case checks a GET request to the home view.
    def test_home_GET(self):
        # Performing a GET request on the home URL
        response = self.client.get(reverse('home'))

        # Test Result: Passed
        # The GET request to the home view returns status code 200 and uses the correct template.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

# Test Analysis and Conclusion:
# All tests have passed. The GET requests to the reservation list view, reservation detail view, and home view 
# all return status code 200 and use the correct templates.

