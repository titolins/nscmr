from flask import (
    render_template,
    url_for,
    request,
    redirect,
    flash,
    jsonify,
    make_response)

from nscmr import app

# Flask-Login
from flask.ext.login import (
    login_user,
    logout_user,
    login_required,
    current_user)

from pymongo.errors import DuplicateKeyError

from functools import wraps
import requests

# import forms and models --> development models only
from nscmr.admin.models import admin, users, user, categories, products

# real models
from nscmr.admin.models.user import User

# started forms
from nscmr.forms import LoginForm, RegistrationForm

# helpers
from nscmr.helper import back


@app.route('/')
@back.anchor
def index():
    return render_template(
            'index.html',
            categories=categories,
            login_form=LoginForm())

#########################################################
###################### decorators #######################
#########################################################


"""
def admin_required(f):
    ''' Decorator for use with pages that require admin privileges
    '''
    @wraps(f)
    def wrap(*args, **kwargs):
        if kwargs['user_access_level'] == login_session['user_access_level']:
            return f(*args, **kwargs)
        flash("Area restricted to admins only!")
        return redirect(url_for('index'))
    return wrap
"""


#########################################################
################### end decorators ######################
#########################################################

#########################################################
######################## CRUD ###########################
#########################################################

##################
# User           #
##################

# Create
@app.route('/usuario/novo', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            user = User.from_form(form.data)
            user.save()
            flash('Cadastro bem sucedido! Você já pode fazer suas compras')
            login_user(user)
            return back.redirect()
        except DuplicateKeyError:
            flash('Este email já está cadastrado em nosso site')
            return redirect(url_for('registration'))
        except Exception as e:
            flash(
                ('Ocorreu um erro. Por favor, tente novamente. Se o erro, '
                'persistir, contate-nos em: {}\nMensagem de erro:\n{}').\
                        format(app.config.get('SUPPORT_CONTACT', ''), str(e)))
            return redirect(url_for('registration'))
    return render_template(
            'registration.html',
            login_form=LoginForm(),
            registration_form=form)

# Read
@app.route('/usuario')
@login_required
def user():
    # dev code below. Still thinking, should we pass the whole user or only
    # what we need (addresses, wishlist, etc..)?
    # Remember to change the template if we decide to pass only the needed
    # properties.
    return render_template('user.html')

# Update
@app.route('/usuario/editar')
@login_required
def edit_user():
    return "<p>To be user {} edit page</p>".format(current_user.get_id())

# Delete
@app.route('/usuario/deletar')
@login_required
def delete_user():
    return "<p>To be user {} delete page</p>".format(current_user.get_id())


##################
# end User       #
##################

##################
# Category       #
##################

# Create
# only the admin can create new categories

# Read
@app.route('/catalogo/<string:category_id>/<string:slug>')
@back.anchor
def category(category_id, slug = None):
    return render_template(
            'category.html',
            category=get_category_by_id(category_id),
            products=products,
            login_form=LoginForm())

# Update
# Delete
# only the admin can update and delete categories

##################
# end Category   #
##################

##################
# Product        #
##################

# Create
# only admin will be able to create products

# Read
@app.route(
        '/catalogo/{}/{}/{}/{}'.format(
            '<string:category_id>',
            '<string:category_slug>',
            '<string:product_id>',
            '<string:product_slug>',)
        )
@back.anchor
def product(category_id, product_id, category_slug = None,
        product_slug = None):
    category = get_category_by_id(category_id)
    return render_template(
            'product.html',
            category = category,
            product = products[0],
            login_form=LoginForm())

# Update
# Delete
# only admin can update or delete products

##################
# end Product    #
##################

#########################################################
####################### end CRUD ########################
#########################################################

#########################################################
####################### login ###########################
#########################################################


@app.route('/entrar', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.get_by_id(form.email.data)
        # no hashing or ssl implemented for now
        if user.check_password(form.password.data):
            # Flask-Login
            login_user(user)
            flash('Log-in bem sucedido! Você já pode fazer suas compras')
            return back.redirect()
        # in case of wrong login/password, return to last page with custom
        # error message
        flash("E-mail ou senha incorreto(s)")
        return back.redirect()
    else:
        return render_template(
                'index.html',
                categories=categories,
                login_form=form,
                login_fail=True)


@app.route('/sair')
def logout():
    logout_user()
    flash('Logged out')
    return back.redirect()


#########################################################
####################### end login #######################
#########################################################


#########################################################
################# development code ######################
#########################################################


def get_category_by_id(category_id):
    for category in categories:
        if category.id_ == category_id:
            return category

#########################################################
################# end development code ##################
#########################################################
