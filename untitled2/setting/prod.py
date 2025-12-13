from untitled2.settings import *
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^#(*+$_7#)^ww-orc58au3z9v&9r4bzn*8cq=d7jklc=_4kyj!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_DIRS = [BASE_DIR / 'statics']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True