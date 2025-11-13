import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
from decouple import config

# ---------------------------------------------------------
# BASE DIRECTORY & ENVIRONMENT
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # load .env variables

# ---------------------------------------------------------
# BASIC SETTINGS
# ---------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS", "localhost"
).split(",")

AUTH_USER_MODEL = "accounts.UserProfile"

# ---------------------------------------------------------
# SECURITY SETTINGS
# ---------------------------------------------------------
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False  # set True after confirming HTTPS works
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ---------------------------------------------------------
# INSTALLED APPS
# ---------------------------------------------------------
INSTALLED_APPS = [
    # Your apps
    "django_daraja",
    "payments",
    "accounts",
    "church_app",
    "blog_app",
    "library_app",

    # Third-party
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework.authtoken",

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------
# CORS CONFIGURATION
# ---------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "https://churchmedia.kahawawendanisda.org",
    "https://kahawawendanisda.org",
]
CORS_ALLOW_CREDENTIALS = True

# ---------------------------------------------------------
# URLS & TEMPLATES
# ---------------------------------------------------------
ROOT_URLCONF = "wendani_project.urls"

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

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
        "OPTIONS": {"sslmode": "require"},  # only if using external DB
    }
}

# ---------------------------------------------------------
# STATIC FILES (served via Nginx)
# ---------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# ---------------------------------------------------------
# MEDIA FILES (served via S3)
# ---------------------------------------------------------
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = "churchmedia.kahawawendanisda.org"  # your subdomain
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_DEFAULT_ACL = "public-read"

DEFAULT_FILE_STORAGE = "wendani_project.storage_backends.MediaStorage"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"

# ---------------------------------------------------------
# REST FRAMEWORK & JWT
# ---------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=12),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ---------------------------------------------------------
# MPESA CONFIGURATION
# ---------------------------------------------------------
MPESA_ENVIRONMENT = config("MPESA_ENVIRONMENT", default="sandbox")
MPESA_CONSUMER_KEY = config("MPESA_CONSUMER_KEY")
MPESA_CONSUMER_SECRET = config("MPESA_CONSUMER_SECRET")
MPESA_SHORTCODE = config("MPESA_SHORTCODE")
MPESA_EXPRESS_SHORTCODE = config("MPESA_EXPRESS_SHORTCODE")
MPESA_PASSKEY = config("MPESA_PASSKEY")
MPESA_SHORTCODE_TYPE = "paybill"  # 'paybill' or 'till_number'
