import os

from flask import Flask

from flask.ext.login import LoginManager, current_user
from flask.ext.principal import (
    Principal,
    identity_loaded,
    RoleNeed,
    UserNeed,
    Permission)
from flask.ext.assets import Environment, Bundle
from flask.ext.session import Session

from nscmr.admin import build_admin_bp
from nscmr.admin.database import build_db
from nscmr.admin.models import User
from nscmr.admin.forms import category_images, product_images

from flask_wtf import CsrfProtect
from flask_uploads import configure_uploads

def build_app():
    '''
    Method for creating and configuring a flask app instance
    '''
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(build_admin_bp(), url_prefix='/admin')

    # Load the default configuration
    app.config.from_object('nscmr.config.default')

    # Load the configuration from the instance folder
    app.config.from_pyfile('config.py')

    # Load the configuration specified by the APP_CONFIG_FILE environment var
    app.config.from_envvar('APP_CONFIG_FILE')

    # config extensions

    ###############
    # Flask-Login #
    ###############

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id, to_obj=True)

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

    #############
    # Flask-WTF #
    #############

    CsrfProtect(app)

    #################
    # Flask-Uploads #
    #################

    configure_uploads(app, (category_images, product_images))

    ################
    # Flask-Assets #
    ################

    assets = Environment(app)
    assets.load_path = [
        os.path.join(app.root_path, 'static/sass'),
        os.path.join(app.root_path, 'static/js'),
        os.path.join(app.root_path, 'bower_components'),
    ]

    assets.register(
        'js_base',
        Bundle(
            'jquery/dist/jquery.min.js',
            'bootstrap/dist/js/bootstrap.min.js',
            'angular/angular.min.js',
            'cart.js',
            'duvet.js'),
        output='js/base.js')

    '''
    assets.register(
        'angular',
        Bundle(
            'angular/angular.min.js',
            'angular_config.js'),
        output='js/angular.js')
    '''

    assets.register(
        'css_all',
        Bundle(
            'bootstrap/dist/css/bootstrap.min.css',
            'font-awesome/css/font-awesome.min.css',
            Bundle(
                'style.scss',
                filters='scss',
                output='css/style.css')),
        output='css/all.css')

    #################
    # Flask session #
    #################

    Session(app)

    # end config extensions

    return app


app = build_app()
db = build_db(app)

from nscmr import views


