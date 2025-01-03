"""
Django settings for duty project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o*hp$9%_88)2e_8ww)tysi1=$oc=xdve46ini%v&6t0f^kkuoq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'settings.suitv2.SuitConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'corsheaders',  # CORS
    'rest_framework',
    'drf_yasg',  # *** swagger ***
    'django_filters',
    # 'rest_framework_simplejwt',
    # 'test111',
    # 'django_crontab',  # 定时任务，仅限Linux上使用
    'personnel'  # 人员管理
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',  # CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'duty.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],   # 自定义模板文件起始根目录
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

WSGI_APPLICATION = 'duty.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sxc_dm',
        'USER': 'sxc_dm_user',
        'PASSWORD': 'SiDt2B&UVl',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 项目上线后，客户端或管理后台动态上传的静态文件根目录，包括ImageField等Django自带字段的upload_to，默认保存根目录也是这个
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 文件上传后的默认权限
FILE_UPLOAD_PERMISSIONS = 0o660

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# *** CORS ***
# CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     'https://*',
# )
#
# CORS_ALLOW_HEADERS = (
#     'XMLHttpRequest',
#     'X_FILENAME',
#     'accept-encoding',
#     'authorization',
#     'content-type',
#     'code-hash',
#     'dnt',
#     'origin',
#     'unit',
#     'user-agent',
#     'x-csrftoken',
#     'x-requested-with'
# )

# *** REST API ***
from settings.rest import *

# *** JWT ***
from settings.jwt import *

# *** swagger ***
from settings.swagger import *

# *** 低版本 suit，不兼容高版本Django，已改用suit-v2 ***
# from settings.suit import *

# 自定义验证
AUTHENTICATION_BACKENDS = ('utils.Auth.CustomAuthBackend',)

# 前后端RSA（PKCS#8，1024 bit）加密的密钥对【注意，jsencrypt中PUBLIC_KEY每一行都要去掉末尾的\n】
PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" \
             "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyGQoOvCFa8R3Zz6eOl2pEL7vJ\n" \
             "v2j8ZfQJKWCav5YWOHJHjCx1AgU0WTsPMJasgTHTNavn3QHlf1+FYevs7pl2ZA0C\n" \
             "wc+1MQ/6LnAwi3uzXTm0ZeClhVsxQ3h0ztlRIENF4/Za0nXh+rrxJ72UnX+7/8Ot\n" \
             "+J/EKMy8XR7LZr2DIwIDAQAB\n" \
             "-----END PUBLIC KEY-----"

PRIVATE_KEY = "-----BEGIN RSA PRIVATE KEY-----\n" \
              "MIICXQIBAAKBgQC1TypY3Oc0QjcZlnT472Oe9/evPXGG1tzurrhXyhkUYF+XnCh3\n" \
              "rVY9QazYLbvDVAHcLki386EnIS6ObPMCIFIJ8TiNVVMnCwW+B2+BPkLrVmjU1EWk\n" \
              "Hzkd4MTHJSEYtXvv7NEBLK1LYFbksKverAHFJa75yMywK/DzOmzx18NpewIDAQAB\n" \
              "AoGABxi5Um9vDfDA4bEDFL1LURe+lkQu6Iq0whOM++6uoEliDyKZw47BeeCosxtz\n" \
              "Jng9dxCetbMvrcLoOhiR7cA1xcRuMVVFgmM26RvQpOGRF2AuoZpwGk+t+meh/tup\n" \
              "MsQKnZ6hV81O8W0FUDq/uzyS20CGiS9UemJUNNxZ4VZsuJ0CQQC3Oj5ysgxEIIHM\n" \
              "NNiHuQAqV8FkMTzFrAbEIJZ6WnyGdhByG2C+B/ONkqBOyfFf1NYpIooQny5DT5nO\n" \
              "JggL8TpvAkEA/VHhOhGPzTx1024V6+rHZns/8OpuH+N5YsKDXiy+n5/L0+ZeUTKN\n" \
              "ItCEcmLvR5vYAuguIcPZawZTmHr5AGz3tQJBAKPlB4MU3H/8C96bzqvowcseYDC9\n" \
              "Ej1HGW5KMBAV7Jlh9mf7MVgKSMN0SszvOmecPEzjRliD6p/vDgcmYcA88SUCQQCH\n" \
              "9DrhtG0uJCXEfI+tVwr/eGRfwyGpYadTFrv0fiUsfFGjfz7dazkOF0UOMwTitMRh\n" \
              "AwVHP9pfMz0IV+9tiA4FAkBMvP/VJiqEdEMRmph7xdSHSfThpsnrUAn76XseZEyA\n" \
              "4vxo2l3ntSEk+tB1IVC8adZXibq44D2MBjgXPImIOqqr\n" \
              "\n" \
              "-----END RSA PRIVATE KEY-----"

# *** Crontab ***
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'

CRONJOBS = [
    # 发送值班计划信息到企业微信群
    ('30 10,19 * * *', 'duty.views.send_duty_plan', '>> ' + os.path.join(os.path.dirname(BASE_DIR), 'crontab.log'))
]
