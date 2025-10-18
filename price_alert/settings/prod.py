import os 
import dj_database_url
from .comm import *

DEBUG = False

ALLOWED_HOSTS = ['price-alert.akrambensouici.com']

CORS_ALLOWED_ORIGINS = [
    "https://app.price-alert.akrambensouici.com",
]

CSRF_TRUSTED_ORIGINS = ['https://price-alert.akrambensouici.com']

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('PRICE_ALERT_DATABASE_URL'))
}

DOMAIN = "app.price-alert.akrambensouici.com"