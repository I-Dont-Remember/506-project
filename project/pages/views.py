from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from allauth.account.views import SignupView
from allauth.account.forms import LoginForm

#from classes.Tags import Tags

from users.models import CustomUser
from users.forms import CustomLoginForm


def home(request):
    context = {'login_form' : LoginForm()}
    return render(request, 'home.html', context=context)

@login_required
def profile(request):
    context = {}
    return render(request, 'profile.html', context=context)

def about_us(request):
    context = {}
    return render(request, 'about_us.html', context=context)

def clients(request):
    context = {}
    return render(request, 'clients.html', context=context)

class CustomSignupView(SignupView):
    def __init__(self, *args, **kwargs):
        super(CustomSignupView, self).__init__(*args, **kwargs)
