"""
Django settings for choose project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-c*o6p89wd33%(f)wda#zxy6!d@_nsmzd@xoy)p%u@avly$9=_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



# Application definition

INSTALLED_APPS = (
	'bootstrap_admin',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'mptt',
	'tasks',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	# 'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'chosen.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
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

WSGI_APPLICATION = 'chosen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'



#### TANGFENG ####
# LOGGING = {
# 	'version': 1,
# 	'disable_existing_loggers': False,
# 	'handlers': {
# 		'file': {
# 			'level': 'DEBUG',
# 			'class': 'logging.FileHandler',
# 			'filename': 'debug.log',
# 		},
# 	},
# 	'loggers': {
# 		'default': {
# 			'handlers': ['file'],
# 			'level': 'DEBUG',
# 			'propagate': True,
# 		},
# 	},
# }

LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'formatters': {
		'standard': {
			'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
		},
	},
	'filters': {
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'class': 'django.utils.log.AdminEmailHandler',
			'include_html': True,
		},
		'default': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': 'all.log',
			'maxBytes': 1024 * 1024 * 5,  # 5 MB
			'backupCount': 5,
			'formatter': 'standard',
		},
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'standard'
		},
		'request_handler': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': 'script.log',
			'maxBytes': 1024 * 1024 * 5,  # 5 MB
			'backupCount': 5,
			'formatter': 'standard',
		},
		'scprits_handler': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': 'script.log',
			'maxBytes': 1024 * 1024 * 5,  # 5 MB
			'backupCount': 5,
			'formatter': 'standard',
		},
	},
	'loggers': {
		'django': {
			'handlers': ['default', 'console'],
			'level': 'DEBUG',
			'propagate': False
		},
		'XieYin.app': {
			'handlers': ['default', 'console'],
			'level': 'DEBUG',
			'propagate': True
		},
		'django.request': {
			'handlers': ['request_handler'],
			'level': 'DEBUG',
			'propagate': False
		},
		'scripts': {
			'handlers': ['scprits_handler'],
			'level': 'INFO',
			'propagate': False
		},
	}
}

# END
