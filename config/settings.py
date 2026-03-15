import os
from pathlib import Path
from dotenv import load_dotenv

# --------------------------------------------------
# Base Directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

# Using openai api-------------------

# LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# --------------------------------------------------
# Local Model Setting
# --------------------------------------------------

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:3.8b")




# Security
# --------------------------------------------------

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "ma@c%al1hx#=@s@_&cj=o7!=t=l2k-3l#i1^kij&=uxhu@gxlr")

DEBUG = True

ALLOWED_HOSTS = []

# --------------------------------------------------
# Installed Apps
# --------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party
    "rest_framework",

    # Local apps
    "categorization",
]

# --------------------------------------------------
# Middleware
# --------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# Root URL Configuration
# --------------------------------------------------

ROOT_URLCONF = "config.urls"

# --------------------------------------------------
# Templates (Required by Django)
# --------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# --------------------------------------------------
# WSGI Application
# --------------------------------------------------

WSGI_APPLICATION = "config.wsgi.application"

# --------------------------------------------------
# Database (Not required but Django needs one)
# We'll use lightweight SQLite
# --------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --------------------------------------------------
# Password Validation (Django default)
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
]

# --------------------------------------------------
# Internationalization
# --------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# --------------------------------------------------
# Static Files
# --------------------------------------------------

STATIC_URL = "static/"

# --------------------------------------------------
# Default Primary Key
# --------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------
# Logging Configuration
# (Required by assignment)
# --------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "%(levelname)s | %(asctime)s | %(name)s | %(message)s"
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },

    "loggers": {
        "transaction_categorizer": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}