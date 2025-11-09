"""
WSGI config for survey_project project on PythonAnywhere.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

# Add your project directory to the sys.path
# Replace 'opros123' with your actual PythonAnywhere username
path = '/home/opros123/Anonymous_survey'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable to tell Django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'survey_project.settings'

# Set default environment variables
os.environ.setdefault('SECRET_KEY', 'django-insecure-pythonanywhere-key-change-in-production')
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('ALLOWED_HOSTS', 'opros123.pythonanywhere.com,localhost,127.0.0.1')

# Activate your virtual env
# Replace 'opros123' with your actual PythonAnywhere username
activate_this = '/home/opros123/.virtualenvs/survey_env/bin/activate_this.py'
try:
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))
except FileNotFoundError:
    pass  # Virtual env might not exist yet

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
