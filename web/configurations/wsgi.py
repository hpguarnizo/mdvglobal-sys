"""
WSGI config for landing project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "landing.settings")


from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
import django.core.handlers.wsgi



# This application object is used by the development server
# as well as any WSGI server configured to use this file.
application = get_wsgi_application()
application = django.core.handlers.wsgi.WSGIHandler()
application = DjangoWhiteNoise(application)