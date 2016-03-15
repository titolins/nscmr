class Config(object):
    DEBUG = False
    TESTING = False

    # update this when db is ready
    # DATABASE_URI = ""

class ProductionConfig(Config):
    # update this when db is ready
    # DATABASE_URI = ""
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

