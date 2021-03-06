[![Build Status](https://travis-ci.org/I-Dont-Remember/506-project.svg?branch=master)](https://travis-ci.org/I-Dont-Remember/506-project) [![Coverage Status](https://coveralls.io/repos/github/I-Dont-Remember/506-project/badge.svg?branch=master)](https://coveralls.io/github/I-Dont-Remember/506-project?branch=master)
# Lucidata - Backend Server and Website

## Summary
   This repo will contain all of the server side code written in python and Django for Lucidata, including the website, backend, and sms handler for the mobile client.

## Current Features
This repo is currently in the Iteration 2 phase, which has the following features implemented.
- Development Environment
  - Travis CI builds
  - Unit Testing via tox and Django's testing framework
  - Code coverage via Coverage and Coveralls
- SMS Send and Receive API
- External API Handler
  - Wikipedia
  - Sports
  - Weather
  - Directions
- Basic User Authentication
  - Sign up, Sign in, Sign out
  - Login via Facebook
- Better templates
   - CSS and other static files incorporated
   - Website looks pretty
- New Views
   - User profile page
   - Home page for logging in
   - Built in authentication extends the base template
   - Menu navigation
   - Clients/About-us pages

## Development Environment Setup
This will give a (hopefully) complete guide on how to clone the repo and begin development in the proper environment.
1. Download python 3+ and pip from the internet. Pip should come with the python distribution.
   - Verify that typing `python` in your command line will bring up python 3+, not python 2+, otherwise you have to change your environment variable to point to python 3+. Google it for help.
   - Verify that pip is installed by typing `pip` in the command line, which should bring up some sort of usage for that program.
2. Clone this repo somewhere with `git clone https://github.com/I-Dont-Remember/506-project.git`
3. Navigate into the root directory of the project (where the README.md lives).
4. Scripts have been made to complete the rest of the steps automatically. This will create the virtual environment, activate it, and install all dependencies.
   - Mac/Linux users can run `source develop.sh`
   - Windows users can run `develop.bat`

**There is no need to complete the rest of the steps if the scripts in step 4 ran successfully**

5. Install virtualenv with `pip install virtualenv`.
6. Create a virtual environment with `virtualenv venv --python=python3`. This creates a virtual environemnt named 'venv', allowing development in an isolated environment, where package dependencies can be managed easily.
7. Activate the virtual environment, which should bring up a `(venv)` string in front of your command line tag. This can be deactivated at any time by typing `deactivate`.
   - Windows user can use `venv\Scripts\activate.bat` to activate the virtual environment.
   - Mac/Linux users can use `source venv/bin/activate` to activate the virtual environment.
8. Install the project dependencies at the root directory using `pip install -e .`. This will find the 'setup.py' file and install any packages specified in there.

## Running the Server
1. First go through the [Development Environment Setup](##Development-Environment-Setup) section.
2. Navigate one layer down into the 'project' directory that contains 'manage.py'.
3. Run the command `python project/manage.py runserver`. This will start a server at the localhost (127.0.0.1:8000).
   - You can optionally broadcast the server to anyone on the network with `python manage.py runserver 0.0.0.0:8000` or any other port, as long as the '0.0.0.0' is specified.

*Please note that the static files (i.e. css and fonts) may not load correctly or the same on every machine. This has been noted on Windows specifically. We have yet to find a solution to this so that every different environment will produce the same results.*

## Testing
Testing is run via Django's testing framework, which is built on top of Unittest. These tests can be found in the various app directories under the 'tests.py' files. Testing is automatically run by Travis daily and new commits, but can be run locally using the following steps.
1. First go through the [Development Environment Setup](##Development-Environment-Setup) section.
2. Testing is done using tox, and must be installed using `pip install tox`.
3. Run the tests with `tox`. Or run `python project/manage.py test <app>` to run the tests in a certain app's directory such as `sms`


## Setting up with Mobile Client
1. Run server on localhost:8000
2. Run ./ngrok 8000
3. Change twilio api handler to <ngrok_website>/sms/receive
4. Create a valid user with the phone number of the mobile client (no duplicate users for now)
