# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.utils.timezone import now

from users.models import CustomUser

class MessageReceived(models.Model):
    '''
    Stores a message sent to the server
    '''
    user = models.ForeignKey(CustomUser, models.SET_NULL, null=True, related_name='received_user')
    date = models.DateTimeField(default=now)
    app = models.ForeignKey('App', models.SET_NULL, null=True)
    data = models.CharField(max_length=1600)


class MessageSent(models.Model):
    '''
    Stores a message sent to the client
    '''
    user = models.ForeignKey(CustomUser, models.SET_NULL, null=True, related_name ='sent_user')
    date = models.DateTimeField(default=now)
    app = models.ForeignKey('App', models.SET_NULL, null=True)
    data = models.CharField(max_length=1600)


class App(models.Model):
    '''
    References an application supported (google maps, wiki, etc.)
    '''
    name = models.CharField(max_length=1600)
    # add more things here like api links, or function names, etc
