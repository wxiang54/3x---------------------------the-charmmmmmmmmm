""" All configuration values for the app """

import os

class HardCoded(object):
    """ Constants to be used throughout the application

    All hard coded settings/data that are not actual/official configuration options for Flask, Celery, or their extensions goes here.
    """

    basedir = os.path.abspath(os.path.dirname(__file__))
    
class CeleryConfig(HardCoded):
    """ Celery Configuration """
    
    # TODO

class SQLConfig(CeleryConfig):
    """ Default SQL Alchemy Configuration """

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(HardCoded.basedir, 'testing_data/stuybulletin.db')
    
    SQLALCHEMY_DATABASE_LOCATION = os.path.join(HardCoded.basedir, 'testing_data')
                                                
    SQLALCHEMY_MIGRATE_REPO = os.path.join(HardCoded.basedir, 'testing_data/migrations')
    
class Config(SQLConfig):
    """ Flask Configuration global to all environments """

    DEBUG = True
    TESTING = False
    SECRET_KEY = 'This is a very very secret key'

    # TODO
    MAIL_SERVER = 'smtp.localhost.test'
    MAIL_DEFAULT_SENDER = 'admin@demo.test'
    MAIL_SUPPRESS_SEND = True

    OAUTH_CLIENT_SECRETS = 'oauth/client_secrets.json'

    ELEMENTS_PER_PAGE = 10

class Testing(Config):
    TESTING = True

    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Production(Config):
    DEBUG = False
    MAIL_SUPPRESS_SEND = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(HardCoded.basedir, 'data/stuybulletin.db')
    SQLALCHEMY_DATABASE_LOCATION = os.path.join(HardCoded.basedir, 'data')
                                                
    SQLALCHEMY_MIGRATE_REPO = os.path.join(HardCoded.basedir, 'data/migrations')

