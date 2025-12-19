from untitled2.settings import *

SECRET_KEY = 'django-insecure-^#(*+$_7#)^ww-orc58au3z9v&9r4bzn*8cq=d7jklc=_4kyj!'
DEBUG = False
ALLOWED_HOSTS = ["95.134.130.121", 'weplay.beauty']


INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'debug_toolbar']
MIDDLEWARE = [m for m in MIDDLEWARE if 'debug_toolbar' not in m]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_DIRS = [BASE_DIR / 'statics']


CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False