from setuptools import setup, find_packages

setup(name='django_project',
      version='0.1',
      description='Base Django template for starting projects.',
      url='http://github.com/dwdresser/django_project',
      author='Doug Dresser',
      author_email='dwdresser@wisc.edu',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'django',
        'django-debug-toolbar',
        'django-allauth',
        'twilio',
        'django-twilio',
        'wikipedia',
      ],
     )
