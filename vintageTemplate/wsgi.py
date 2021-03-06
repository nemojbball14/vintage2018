"""
WSGI config for vintage2018 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys
sys.path.append('/usr/local/django')
os.environ['DJANGO_SETTINGS_MODULE'] = "vintage2018.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
