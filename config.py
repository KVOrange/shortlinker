class Config(object):
    DEBUG = False
    CSRF_ENABLED = False
    SECRET_KEY = '2e0f85bf2bbe4caf908390ab6464bcf0'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///server.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
