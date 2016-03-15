from flask import Flask

from instance.config import config_app

#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker

def build_app():
    # import blueprints and register
    import nscmr.admin
    app = Flask(__name__)
    app.register_blueprint(admin.bp, url_prefix='/admin')
    # config app and return
    config_app(app)
    return app

app = build_app()

# create db engine
# engine = create_engine('path/to/db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

from nscmr import views
