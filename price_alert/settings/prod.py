from .comm import *

DEBUG = False

ALLOWED_HOSTS = ['*'] # TODO : set it into the app subdomain 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'price_alert',    
        'USER': 'postgres',           
        'PASSWORD': 'qqqq', 
        'HOST': 'localhost',
        'PORT': '5432',
    }
}