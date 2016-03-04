from flask import (
    render_template,
    url_for,
    request,
    redirect,
    flash,
    jsonify,
    make_response)

from nscmr import app #, session

# import forms and models --> development only
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
@app.route('/user/new')
def userRegistration():
    return render_template('userregistration.html')

# Read
@app.route('/user/<int:user_id>')
@user_required
def showUser(user_id):
    return render_template('user.html')

# Update
@user_required
@app.route('/user/<int:user_id>/edit')
def editUser(user_id):
    return "<p>To be user {} edit page</p>".format(user_id)

# Delete
@user_required
@app.route('/user/<int:user_id>/delete')
def deleteUser(user_id):
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
@app.route('/catalog/<int:category_id>')
def showCategory(category_id):
    return render_template(
            'category.html',
            category=getCategoryById(category_id),
            products=products)

# Update

# Delete

##################
# end Category   #
##################

##################
# Product        #
##################

# Create
# only admin will be able to create products

# Read
@app.route('/catalog/<int:category_id>/<int:product_id>')
def showProduct(category_id, product_id):
    category = getCategoryById(category_id)
    return render_template(
            'product.html',
            category = category,
            product = products[0])

# Update

# Delete

##################
# end Product    #
##################

#########################################################
####################### end CRUD ########################
#########################################################

#########################################################
####################### login ###########################
#########################################################

@app.route('/login', methods=['POST'])
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


@app.route('/logout')
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
    login_session['email'] = user.name
    return redirect(url_for('index'))

@app.route('/login/logAdminUser')
def logAdminUser():
    login_session['user_id'] = admin.id_
    login_session['user_access_level'] = admin.access_level
    login_session['username'] = admin.name
    login_session['email'] = admin.name
    return redirect(url_for('index'))

def getCategoryById(category_id):
    for category in categories:
        if category.id_ == category_id:
            return category

#########################################################
################# end development code ##################
#########################################################
