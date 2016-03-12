from flask import (
    render_template,
    url_for,
    request,
    redirect,
    flash,
    jsonify,
    make_response)

#from . import app #, session
from nscmr import app

# import forms and models --> development models only
from nscmr.models import admin, users, user, categories, products

from flask import session as login_session
from functools import wraps

import requests

@app.route('/')
def index():
    return render_template('index.html', categories=categories)

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
            return redirect(url_for('login'))
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
def userRegistration():
    return render_template('userregistration.html')

# Read
@app.route('/usuario/<int:user_id>')
@app.route('/usuario/<int:user_id>/<string:slug>')
@user_required
def showUser(user_id, slug = None):
    # dev code below. Still thinking, should we pass the whole user or only
    # what we need (addresses, wishlist, etc..)?
    # Remember to change the template if we decide to pass only the needed
    # properties.
    logged_user = getCurrentUser()
    return render_template('user.html', user=logged_user)

# Update
@user_required
@app.route('/usuario/<int:user_id>/editar')
@app.route('/usuario/<int:user_id>/<string:slug>/editar')
def editUser(user_id, slug = None):
    return "<p>To be user {} edit page</p>".format(user_id)

# Delete
@user_required
@app.route('/usuario/<int:user_id>/deletar')
@app.route('/usuario/<int:user_id>/<string:slug>/deletar')
def deleteUser(user_id, slug = None):
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
@app.route('/catalogo/<int:category_id>/<string:slug>')
def showCategory(category_id, slug = None):
    return render_template(
            'category.html',
            category=getCategoryById(category_id),
            products=products)

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
            '<int:category_id>',
            '<string:category_slug>',
            '<int:product_id>',
            '<string:product_slug>',)
        )
def showProduct(category_id, product_id, category_slug = None,
        product_slug = None):
    category = getCategoryById(category_id)
    return render_template(
            'product.html',
            category = category,
            product = products[0])

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
    return """
        <h1>Login Page</h1>

        <div style='background: lightblue; width: 200px; height:50px;'>
            <a href="{0}">
                Regular user
            </a>
        </div>
        <div style='background: lightgreen; width: 200px; height:50px;'>
            <a href="{1}">
                Admin user
            </a>
        </div>
    """.format(url_for('logRegularUser'), url_for('logAdminUser'))


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


@app.route('/login/logRegularUser')
def logRegularUser():
    login_session['user_id'] = user.id_
    login_session['user_access_level'] = user.access_level
    login_session['username'] = user.name
    login_session['email'] = user.email
    return redirect(url_for('index'))


@app.route('/login/logAdminUser')
def logAdminUser():
    login_session['user_id'] = admin.id_
    login_session['user_access_level'] = admin.access_level
    login_session['username'] = admin.name
    login_session['email'] = admin.email
    return redirect(url_for('index'))


def getCurrentUser():
    if login_session['user_access_level'] > 0:
        return admin
    else:
        return user


def getCategoryById(category_id):
    for category in categories:
        if category.id_ == category_id:
            return category

#########################################################
################# end development code ##################
#########################################################