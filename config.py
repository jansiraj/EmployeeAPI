class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'GDtfDCFYjD'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///company.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False