import os 
import dj_database_url
from .comm import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'price-alert.akrambensouici.com,api.price-alert.akrambensouici.com').split(',')

CORS_ALLOWED_ORIGINS = [
    "https://price-alert.akrambensouici.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://price-alert.akrambensouici.com",
    "https://api.price-alert.akrambensouici.com",
]

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('PRICE_ALERT_DATABASE_URL'))
}

DOMAIN = "price-alert.akrambensouici.com"