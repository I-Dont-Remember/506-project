#from project.sms.sms import send, receive
#from project.users.models import CustomUser

from django.conf import settings

# Test that testing itself works
class TestClass:
    def test_simple(self):
        assert True

#def test_sms():
#    user = CustomUser.objects.get(username='dummy')
#    app = App('test')
#    send(user, app, 'Test Message')
