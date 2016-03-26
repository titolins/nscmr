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
from nscmr.admin.models import User

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
    ########
    # user #
    ########

    # create admin
    from werkzeug.security import generate_password_hash
    from nscmr.admin.models import User, Category, Product
    user_content = {
        '_id': 'admin@studioduvet.com',
        'name': 'administrador',
        'password': generate_password_hash('admin'),
        'roles': ['user','admin'],
    }
    u = User.get_by_id('admin@studioduvet.com')
    try:
        u.id
    except:
        u = User(user_content)
        u.set_defaults()
        u.insert()
    # create regular users
    def insert_users():
        user_content['roles'] = ['user']
        for i in range(1000):
            user_content['_id'] = 'test{}@example.com'.format(i)
            user = User(user_content)
            user.set_defaults()
            user.insert()

    #########
    # admin #
    #########
    # fields = ['name', 'parent', 'ancestors', 'thumbnail', 'header']
    category_content = {
        'name': '',
        'parent': None,
        'ancestors': [],
        'thumbnail' : 'http://placehold.it/400x300',
        'header': 'http://placehold.it/1400x400',
    }
    categories = ['Lençóis', 'Toalhas de mesa', 'Peseiras', 'Acessórios',
        'Duvets', 'Colchas']
    for category in categories:
        category_content['name'] = category
        c = Category(category_content.copy())
        try:
            c.insert()
        except Exception as e:
            print(e)

    def insert_products(n=9):
        categories = Category.get_all()
        for category in categories:
            for i in range(9):
                description = (
                        'FEITO COM PERCAL 7000 FIOS DA ÍNDIA ORIENTAL',
                        'IDEAL PARA CASAS DE CAMPO, SÍTIOS, FAZENDAS ETC.')
                product_content = {
                    'name': 'Lençol com estampa florida c/ tecido importado',
                    'description': description,
                    'price': 450.00,
                    'size': "3.50m x 2.50m",
                    'thumbnail': "http://placehold.it/400x300",
                    'background': "http://placehold.it/1920x1080",
                    'category': category
                }
                p = Product(product_content)
                p.insert()

