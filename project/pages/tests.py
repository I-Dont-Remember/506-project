from django.test import TestCase, Client
from django.urls import reverse

from users.models import CustomUser

class TestRendering(TestCase):
    '''
    Tests various cases for sending data from the server to Twilio
    '''
    def setUp(self):
        '''
        Test case setup
        '''
        self.c = Client()
        CustomUser.objects.create(username='dummy',password='123456789Test')


    def test_home(self):
        '''
        Test rendering home page
        '''
        response = self.c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_us(self):
        '''
        Test rendering about us page
        '''
        response = self.c.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)

    def test_clients(self):
        '''
        Test rendering clients page
        '''
        response = self.c.get(reverse('clients'))
        self.assertEqual(response.status_code, 200)

    def test_profile_bad(self):
        '''
        Test rendering profile page while not logged in
        '''
        response = self.c.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
