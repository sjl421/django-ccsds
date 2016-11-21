# coding:utf-8
"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.8.16.

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
SECRET_KEY = '_(s0l@@d4yanq8$uxu)f+*tws9vv-$2r(ih^it0bp!to8r673e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
   
    'django.contrib.admin', 
     # 身份验证系统
    'django.contrib.auth', 
    # 内容类型框架
    'django.contrib.contenttypes',
    # Session框架
    'django.contrib.sessions',
    # 消息框架
    'django.contrib.messages',
    # 静态文件管理框架
    'django.contrib.staticfiles',
    # 手动新增投票系统
    'polls',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR+'/db', 'db.sqlite3'), # 数据库sqlite３文件的绝对地址
    }
}

"""
    如果是其他数据库，比如mysql,Oracle,则需要用以下格式。
    'default':{
        'ENGINE': 'django.db.backends.mysql' 或者　'django.db.backends.oracle'　或者　 'django.db.backends.postgresql_psycopg2'　等
        'NAME':  '数据库名'
        'USER':  '数据库用户名'
        'PASSWORD': '数据库密码'
        'HOST': '主机地址'　（如果和你的数据库服务器是同一台物理机器，则此处留空）
    }
"""
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
# 默认时区为芝加哥时间
TIME_ZONE = 'UTC' 

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
