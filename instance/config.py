import os

config = {
    "development": "nscmr.config.DevelopmentConfig",
    "testing": "nscmr.config.TestingConfig",
    "production": "nscmr.config.ProductionConfig",
    "default": "nscmr.config.DevelopmentConfig"
}

def config_app(app):
    from instance.secret import install_secret_key
    #from flask_bootstrap import Bootstrap
    #from flask_wtf.csrf import CsrfProtect

    install_secret_key(app)
    # add those later on..
    #Bootstrap(app)
    #CsrfProtect(app)

    app.config.from_object(config[os.environ.get('FLASK_APP_MODE', 'default')])

