import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.project.settings')

def pytest_configure():
    settings.DEBUG = False
    settings.configure()
