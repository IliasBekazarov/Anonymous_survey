"""
WSGI config for survey_project project on PythonAnywhere.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

# ============ МААНИЛҮҮ: opros123 дегенди өзүңүздүн username менен алмаштырыңыз! ============

# Add your project directory to the sys.path
# Replace 'opros123' with your actual PythonAnywhere username
path = '/home/opros123/Anonymous_survey'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable to tell Django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'survey_project.settings'

# Set environment variables for PRODUCTION
os.environ['SECRET_KEY'] = 'django-insecure-pythonanywhere-production-key-CHANGE-ME-12345'
os.environ['DEBUG'] = 'False'
os.environ['ALLOWED_HOSTS'] = 'opros123.pythonanywhere.com,localhost,127.0.0.1'

# Activate your virtual env
activate_this = '/home/opros123/.virtualenvs/survey_env/bin/activate_this.py'
try:
    with open(activate_this) as f:
        code = compile(f.read(), activate_this, 'exec')
        exec(code, dict(__file__=activate_this))
except FileNotFoundError:
    # If activate_this.py is not found, add site-packages to path
    site_packages = '/home/opros123/.virtualenvs/survey_env/lib/python3.10/site-packages'
    if site_packages not in sys.path:
        sys.path.insert(0, site_packages)

# Get the Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
