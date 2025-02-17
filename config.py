from os import environ, path
import os



class Config:
    # General Flask Config
    SECRET_KEY = b'ergergergergegg/'
    USE_PROXYFIX = True

    APPLICATION_ROOT = '/'

    FLASK_APP = 'app.py'
    FLASK_RUN_HOST = '0.0.0.0'
    FLASK_RUN_PORT = 80

    #FLASK_DEBUG = 1
    #FLASK_ENV = "development" #production
    #DEBUG = True

    # no double mqtt message config

    FLASK_DEBUG = 1
    FLASK_ENV = "development" #production
    #FLASK_ENV = "production"  # production

    DEBUG = True # IF PROBLEMS WITH MQTT SET THIS TO FALSE
    TESTING = False #True

    SESSION_TYPE = 'sqlalchemy' #'redis'
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SESSION_COOKIE_NAME = 'my_cookieGetFace'
    SESSION_PERMANENT = True
    