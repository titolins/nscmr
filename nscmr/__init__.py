from flask import Flask

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
    return app

app = build_app()
db = build_db(app)

from nscmr import views
