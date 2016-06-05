from flask import (
    session,
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

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

from functools import wraps
import requests
import json

# models
from nscmr.admin.models import (
    User,
    Category,
    Product,
    Variant,
    Summary,
    CartLine)

# started forms
from nscmr.forms import (
    LoginForm,
    RegistrationForm,
    ContactForm,
    CustomMadeForm)

from nscmr.admin.forms import AddressForm

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
    categories = Category.get_all(to_obj=True)
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
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
                    registration_form=registration_form,
                    categories=categories)
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
            registration_form=registration_form,
            categories=categories)

# Read
@app.route('/usuario')
@login_required
def user():
    return render_template('user.html',
        categories=Category.get_all(to_obj=True),
        cart=get_cart(),
        form=AddressForm())

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

# Add address
@app.route('/usuario/enderecos/adicionar', methods=['POST'])
def add_address():
    form = AddressForm()
    if form.validate_on_submit():
        data = {}
        for field in form.data.keys():
            if field in ['street_address_1', 'street_address_2', 'city',
                    'state']:
                data[field] = form.data[field].lower()
            else:
                data[field] = form.data[field]
        data['_id'] = ObjectId()
        User.update_by_id(current_user.id, push_data={'addresses':data})
    return render_template('user.html',
        categories=Category.get_all(to_obj=True),
        cart=get_cart(),
        form=form)


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
    categories = Category.get_all(to_obj=True)
    category = [c for c in categories if c.permalink == permalink][0]
    categories.remove(category)
    products = Summary.get_by_category(category.id)
    return render_template(
            'category.html',
            # we don't need to access both category and products collection,
            # considering that each product has a manual reference to the
            # category it belongs.. good opportunity to see which category
            # fields we need in the products ref
            category=category,
            categories=categories,
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
@app.route('/catalogo/<string:c_permalink>/<string:p_permalink>/<string:v_id>')
@back.anchor
def product(c_permalink, p_permalink, v_id):
    #category = Category.get_by_permalink(c_permalink)
    categories = Category.get_all()
    product = Product.get_by_permalink(p_permalink, to_obj=True)
    var = Variant.get_by_id(v_id, to_obj=True)
    return render_template(
        'product.html',
        categories = categories,
        product = product,
        variant = var,
        attributes = product.attributes,
        login_form=LoginForm())

# Update
# Delete
# only admin can update or delete products

##################
# Cart/Orders    #
##################

def get_cart():
    if current_user.is_anonymous:
        cart = session.get('cart', [])
    else:
        cart = current_user.cart
    return [CartLine(item)() for item in cart]

@app.route('/usuario/compras')
def cart():
    response = make_response(json.dumps(get_cart()), 200)
    response.headers['Content-Type'] = 'application/json'
    print(response)
    return response

@app.route('/usuario/carrinho/adicionar', methods=['POST'])
def add_to_cart():
    variant_id = request.json['variant_id']
    cart_line = { '_id': variant_id, 'quantity': 1 }
    if current_user.is_anonymous:
        if session.get('cart', None) is None:
            session['cart'] = []
        inc = False
        for item in session['cart']:
            if item['_id'] == variant_id:
                item['quantity'] += 1
                inc = True
        if not inc:
            session['cart'].append(cart_line)
    else:
        result = User._update_one(
                {'_id': current_user.id, 'cart._id': variant_id},
                inc_data = {'cart.$.quantity': 1 })
        if result.modified_count == 0:
            print('none modified')
            result = User.update_by_id(current_user.id, push_data={'cart': cart_line})
            print('push result = {}'.format(result))
        else:
            print('modified')
    response = make_response(
        json.dumps('Produto adicionado ao seu carrinho!'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/usuario/carrinho/editar', methods=['POST'])
def edit_cart():
    qty = int(request.json['quantity'])
    if qty < 0:
        response = make_response(
            json.dumps(
                'Não é possível alterar a quantidade para um número negativo'),
            200)
        response.headers['Content-Type'] = 'application/json'
    elif qty == 0:
        # remove item from cart
        User.update_by_id(current_user.id,
                pull_data={'cart': {'_id': request.json['id'] }})
        response = make_response(
            json.dumps('Produto removido do seu carrinho!'), 200)
        response.headers['Content-Type'] = 'application/json'
    else:
        # decrement/increment
        User._update_one(
            {'_id': current_user.id, 'cart._id': request.json['id'] },
            set_data={'cart.$.quantity': request.json['quantity'] })
        response = make_response(
            json.dumps('Quantidade do produto alterada!'), 200)
        response.headers['Content-Type'] = 'application/json'
    return response


######################
# end Cart/Orders    #
######################

#########################################################
####################### end CRUD ########################
#########################################################

#########################################################
####################### login ###########################
#########################################################


@app.route('/entrar', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data.lower(), to_obj=True)
        # no hashing or ssl implemented for now
        if user is not None and user.check_password(form.password.data):
            # Flask-Login
            login_user(user)
            identity_changed.send(
                    current_app._get_current_object(),
                    identity=Identity(str(user.id)))
            # update user cart with cart from session, if existing
            if session.get('cart', None) is not None:
                for item in session['cart']:
                    if User._update_one({'cart._id': item['_id']}, inc_data=\
                                        {'cart.$.quantity': item['quantity'] }).\
                            modified_count == 0:
                        User.update_by_id(current_user.id, push_data={'cart': item})
                del(session['cart'])
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
######################### misc #########################
#########################################################

@app.route('/contato', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    categories = Category.get_all(to_obj=True)
    if form.validate_on_submit():
        # send email...
        pass
    return render_template(
        'contact.html',
        form=form,
        login_form=LoginForm(),
        categories=categories)

@app.route('/sobre')
def about():
    categories = Category.get_all(to_obj=True)
    return render_template(
        'aboutus.html',
        login_form=LoginForm(),
        categories=categories)

@app.route('/sobmedida', methods=['GET', 'POST'])
def custom_made():
    form = CustomMadeForm()
    categories = Category.get_all(to_obj=True)
    if form.validate_on_submit():
        # notify custom made request -- how, email?
        pass
    return render_template(
        'custommade.html',
        form=form,
        login_form=LoginForm(),
        categories=categories)

@app.route('/trocas', methods=['GET', 'POST'])
def returns():
    form = ContactForm()
    categories = Category.get_all(to_obj=True)
    if form.validate_on_submit():
        # send email...
        pass
    return render_template('returns.html',
        form=form,
        login_form=LoginForm(),
        categories=categories)

@app.route('/lavanderia')
def wash():
    return render_template(
        'wash.html',
        login_form=LoginForm(),
        categories=Category.get_all(to_obj=True))

#########################################################
####################### end misc ########################
#########################################################

#########################################################
###################### end routes  ######################
#########################################################

