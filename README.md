# Lucidata - Backend Server and Website

## Summary
This repo will contain all of the server side code written in python and Django for Lucidata, including the website, backend, and sms handler for the mobile client.

## Current Features
- SMS Send and Receive API
- External API Handler
  - Wikipedia
- Basic User Authentication
  - Sign up, Sign in, Sign out
  - Login via Facebook
  
## Development Setup
This will give a (hopefully) complete guide on how to clone the repo and begin development in the proper environment.
1. Download python 3+ and pip from the internet. I believe pip comes with the python distribution.
   - Verify that typing 'python' in your command line will bring up python 3+, not python 2+, otherwise you have to change your environment variable to point to python 3+. Google it for help.
   - Verify that pip is installed by typing 'pip' in the command line, which should bring up some sort of usage for that program.
2. Clone this repo somewhere with 'git clone https://github.com/I-Dont-Remember/506-project.git
3. Go into the root directory of the project (where the README.md lives)
4. Install virtualenv with 'pip install virtualenv'
5. Create a virtual environment with 'virtualenv venv'. This basically creates a fancy container for doing development that makes sure you can control all of the project dependencies.
6. Activate the virtual environment, which should bring up a '( venv )' in front of your command line thing 
   - Windows peeps use 'venv\Scripts\activate.bat'
   - Mac/Linux peeps use 'source venv/bin/activate'
7. Install the project directory using 'pip install -e .'
8. You can optionally run tests with 'tox'

## Running the Server
1. First go through the Development Setup section.
2. Navigate one layer down into the 'project' directory that contains 'manage.py'.
3. Run the command 'python manage.py runserver'. This will start it up from the localhost (127.0.0.1:8000).
   - You can optionally run it not locally using 'python manage.py runserver 0.0.0.0:8000' or some other port, but make sure those zeroes are there. This lets everyone else access the server via your IP address.
