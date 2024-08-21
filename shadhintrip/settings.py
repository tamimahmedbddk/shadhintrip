from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# For local development, set ENVIRONMENT=development.
# For production, set ENVIRONMENT=production.

ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
if ENVIRONMENT == 'production':
    from .settings_prod import *
else:
    from .settings_dev import *


# settings.py
AUTH_USER_MODEL = 'users.CustomUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'maintenance_mode',
    'django.contrib.humanize',
    'home',
    'SiteSetting',
    'tours',
    'blog',
    'users',
    'visa',
    'bookings',
    'newsletter',
    'contact',

    # tootls
    'dbbackup',
    'ckeditor',
    'widget_tweaks',
    'django_social_share'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]

ROOT_URLCONF = 'shadhintrip.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'SiteSetting.context_processors.common_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'shadhintrip.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config('SQL_ENGINE'),
        "NAME": config('SQL_DATABASE'),
        "USER": config('SQL_USER'),
        "PASSWORD": config('SQL_PASSWORD'),
        "HOST": config('SQL_HOST'),
        "PORT": config('SQL_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
   os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'shadhintripbd@gmail.com'  # Gmail email address
EMAIL_HOST_PASSWORD = 'vydw rfew jfsw gtuv'     # Gmail password or app-specific password
DEFAULT_FROM_EMAIL = 'ShadhinTrip <info@shadhintrip.com>'

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}


# ====maintenance_mode====
MAINTENANCE_MODE = True
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True
MAINTENANCE_MODE_IGNORE_STAFF = True
# ====maintenance_mode====

