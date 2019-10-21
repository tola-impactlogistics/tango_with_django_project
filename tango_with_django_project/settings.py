"""
Django settings for tango_with_django_project project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'p_+1gtjxjkt#rhq5k2ai7o79qlolim+0zr#^m-dc0fcqit=2uj'
SECRET_KEY = 'yu9876+=9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'djng',
    'registration',
    'rango.apps.RangoConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'tango_with_django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                    os.path.join(BASE_DIR, 'rango', 'templates', 'rango'),        
                    #os.path.join(os.path.join(BASE_DIR), 'rango', 'templates', 'rango'),
                    #'/users/user/code/tango_with_django_project/rango/Templates/rango',
                    '/users/user/code/default',
                ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tango_with_django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

RANGO_PATH = os.path.join(BASE_DIR, 'rango')

STATIC_PATH = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = [STATIC_PATH,]

# Media files 

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(RANGO_PATH, 'media') # Absolute path to the media directory

LOGIN_URL = '/rango/login/'


# Dis-enabling browser-lenght sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = False # To enables persistent sessions
SESSION_COOKIE_AGE = 1209600  # a Two Weeks Period

# python manage.py clearsessions      Sessions cookies accumulate. So if you're using the db backend you will have to periodically clear the db that stores the cookies.

    #The per-site cache
 #   'django.middleware.cache.UpdateCacheMiddleware',
 #   'django.middleware.cache.CommonMiddleware',
 #   'django.middleware.cache.FetchFromCacheMiddleware',

#CACHE_MIDDLEWARE_ALIAS = '' # - The cache alias to use for storage
#CACHE_MIDDLEWARE_SECONDS = '' # - The cache alias to use for storage
#CACHE_MIDDLEWARE_KEY_PREFIX = '' # - The cache alias to use for storage

#Email StathandleConfig
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'                 #Now Working
#EMAIL_FILE_PATH = '/rango/rango-messages/email/'

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_PORT = 25
EMAIL_USE_TLS = False

ADMINS = (('admin', 'admin@rango.com'),)
MANAGERS = (('popoli', 'popoli@polo.com'),)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#        'LOCATION': 'c:/users/user/code/tango_with_django_project/rango-messages/cache/',
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }

}

#Django-Registration-Redux Connection
REGISTRATION_OPEN = True                # If True, users can register
ACCOUNT_ACTIVATION_DAYS = 7     # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True  # If True, the user will be automatically logged in.
LOGIN_REDIRECT_URL = '/rango/'  # The page you want users to arrive at after they successful log in
LOGIN_URL = '/accounts/login/'  # The page users are directed to if they are not logged in,
                                                                # and are trying to access pages requiring authentication