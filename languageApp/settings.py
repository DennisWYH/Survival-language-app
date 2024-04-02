from pathlib import Path
import os
from django.core.management.utils import get_random_secret_key
import sys
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Deployment settings following instruction from Digital Occean:
# see https://docs.digitalocean.com/developer-center/deploy-a-django-app-on-app-platform/
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())
DEBUG = os.getenv("DEBUG", "FALSE") == "TRUE"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1, localhost").split(",")
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

INSTALLED_APPS = [
    'user.apps.UserConfig',
    'card.apps.CardConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
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

ROOT_URLCONF = 'languageApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'languageApp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# We can flip this to use sqlite for development :)
# DEVELOPMENT_MODE = True
# DEBUG = True

if DEVELOPMENT_MODE is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

if DEVELOPMENT_MODE is False:
    if len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
        if os.getenv("DATABASE_URL", None) is None:
            raise Exception("DATABASE_URL environment variable not defined")
        DATABASES = {
            "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
        }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# for files that doesn't belong to specific app
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "languageApp", "static"),
]

# Setting up Digital ocean object storage space for the media files
# It uses S3 protocol
AWS_ACCESS_KEY_ID = 'DO00HU78UG6GDDQEBGF7'
AWS_SECRET_ACCESS_KEY = 'fvpa1h23MGS5gP3c2XWEvtFb5miIC0v80NqfRuQCJoo'
AWS_STORAGE_BUCKET_NAME = 'languageappmediakey'
AWS_S3_ENDPOINT_URL = 'https://languagereference.ams3.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'media'

if DEVELOPMENT_MODE is True:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
    DEFAULT_FILE_STORAGE = 'django_project.storage_backends.MediaStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Set the age of session cookies in seconds
SESSION_COOKIE_AGE = 1209600  # 2 weeks, in seconds

# Save the session data on every request
SESSION_SAVE_EVERY_REQUEST = True