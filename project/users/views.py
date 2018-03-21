from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm

class SignUp(generic.CreateView):

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def signup(request):

    context = {
        'form': CustomUserCreationForm,
        'success_url': reverse_lazy('login')
    }
    return render(request, 'registration/signup.html', context)
