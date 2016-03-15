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

def config_app(app, app_mode = 'debug'):
    from instance.secret import install_secret_key
    install_secret_key(app)
    app.config.from_object(Config)
    if app_mode == 'debug':
        app.config.from_object(DevelopmentConfig)
    elif app_mode == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(ProductionConfig)


