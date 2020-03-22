import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#ENVIRONMENT = os.environ.get('ENVIRONMENT', default='debug')   #production
ENVIRONMENT = 'debug'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#_0)(%$2pipfw-14aoqz&9kmu%ex8$_8u35gj99=je7t_asf*7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False #True  # deploy 시는 False로 변경.

# 나중에 호스팅 업체 선정하면 반드시 수정해야 한다.
#ALLOWED_HOSTS = ['.herokuapp.com', 'localhost', '127.0.0.1']
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions', #세션용
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', #배포용 라이브러리
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',  # 숫자 천자리 콤마 표시용.

    # 사용자 개발앱
    #'pages.apps.PagesConfig',
    'stock.apps.StockConfig',
    #'orders.apps.OrdersConfig', 그냥 stock 아래로 진행하자..

    # Third-party
    'crispy_forms',
    'allauth',
    'allauth.account',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # 배포용.
    'django.contrib.sessions.middleware.SessionMiddleware', #세션용.
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'config.urls'

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # 세션용
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# pythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yosoysim$erp', #db name
        'USER': 'yosoysim',
        'PASSWORD' : 'orange!1',
        'HOST': 'yosoysim.mysql.pythonanywhere-services.com',
        'PORT': "",
    }
}


# localhost
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'erp', #db name
        'USER': 'root',
        'PASSWORD' : '123456',
        'HOST': '127.0.0.1',
        'PORT': "",
    }
}
"""

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/stock/static/'   # 그냥 /static/만 할 경우 프로젝트의 하위 폴더를 찾는다!!
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'stock/static'),]
STATIC_ROOT = os.path.join(BASE_DIR, 'stock/staticfiles')
#아래는 굳이 안 해도 되는데, 명시적으로 하기 위해.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


#AUTH_USER_MODEL = 'users.CustomUser' # 이것 추가하면 에러 발생하니 주석 해제 말 것..

LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT = 'home'

# django-crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# django-allauth config
LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT = 'home'

SITE_ID = 1


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST=os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER=os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT=os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS=os.environ.get('EMAIL_USE_TLS')

ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

# django-allauth config end

DEFAULT_FROM_EMAIL = 'simkal@naver.com'

# django-debug-toolbar (docker 기준)
#import socket
#hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = '127.0.0.1' #'[ip[:-1] + "1" for ip in ips]

# production
if ENVIRONMENT == 'production':
    SECURE_BROWSER_XSS_FILTER = True # cross-site request forgery protection
    X_FRAME_OPTIONS = 'DENY' # clickjacking proyection
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Heroku
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)