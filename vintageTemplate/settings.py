"""
Django settings for vintage20xx project.

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

STATIC_URL = '/static/20xx/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'vintage20xx', 'webContent', 'static', '20xx')

MEDIA_URL = '/uploads/20xx/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'vintage20xx', 'webContent', 'uploads', '20xx')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'replace this'

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
    'timeline',
    'people',
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

ROOT_URLCONF = 'vintage20xx.urls'

WSGI_APPLICATION = 'vintage20xx.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': 'bjuvinta_db_20xx',
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
LOGIN_URL = '/20xx/login/'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Mapping of society mascots to their Greek
ALIASES = {
    "eagles" : "Alpha Gamma Tau", #"Basilean"
    "ambassadors" : "Alpha Sigma Omicron",
    "bear cubs" : "Beta Chi Omega",
    "cardinals" : "Beta Epsilon Chi",
    "bobcats" : "Chi Epsilon Sigma",
    "dragons" : "Chi Kappa Delta",
    "sailors" : "Chi Sigma Phi",
    "gators" : "Chi Theta Upsilon",
    "flames" : "Nu Alpha Phi",
    "classics" : "Pi Delta Chi",
    "firebirds" : "Sigma Kappa Rho",
    "duskie birds" : "Sigma Lambda Delta",
    "kangaroos" : "Tau Delta Chi",
    "owls" : "Theta Alpha Chi",
    "tigers" : "Theta Delta Omicron",
    "bandits" : "Theta Mu Theta",
    "mustangs" : "Theta Pi Delta",
    "colts" : "Theta Sigma Chi",
    "pirtates" : "Tri Epsilon",
    "seagulls" : "Zeta Tau Omega",
    "wildcats" : "Zoe Aletheia",
    "lions" : "Alpha Omega Delta",
    "farley barnhardt" : "Alpha Omega Delta",
    "razorbacks" : "Alpha Theta Pi",
    "patriots" : "Beta Gamma Delta",
    "bears" : "Bryan",
    "cavaliers" : "Chi Alpha Pi",
    "wolves" : "Chi Epsilon Delta",
    "tornadoes" : "Epsilon Zeta Chi",
    "knights" : "Kappa Sigma Chi",
    "stallions" : "Kappa Theta Chi",
    "falcons" : "Lanier",
    "vikings" : "Nu Delta Chi",
    "bulldogs" : "Phi Beta Chi",
    "rams" : "Phi Kappa Pi",
    "royals" : "Pi Gamma Delta",
    "cobras" : "Pi Kappa Sigma",
    "spartans" : "Sigma Alpha Chi",
    "panthers" : "Theta Kappa Nu",
    "hawks" : "Zeta Alpha Pi",
}
