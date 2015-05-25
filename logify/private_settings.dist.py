import os

# Used to build paths inside the project
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'TODO: place your secret key here'

# SECURITY WARNING: don't run with debug turned on in production
DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

}

# Static files (CSS, JavaScript, Images)                   
# https://docs.djangoproject.com/en/1.7/howto/static-files/

_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR + '/static/',
)

TEMPLATE_DIRS = (
    BASE_DIR +  '/templates/',
)
