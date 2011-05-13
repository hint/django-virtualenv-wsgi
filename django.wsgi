#!./_env/bin/python
# -*- coding: utf-8 -*-

# Name of a directory (Python package) containing your Django project.
# This directory should be in the same location as this WSGI handler.
PROJECT_NAME = 'django_project'

# A relative path to file which, if exists, forces the handler to respond with server
# maintenance message. 
MAINTENANCE_LOCK_FILE = 'maintenance.lock'

# Relative path to HTML file sent as a maintenance message.
# This file should be encoded in UTF-8.
MAINTENANCE_MESSAGE_FILE = 'maintenance.html'

# The message sent in case MAINTENANCE_MESSAGE_FILE doesn't exist or is not readable.
# This should be an unicode plain text string.
MAINTENANCE_MESSAGE_FALLBACK = u"Server is down for maintenance. Please try again later."

################################################################################

import os
import sys
import site

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

def get_django_wsgi_application():
    """
    Sets up an environment for a Django application and returns Django built-in WSGI handler.
    """
    PROJECT_PATH = os.path.join(BASE_PATH, PROJECT_NAME)

    PYTHON_ENV_PATH = os.path.join(BASE_PATH, '_env')

    PYTHON_ENV_ACTIVATOR = os.path.join(PYTHON_ENV_PATH, 'bin', 'activate_this.py')

    # Activate virtualenv
    execfile(PYTHON_ENV_ACTIVATOR, dict(__file__=PYTHON_ENV_ACTIVATOR))

    # Insert important import paths at the beginning of PATH
    sys.path.insert(0, PROJECT_PATH)
    sys.path.insert(1, BASE_PATH)

    # Import project settings
    import settings as project_settings

    # Setup project environment
    import django.core.management
    django.core.management.setup_environ(project_settings)

    # Validate models
    django.core.management.ManagementUtility().fetch_command('runserver').validate()

    # Activate default language
    import django.conf
    import django.utils
    django.utils.translation.activate(django.conf.settings.LANGUAGE_CODE)

    # Return Django's WSGI handler
    import django.core.handlers.wsgi
    return django.core.handlers.wsgi.WSGIHandler()

def maintenance_wsgi_application(environ, start_response):
    """
    WSGI handler (see PEP333) responding with server maintenance message from a HTML file.
    If a message file doesn't exist, responds with default, plain text message.
    Uses UTF-8 encoding for all its input and output.
    """
    status = '503 Service Unavailable'
    headers = []
    body = []
    try:
        # Try to open a HTML file with maintenance message
        file = open(os.path.join(BASE_PATH, MAINTENANCE_MESSAGE_FILE), 'r')
        body.append(file.read())
        file.close()
        headers.append(('Content-Type', 'text/html; charset=UTF-8'))
    except IOError:
        # Apparently message HTML file doesn't exist. Fallback to plain text message.
        body.append(MAINTENANCE_MESSAGE_FALLBACK.encode('utf-8') + "\r\n")
        headers.append(('Content-Type', 'text/plain; charset=UTF-8'))
    start_response(status, headers)
    return body

if not os.path.exists(os.path.join(BASE_PATH, MAINTENANCE_LOCK_FILE)):
    # Maintenance lock file doesn't exist - running Django app
    application = get_django_wsgi_application()
else:
    # Maintenance lock file exists - respond with maintenance message
    application = maintenance_wsgi_application
    
