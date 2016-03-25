from flask import Flask

from flask.ext.login import LoginManager, current_user
from flask.ext.principal import (
    Principal,
    identity_loaded,
    RoleNeed,
    UserNeed,
    Permission)

from instance.config import config_app
from nscmr.admin import build_admin_bp
from nscmr.admin.database import build_db
from nscmr.admin.models.user import User

def build_app():
    '''
    Method for creating and configuring a flask app instance
    '''
    app = Flask(__name__)
    app.register_blueprint(build_admin_bp(), url_prefix='/admin')

    # config app environment
    config_app(app)

    # config extensions

    ###############
    # Flask-Login #
    ###############

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    ###################
    # Flask-Principal #
    ###################

    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user

        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        if hasattr(current_user, 'roles') and \
                getattr(current_user, 'roles') is not None:
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role))

    # end config extensions

    return app

app = build_app()
db = build_db(app)

from nscmr import views

# dev code
if __name__ == '__main__':
    from werkzeug.security import generate_password_hash
    from nscmr.admin.models.user import User
    u = User.get_by_id('test@example.com')
    user_content = {
        '_id': 'test@example.com',
        'name': 'dev user',
        'password': generate_password_hash('123'),
        'roles': ['user','admin'],
    }
    if u is None:
        u = User(user_content)
        u.set_defaults()
        u.insert()
    def insert_users():
        for i in range(1000):
            user_content['_id'] = 'test{}@example.com'.format(i)
            user = User(user_content)
            user.set_defaults()
            user.insert()


