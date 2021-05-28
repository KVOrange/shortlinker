class Config(object):
    DEBUG = False
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///server.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '2e0f85bf2bbe4caf908390ab6464bcf0'
