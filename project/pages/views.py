from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import CustomUser

def home(request):
    context = {}
    return render(request, 'home.html', context=context)

@login_required
def profile(request):
    context = {}
    return render(request, 'profile.html', context=context)
