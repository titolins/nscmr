from flask import (
    render_template,
    url_for,
    request,
    redirect,
    flash,
    jsonify,
    make_response)

from nscmr import app

# import forms and models --> development models only
from nscmr.admin.models import admin, users, user, categories, products

# started forms
from nscmr.forms import LoginForm
from nscmr.admin.models.userprofile import get_profile_by_email

from flask import session as login_session
from functools import wraps

import requests

@app.route('/')
def index():
    return render_template(
            'index.html',
            categories=categories,
            form=LoginForm())

#########################################################
###################### decorators #######################
#########################################################

def login_required(f):
    ''' Decorator for use with pages that require login access
    '''
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You need to login for that!")
            return redirect(url_for('index'))
    return wrap


def user_required(f):
    ''' Decorator for use with pages that require the currently logged in user
    '''
    @wraps(f)
    def wrap(*args, **kwargs):
        if kwargs['user_id'] == login_session['user_id']:
            return f(*args, **kwargs)
        flash("Only the user may have access to it's profile or delete it")
        return redirect(url_for('index'))
    return wrap


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
@app.route('/usuario/novo')
def registration():
    return render_template('registration.html', form=LoginForm())

# Read
@app.route('/usuario/<string:user_id>')
@app.route('/usuario/<string:user_id>/<string:slug>')
@user_required
def user(user_id, slug = None):
    # dev code below. Still thinking, should we pass the whole user or only
    # what we need (addresses, wishlist, etc..)?
    # Remember to change the template if we decide to pass only the needed
    # properties.
    logged_user = get_current_user()
    return render_template('user.html', user=logged_user)

# Update
@user_required
@app.route('/usuario/<string:user_id>/editar')
@app.route('/usuario/<string:user_id>/<string:slug>/editar')
def edit_user(user_id, slug = None):
    return "<p>To be user {} edit page</p>".format(user_id)

# Delete
@user_required
@app.route('/usuario/<string:user_id>/deletar')
@app.route('/usuario/<string:user_id>/<string:slug>/deletar')
def delete_user(user_id, slug = None):
    return "<p>To be user {} delete page</p>".format(user_id)


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
def category(category_id, slug = None):
    return render_template(
            'category.html',
            category=get_category_by_id(category_id),
            products=products,
            form=LoginForm())

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
def product(category_id, product_id, category_slug = None,
        product_slug = None):
    category = get_category_by_id(category_id)
    return render_template(
            'product.html',
            category = category,
            product = products[0],
            form=LoginForm())

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

def log_user(user):
    login_session['user_id'] = str(user['_id'])
    login_session['user_access_level'] = int(user['access_level'])
    login_session['username'] = user['name']
    login_session['email'] = user['email']


@app.route('/entrar', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        profile = get_profile_by_email(form.email.data)
        # no hashing or ssl implemented for now
        if profile['password'] == form.password.data:
            log_user(profile)
            return form.redirect('index')
        # in case of wrong login/password, return to last page with custom
        # error message
    else:
        return render_template(
                'index.html',
                categories=categories,
                form=form,
                login_fail=True)


@app.route('/sair')
def logout():
    del login_session['user_id']
    del login_session['user_access_level']
    del login_session['username']
    del login_session['email']
    return redirect(url_for('index'))

#########################################################
####################### end login #######################
#########################################################


#########################################################
################# development code ######################
#########################################################


@app.route('/login/log_user')
def log_regular_user():
    login_session['user_id'] = user._id_
    login_session['user_access_level'] = user.access_level
    login_session['username'] = user.name
    login_session['email'] = user.email
    return redirect(url_for('index'))


@app.route('/login/log_admin')
def log_admin_user():
    login_session['user_id'] = admin.id_
    login_session['user_access_level'] = admin.access_level
    login_session['username'] = admin.name
    login_session['email'] = admin.email
    return redirect(url_for('index'))


def get_current_user():
    if login_session['user_access_level'] > 0:
        return admin
    else:
        return user


def get_category_by_id(category_id):
    for category in categories:
        if category.id_ == category_id:
            return category

#########################################################
################# end development code ##################
#########################################################
