"""
Django settings for DailyFresh project.

Generated by 'django-admin startproject' using Django 1.11.6.

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
SECRET_KEY = 'fhixpf)g$0c@b8qic4%ll%(g!36@$_f#-!*&)23wf8@m_x1dsj'

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
    'apps',  # 配置apps总应用
    'tinymce',  # 富文本编辑器,安装: pip install django-tinymce
    'user',  # 用户模块
    'goods',  # 商品模块
    'order',  # 订单模块
    'cart',  # 购物车模块
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

ROOT_URLCONF = 'DailyFresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 配置模版路径
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

WSGI_APPLICATION = 'DailyFresh.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# 配置数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dailyfresh',  # 数据库名称
        'USER': 'root',  # mysql数据库用户名
        'PASSWORD': 'root',  # mysql数据库登陆密码
        'HOST': 'localhost',  # IP地址
        'PORT': '3306',  # 端口号
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

STATIC_URL = '/static/'

# 配置静态文件路径
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# 富文本编辑器配置: 安装: pip install django-tinymce
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',  # 主题模式:高级
    'width': 600,  # 富文本宽度
    'height': 400,  # 富文本高度
}

import sys

# 把apps应用目录添加进系统环境中
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# django认证系统指定使用的模型类
AUTH_USER_MODEL = 'user.User'
# settings配置默认检查用户是否活跃状态is_axtive,不活跃返回None
# AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
# settings配置设置不检查用户的活跃状态is_active
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']

# 发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'  # smpt服务地址
EMAIL_PORT = 25  # 端口号
EMAIL_HOST_USER = 'configureadmin@163.com'  # 发送邮件的邮箱
EMAIL_HOST_PASSWORD = 'asdfghjkl123456'  # 在邮箱中设置的客户端授权密码
EMAIL_FROM = '天天生鲜<configureadmin@163.com>'  # 收件人看到的发件人

'''
默认情况下session是存储在数据库中的，但是当用session保存用户的状态时，用户频繁的访问服务器，
会增大数据库的压力，也会降低用户访问的速度。为了解决这个问题将session存储到redis中。
'''
# Django框架项目中session存储到redis中的配置(两种方式):
# 1.第一种配置:直接将session存储的地方配置到redis中
# ①.)安装: pip install django-redis-sessions==0.5.6
# ②.)在django项目的settings文件中配置redis作为存储session的位置
# SESSION_ENGINE = 'redis_sessions.session'
# SESSION_REDIS_HOST = 'localhost'
# SESSION_REDIS_PORT = 6379
# SESSION_REDIS_DB = 2
# SESSION_REDIS_PASSWORD = ''
# SESSION_REDIS_PREFIX = 'session'

# 2.第二种配置:将django项目的缓存设置为redis,然后将session的存储地方设置到django项目的缓存中
# ①.)安装: pip install django-redis
# ②.)配置redis作为django项目的缓存设置:
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # 设置redis服务的IP地址与端口号以及哪个数据库
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "password",
        }
    }
}
# ③.)配置session的存储位置到redis缓存的设置:
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
