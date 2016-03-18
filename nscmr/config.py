class Config(object):
    DEBUG = False
    TESTING = False

    SUPPORT_CONTACT = 'example@example.com'
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_DB = 'nscmr_dev'


class TestingConfig(Config):
    TESTING = True
    MONGO_DB = 'nscmr_test'


class ProductionConfig(Config):
    # update this when db is ready
    # DATABASE_URI = ""
    MONGO_DB = 'nscmr'
