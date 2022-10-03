"""
Django settings for learning_site project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from learning_site import secret

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'web.apps.WebConfig',
    # 'learn_test.apps.LearnTestConfig',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 添加自己的中间件
    'web.middlewares.AuthMiddleware',
]

ROOT_URLCONF = 'learning_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', ]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'web_tag': 'web.templatetags.project'
            }
        },
    },
]
WSGI_APPLICATION = 'learning_site.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secret.NAME,
        'USER': secret.USER,
        'PORT': secret.PORT,
        'PASSWORD': secret.PASSWORD,
        'HOST': secret.HOST
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
# 静态文件相关


STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static') # 和app有关
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]  # 和app无关
# 使用Django内建用户系统
AUTH_USER_MODEL = 'web.User'

# 中间资源相关
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 缓冲相关
CACHES = {
    'default': {  # locmem.LocMemCache
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table1',  # 缓存表
        'TIMEOUT': 300,  # 默认缓存保存时间
        'OPTIONS': {
            'MAX_ENTRIES': 300,  # 最大缓存数据量
            'CULL_FREQUENCY': 2,  # 缓存条目到达最大值时,删除缓存的 1/x 的数据
        }
    },
    "REDIS": {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{secret.REDIS_HOST}:{secret.REDIS_PORT}',  #
        'OPTIONS': {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'max_connections': 1000,
            'encoding': 'utf-8',
            'PASSWORD': secret.REDIS_PASSWORD,
        },
    }

}
# SESSION相关
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
# session存储时间
SESSION_COOKIE_AGE = 60 * 10  # 存储时间

# 样式相关
BOOTSTRAP3 = {
    'include_jquery': True,
}
# 邮件配置
# 配置邮件
EMAIL_BACKEND = secret.EMAIL_BACKEND
EMAIL_HOST = secret.EMAIL_HOST
EMAIL_PORT = secret.EMAIL_PORT
EMAIL_HOST_USER = secret.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secret.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = secret.EMAIL_USE_TLS
# 配置登录状态
USER_STATE = {'register', 'logging'}

# MINIO相关
MINIO_HOST = secret.MINIO_HOST
MINIO_PORT = secret.MINIO_PORT
MINIO_ACCESS_KEY = secret.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = secret.MINIO_SECRET_KEY
MINIO_DEFAULT_REGION = secret.MINIO_DEFAULT_REGION

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
