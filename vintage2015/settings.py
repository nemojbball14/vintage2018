"""
Django settings for vintage2015 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,'templates'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/2015/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'webContent', 'static', '2015')

MEDIA_URL = '/uploads/2015/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'webContent', 'uploads', '2015')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l@ulbf7#6+9%ve&*n*^x)-ujlc30s1fo0l%&4ibh$3shp=06h^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    'bjuvintage.com',
    'www.bjuvintage.com',
]
# ALLOWED_HOSTS = ['localhost',]



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'picsearch',
    'organizations',
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'vintage2015.urls'

WSGI_APPLICATION = 'vintage2015.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': 'bjuvinta_db',
        'ENGINE': 'mysql.connector.django',
        'USER': 'bjuvinta_django',
        'PASSWORD': 'M~au4G5z.^%]',
        'OPTIONS': {
         'autocommit': True,
        },
    }
}

SOUTH_DATABASE_ADAPTERS = { 'default' : 'south.db.mysql' }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# uncomment to allow login stuff
LOGIN_URL = '/2015/login/'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

