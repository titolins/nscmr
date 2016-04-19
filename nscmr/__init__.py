from flask import Flask

from flask.ext.login import LoginManager, current_user
from flask.ext.principal import (
    Principal,
    identity_loaded,
    RoleNeed,
    UserNeed,
    Permission)

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

    # end config extensions

    #############
    # Flask-WTF #
    #############

    CsrfProtect(app)

    #################
    # Flask-Uploads #
    #################

    configure_uploads(app, (category_images, product_images))


    return app


app = build_app()
db = build_db(app)

from nscmr import views

# dev code
if __name__ == '__main__':

    # create admin
    from werkzeug.security import generate_password_hash
    from nscmr.admin.helper import slugify
    from nscmr.admin.models import User, Product, Category
    user_content = {
        '_id': 'admin@studioduvet.com',
        'name': 'administrador',
        'password': generate_password_hash('admin'),
        'roles': ['user','admin'],
    }
    u = User.get_by_id('admin@studioduvet.com',to_obj=True)
    try:
        u.id
    except:
        u = User(user_content)
        u.set_defaults()
        u.insert()

    def insert_product(category_permalink):
        category = Category.get_by_permalink(category_permalink)
        description = "{} feito com percal 5000 fios".format(category['name'])
        name = "{} estampado".format(category['name'])
        permalink = slugify(name)
        price = "450.00"
        big_image = "http://placehold.it/1920x1080"
        thumb_image = "http://placehold.it/128x128"
        image = { 'big': big_image, 'thumb': thumb_image }
        images = [image for i in range(20)]
        cat = { 'name' : category['name'], '_id': category['_id'] }
        product = {
            'name': name,
            'description': description,
            'category': cat,
            'images': images,
            'permalink': permalink
        }
        p = Product(product)
        p.insert()


