from django.test import TestCase, Client
from django.urls import reverse
from reservations.models import Reservation, Table, Customer, Item
from django.contrib.auth.models import User
from datetime import datetime

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.reservation_list_url = reverse('reservation_list')
        self.user = User.objects.create_user('testuser', 'test@gmail.com', 'testpass')
        self.user.save()
        self.table = Table.objects.create(number=1, capacity=4)
        self.customer = Customer.objects.create(user=self.user, name='Test', phone_number='123456789')
        self.reservation = Reservation.objects.create(
            date=datetime.today(), 
            time=datetime.now().time(), 
            guests=2, 
            name='Test', 
            email='test@gmail.com', 
            phone_number='1234567890', 
            customer_user=self.user
        )

    def test_reservation_list_GET(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.reservation_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation_list.html')

    def test_reservation_detail_GET(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('reservation_detail', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation_detail.html')

    def test_home_GET(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
