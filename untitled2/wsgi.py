import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled2.setting.prod")
application = get_wsgi_application()
