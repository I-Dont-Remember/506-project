from django.test import TestCase, Client
from django.test.utils import override_settings
from django.conf import settings

from users.models import CustomUser
from .models import App
from .sms import send, receive
from .api_handler import api_handler, wiki_handler

TWILIO_TRIAL = 'Sent from your Twilio trial account - '

class TestSmsSend(TestCase):
    '''
    Tests various cases for sending data from the server to Twilio
    '''
    def setUp(self):
        '''
        Test case setup
        '''
        # dummy objects for testings
        CustomUser.objects.create(username='dummy', phone='6306990113', twilio_phone='15005550006')
        App.objects.create(name='dummy')

    def test_basic_send(self):
        '''
        Test send that should succeed
        '''
        # fetch dummy objects
        user = CustomUser.objects.get(username='dummy')
        app = App.objects.get(name='dummy')

        # send text and verify return
        body = 'TestMessage Hi!'
        msg = send(user, app, body)
        self.assertEqual(msg.status, 'queued')
        self.assertEqual(msg.body, TWILIO_TRIAL + app.name + ',' + body)
        self.assertEqual(msg.to, '+1' + user.phone)

class TestSmsReceive(TestCase):
    '''
    Tests various cases for receiving ata from the server to Twilio
    '''
    def setUp(self):
        '''
        Test case setup
        '''
        CustomUser.objects.create(username='dummy', phone='6306990113', twilio_phone='15005550006')
        App.objects.create(name='dummy')

    def test_basic_receive(self):
        post_data = {'From': '+16306990113',
                     'Body': 'wikipedia,Potato'}
        c = Client()
        response = c.post('/sms/receive', post_data)
        self.assertEqual(response.status_code, 403)

class TestAPI(TestCase):
    '''
    Tests various external API calls and handler tests
    '''
    def setUp(self):
        '''
        Test case setup
        '''
        pass

    def test_wikipedia(self):
        '''
        Test wikipedia API
        '''
        # test good input
        summary = ('The potato is a starchy, tuberous crop from the perennial '
                   'nightshade Solanum tuberosum. Potato may be applied to both '
                   'the plant and the edible tuber. Pot...'
                  )
        self.assertEqual(summary, wiki_handler('potato'))

        # test bad input
        bad_word = 'THeresNoWayThis3xists'
        bad_summary = 'No Wikipedia entry found for ' + bad_word
        self.assertEqual(bad_summary, wiki_handler(bad_word))
