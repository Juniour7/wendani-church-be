import os
from pathlib import Path
from dotenv import load_dotenv
from decouple import config
from datetime import timedelta



BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# -------------------------------------------------------------------
# BASIC SETTINGS
# -------------------------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY")  # <- change from DJANGO_SECURITY_KEY to SECRET_KEY
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

AUTH_USER_MODEL = 'accounts.UserProfile'


# --------------------------
# SECURITY MIDDLEWARE & HEADERS
# ---------------------------

# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True

# HTTP Strict Transport Security (forces browsers to use HTTPS)
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False  # set to True only after confirming HTTPS is fully working

# Prevent information leaks and some browser-based attacks
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Clickjacking protection (use "SAMEORIGIN" if you use frames within your own site)
X_FRAME_OPTIONS = "DENY"

# Ensures Django knows it's behind a proxy/load balancer using HTTPS (e.g., Render, Nginx)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")



# -------------------------------------------------------------------
# APPLICATIONS
# -------------------------------------------------------------------

INSTALLED_APPS = [
    'django_daraja',
    'payments',
    'accounts',
    'church_app',
    'blog_app',
    'library_app',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework.authtoken',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'wendani_project.urls'

# -------------------------------------------------------------------
# DATABASE
# -------------------------------------------------------------------

# Python Anywhere DB
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.getenv("PA_DB_NAME"),
#         'USER': os.getenv("PA_DB_USER"),
#         'PASSWORD': os.getenv("PA_DB_PASSWORD"),
#         'HOST': os.getenv("PA_DB_HOST"),
#         'PORT': os.getenv("PA_DB_PORT", "3306"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}

# Local DB For Testing
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',  # Path to the SQLite database file
#     }
# }



# -------------------------------------------------------------------
# STATIC FILES
# -------------------------------------------------------------------

# Static and Media files
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

STATIC_URL = f'https://churchmedia.kahawawendanisda.org/{STATICFILES_LOCATION}/'
MEDIA_URL = f'https://churchmedia.kahawawendanisda.org/{MEDIAFILES_LOCATION}/'

# Storage Backends
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# -------------------------------------------------------------------
# REST FRAMEWORK / JWT
# -------------------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Mpesa Configurations
MPESA_ENVIRONMENT = config('MPESA_ENVIRONMENT', default='sandbox')
MPESA_CONSUMER_KEY = config('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = config('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = config('MPESA_SHORTCODE')
MPESA_EXPRESS_SHORTCODE = config('MPESA_EXPRESS_SHORTCODE')
MPESA_PASSKEY = config('MPESA_PASSKEY')
MPESA_SHORTCODE_TYPE = 'paybill' # Use 'till_number' for Buy Goods

# AWS S3 Settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = 'public-read'