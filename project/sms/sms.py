# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django_twilio.decorators import twilio_view
from twilio.rest import Client

from django.conf import settings

from .models import App, MessageReceived, MessageSent
from .api_handler import api_handler
from users.models import CustomUser


@twilio_view
def receive(request):
    '''
    This is the webhook given to the sms provider, and expects a POST
    request to be sent with the sms data.

    param request: the http request data

    Return the http response
    '''
    # EXAMPLE USING TWILIO

    # parse the http request to get message content
    phone = request.POST.get('From', '')
    body = request.POST.get('Body', '').split(',')
    app = body[0]
    data = body[1]

    # try matching a user to the phone number
    try:
        user = CustomUser.objects.get(phone=phone[2:])
    except ObjectDoesNotExist:
        user = None

    # try matching an app, this should work unless we did something bad
    try:
        app = App.objects.get(name=app)
    except:
        app = None

    # create and save a db instance of the message
    new_message = MessageReceived(
                    user=user,
                    date=datetime.now(),
                    app=app,
                    data=data,
                    )
    new_message.save()

    # only proceed if the number is linked to a user
    if new_message.user:
        response = api_handler(app, data)
        if response is None:
            return HttpResponse(400)
        send(user, app, response)
        HttpResponse(200)
    return HttpResponse(400)

def send(user, app, data):
    '''
    This method sends a message to a user given data from an app.

    param user: User object of the user to send the message
    param app: App object of the applction the message pertains to
    param data: string of data that is the body of the sms
    '''
    # EXAMPLE USING TWILIO

    # instantiate twilio client from api keys in the settings file
    client = Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN
    )

    # send the text
    message = client.messages.create(
        to=user.phone,
        from_=user.twilio_phone,
        body="{},{}".format(app.name,data),
    )

    # create and save a db instance for our records
    new_message = MessageSent(
                    user=user,
                    date=datetime.now(),
                    app=app,
                    data=data,
                    )
    new_message.save()
    print('sent')

    return message
