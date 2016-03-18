from flask import Flask

from flask.ext.login import LoginManager

from instance.config import config_app
from nscmr.admin.database import build_db

def build_app():
    '''
    Method for creating and configuring a flask app instance
    '''
    # import blueprints and register
    import nscmr.admin as admin
    app = Flask(__name__)
    app.register_blueprint(admin.bp, url_prefix='/admin')
    # config app and return
    config_app(app)
    # starts Flask-Login
    login_manager.init_app(app)

    return app

# instantiates the login_manager outside the build_app method to allow us to
# import it later..
login_manager = LoginManager()
app = build_app()
db = build_db(app)

from nscmr import views
