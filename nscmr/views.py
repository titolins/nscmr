from flask import (
    render_template,
    url_for,
    request,
    redirect,
    flash,
    jsonify,
    make_response,
    current_app)

# Flask-Login
from flask.ext.login import (
    login_user,
    logout_user,
    login_required,
    current_user)

from flask.ext.principal import (
    identity_changed,
    Identity,
    AnonymousIdentity)

from bson import ObjectId

from pymongo.errors import DuplicateKeyError

from functools import wraps
import requests

# models
from nscmr.admin.models import User, Category, Product

# started forms
from nscmr.forms import LoginForm, ProfileForm, AddressForm, RegistrationForm

# helpers
from nscmr.helper.back import Back

# app
from nscmr import app

#########################################################
######################## routes #########################
#########################################################

back = Back()

@app.route('/')
@back.anchor
def index():
    return render_template(
            'index.html',
            # get the objects as we need the slug
            categories=Category.get_all(to_obj=True),
            login_form=LoginForm())


#########################################################
######################## CRUD ###########################
#########################################################

##################
# User           #
##################

# Create
@app.route('/usuario/novo', methods=['GET', 'POST'])
def registration():
    registration_form = RegistrationForm(request.form)
    if request.method == 'POST' and registration_form.validate_on_submit():
        try:
            user = User.from_form(registration_form.data)
            user.insert()
            flash('Cadastro bem sucedido! Você já pode fazer suas compras')
            login_user(user)
            return back.redirect()
        except DuplicateKeyError:
            registration_form.email.errors.append(
                'Este email já está cadastrado em nosso site')
            return render_template(
                    'registration.html',
                    login_form=LoginForm(),
                    registration_form=registration_form)
        except Exception as e:
            flash(
                ('Ocorreu um erro. Por favor, tente novamente. Se o erro, '
                'persistir, contate-nos em: {}\nMensagem de erro:\n{}').\
                        format(app.config.get(
                            'SUPPORT_CONTACT', ''), str(e)))
            return redirect(url_for('registration'))
    return render_template(
            'registration.html',
            login_form=LoginForm(),
            registration_form=registration_form)

# Read
@app.route('/usuario')
@login_required
def user():
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
@app.route('/catalogo/<string:permalink>')
@back.anchor
def category(permalink):
    # get objects so we may retrieve the category from any of the products
    # and get category object because we need the slug
    category = Category.get_by_permalink(permalink)
    products = Product.get_by_category(category['_id'])
    return render_template(
            'category.html',
            # we don't need to access both category and products collection,
            # considering that each product has a manual reference to the
            # category it belongs.. good opportunity to see which category
            # fields we need in the products ref
            category=category,
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
@app.route('/catalogo/<string:c_permalink>/<string:p_permalink>')
@back.anchor
def product(c_permalink, p_permalink):
    category = Category.get_by_permalink(c_permalink)
    product = Product.get_by_permalink(p_permalink)
    return render_template(
            'product.html',
            category = category,
            product = product,
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
        user = User.get_by_id(form.email.data, to_obj=True)
        # no hashing or ssl implemented for now
        if user is not None and user.check_password(form.password.data):
            # Flask-Login
            login_user(user)
            identity_changed.send(
                    current_app._get_current_object(),
                    identity=Identity(user.id))
            flash('Log-in bem sucedido! Você já pode fazer suas compras')
            return back.redirect()
        # in case of wrong login/password, return to last page with custom
        # error message
        flash("E-mail ou senha incorreto(s)")
        # test code
        #form.errors['form'].append("E-mail ou senha incorreto(s)")
        return back.redirect()
    else:
        return render_template(
                'index.html',
                categories=Category.get_all(),
                login_form=form,
                login_fail=True)


@app.route('/sair')
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity())
    flash('Você saiu da sua conta')
    return back.redirect()

#########################################################
####################### end login #######################
#########################################################

#########################################################
###################### end routes  ######################
#########################################################

