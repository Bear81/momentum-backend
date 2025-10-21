from .base import *
import os
import dj_database_url

DEBUG = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = "same-origin"

DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL", ""), conn_max_age=600, ssl_require=True)
}

INSTALLED_APPS += ["cloudinary", "cloudinary_storage"]

STATICFILES_STORAGE = "cloudinary_storage.storage.StaticHashedCloudinaryStorage"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Static / media URLs (Cloudinary will host)
# STATIC_URL is already "static/" from base.py; Cloudinary will override when configured.
MEDIA_URL = "/media/"