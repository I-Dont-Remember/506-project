from django.urls import path

from .sms import receive

urlpatterns = [
    path(r'receive', receive , name='receive')
]
