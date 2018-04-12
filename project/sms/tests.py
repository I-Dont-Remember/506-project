from django.test import TestCase, Client
from django.test.utils import override_settings
from django.conf import settings

from users.models import CustomUser
from .models import App
from .sms import send, receive
from .api_handler import api_handler, wiki_handler, dir_handler, weather_handler, sports_handler

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
        self.app = App.objects.create()

    def test_wikipedia(self):
        '''
        Test wikipedia API
        '''
        self.app.name = 'wikipedia'
        # test good input
        summary = ('The potato is a starchy, tuberous crop from the perennial '
                   'nightshade Solanum tuberosum. Potato may be applied to both '
                   'the plant and the edible tuber. Pot...'
                  )
        #self.assertEqual(summary, wiki_handler('potato'))
        self.assertEqual(summary, api_handler(self.app, 'potato'))

        # test bad input
        bad_word = 'THeresNoWayThis3xists'
        bad_summary = 'No Wikipedia entry found for ' + bad_word
        self.assertEqual(bad_summary, wiki_handler(bad_word))

    def test_directions(self):
        '''
        Test directions API
        '''
        self.app.name = 'directions'
        #test good input of addresses for origin and destination
        directions = ('(112 ft) Head northeast on Adams St toward S Randall Ave;'
                      '(0.3 mi) Turn left onto S Randall Ave. Destination will '
                      'be on the right')
        route = "1512 Adams St, Madison WI;215 N Randall Ave, Madison WI"
        self.assertEqual(directions, dir_handler(route))

        #test good input of lat/lng coordinates for origin and destination
        route = "43.066664,-89.409532;43.071456,-89.408663"
        self.assertEqual(directions, dir_handler(route))

        #test good input of address for origin and lat/lng for destination
        route = "1512 Adams St, Madison WI;43.071456,-89.408663"
        self.assertEqual(directions, dir_handler(route))

        #test good input of lat/lng for origin and address for destination
        route = "43.066664,-89.409532;215 N Randall Ave, Madison WI"
        self.assertEqual(directions, dir_handler(route))

        #test bad input
        bad_route = "some place that doesn't exist;45"
        bad_directions = "Directions not found for " + bad_route[:29] + " to " + bad_route[30:]
        self.assertEqual(bad_directions, dir_handler(bad_route))

    def test_weather(self):
        '''
        Test weather API
        '''
        self.app.name = 'weather'
        address = '215 N Randall Ave, Madison WI'
        coordinates = '43.071456,-89.408663'

        #test good input of address for 24-hour forecast
        response = weather_handler('a2' + address)
        response = response.split('/')
        self.assertEqual(24, len(response))

        #test good input of coordinates for 24-hour forecast
        response = weather_handler('c2' + coordinates)
        response = response.split('/')
        self.assertEqual(24, len(response))

        #test good input of address for 7-day forecast
        response = weather_handler('a7' + address)
        response = response.split('/')
        self.assertEqual(7, len(response))

        #test good input of coordinates for 7-day forecast
        response = weather_handler('c7' + coordinates)
        response = response.split('/')
        self.assertEqual(7, len(response))


    def test_sports(self):
        '''
        Test sports API
        '''
        self.app.name = 'sports'
        league = 'b'
        date = '20180423'
        scoreboard = ('HOU;MIN;8:00PM/OKL;UTA;10:30PM')
        self.assertEqual(scoreboard, sports_handler(league + date))

        #test a day where there are no games for the given league
        league_short = 'f'
        league_long = 'nfl'
        date = '20180408'
        no_games = 'No ' + league_long + ' games found on ' + date[4:6] + '/' + date[6:8] + '/' + date[0:4]
        self.assertEqual(no_games, sports_handler(league_short + date))
