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

from datetime import datetime
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

#mundipagg
from data_contracts import creditcard, creditcard_transaction, \
    creditcard_transaction_options, create_sale_request, order
from mundipaggOnePython import GatewayServiceClient
from enum_types import PlatformEnvironment, HttpContentTypeEnum
import uuid

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
    CartLine,
    Order)

# started forms
from nscmr.forms import (
    LoginForm,
    RegistrationForm,
    ContactForm,
    CustomMadeForm,
    CreditCardForm)

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

@app.route('/usuario/enderecos')
@login_required
def get_addresses():
    user = User.get_by_id(current_user.id, projection={
        '_id': 0,
        'addresses': 1})
    for addr in user['addresses']:
        addr['_id'] = str(addr['_id'])
    response = make_response(json.dumps(user['addresses']),200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/usuario')
@login_required
def get_user():
    user = User.get_by_id(current_user.id, projection={
        '_id': 0,
        'email': 1,
        'name':1,
        'addresses': 1,
        'dob': 1,
        'orders': 1})
    user['dob'] = \
        str(user['dob']).split(' ')[0] if 'dob' in user.keys() else None
    for addr in user['addresses']:
        addr['_id'] = str(addr['_id'])
    response = make_response(json.dumps(user),200)
    response.headers['Content-Type'] = 'application/json'
    return response

# Read
@app.route('/usuario/perfil')
@login_required
def user():
    return render_template('user.html',
        categories=Category.get_all(to_obj=True),
        form=AddressForm())

# Delete
@app.route('/usuario/editar', methods=['POST'])
@login_required
def edit_user():
    data = {}
    for field in request.json:
        if field in ('name', 'email'):
            data[field] = request.json[field].lower()
        elif field == 'dob':
            data[field] = datetime.strptime(request.json[field], "%d/%m/%Y")
        else:
            #ignore unwanted fields
            continue
    res = User.update_by_id(current_user.id, set_data=data)
    if res.modified_count > 0:
        response = make_response(json.dumps('Alterações realizadas!'), 200)
    else:
        response = make_response(json.dumps('Erro alterando usuário'), 500)
    response.headers['Content-Type'] = 'application/json'
    return response

# Delete
@app.route('/usuario/deletar')
@login_required
def delete_user():
    return "<p>To be user {} delete page</p>".format(current_user.get_id())

# Add address
@app.route('/usuario/enderecos/adicionar', methods=['POST'])
@login_required
def add_address():
    form = AddressForm()
    if form.validate_on_submit():
        data = {}
        for field in form.data.keys():
            if field in ['street_address_1', 'street_address_2', 'city',
                    'state', 'neighbourhood']:
                data[field] = form.data[field].lower()
            else:
                data[field] = form.data[field]
        data['_id'] = ObjectId()
        User.update_by_id(current_user.id, push_data={'addresses':data})
        response = make_response(json.dumps('Endereço adicionado'),200)
    else:
        response = make_response(json.dumps(form.errors), 500)
    response.headers['Content-Type'] = 'application/json'
    return response

# Delete address
@app.route('/usuario/enderecos/deletar', methods=['POST'])
@login_required
def delete_address():
    address_id = request.json['address_id']
    res = User.update_by_id(current_user.id, pull_data=
        {'addresses': {'_id': ObjectId(address_id)}})
    if res.modified_count > 0:
        response = make_response(json.dumps('Endereço removido'), 200)
    else:
        response = make_response(
            json.dumps('Erro ao tentar remover endereço'), 500)
    response.headers['Content-Type'] = 'application/json'
    return response

##################
# end User       #
##################

##################
# Category       #
##################

# Create
# only the admin can create new categories

# Read
@app.route('/catalogo')
@app.route('/catalogo/<string:permalink>')
@back.anchor
def category(permalink=None):
    categories = Category.get_all(to_obj=True)
    if permalink is not None:
        category = [c for c in categories if c.permalink == permalink][0]
        categories.remove(category)
        products = Summary.get_by_category(category.id)
    else:
        category = None
        products = Summary.get_all()
    return render_template(
            'category.html',
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
# Wishlist       #
##################

def get_wishlist():
    if current_user.is_anonymous:
        return []
    else:
        wishlist = []
        for item in current_user.wishlist:
            product = Summary.get_summary_by_variant(item['_id'])
            product['_id'] = str(product['_id'])
            for var in product['variants']:
                var['_id'] = str(var['_id'])
            wishlist.append(product)
        return wishlist

@app.route('/usuario/wishlist')
@login_required
def wishlist():
    response = make_response(json.dumps(get_wishlist()), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/usuario/wishlist/adicionar', methods=['POST'])
@login_required
def add_to_wishlist():
    if current_user.is_anonymous:
        response = make_response(
            json.dumps('{}{}'.format(
                'Você precisa estar logado para',
                'adicionar produtos na sua lista de desejos')),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response
    variant_id = request.json['variant_id']
    result = User._get_one(False,query={'_id': current_user.id, 'wishlist._id': variant_id})
    if result is None:
        result = User.update_by_id(current_user.id,
            push_data={'wishlist': {'_id':variant_id}})
        response = make_response(
            json.dumps('Produto adicionado à lista de desejos'), 200)
    else:
        response = make_response(
            json.dumps('Produto já está na sua lista de desejos'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/usuario/wishlist/remover', methods=['POST'])
@login_required
def remove_from_wishlist():
    res = User.update_by_id(current_user.id,
            pull_data={'wishlist': {'_id': request.json['id'] }})
    if res.modified_count > 0:
        response = make_response(
            json.dumps('Produto removido da sua lista'), 200)
    else:
        response = make_response(json.dumps('Erro ao remover produto'), 500)
    response.headers['Content-Type'] = 'application/json'
    return response

##################
# end Wishlist   #
##################

##################
# Cart/Orders    #
##################

def get_cart():
    if current_user.is_anonymous:
        cart = session.get('cart', [])
    else:
        cart = current_user.cart
        print(cart)
    return [CartLine(item)() for item in cart]

@app.route('/usuario/compras')
def cart():
    response = make_response(json.dumps(get_cart()), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/usuario/carrinho/adicionar', methods=['POST'])
def add_to_cart():
    variant_id = request.json['variant_id']
    qty = 1
    res = Variant.update_by_id_and_qty(variant_id, qty,
        inc_data = {
            'quantity': -qty,
            'reserved': qty })
    if res.modified_count == 0:
        response = make_response(
            json.dumps('Produto indisponível no estoque'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    cart_line = { '_id': variant_id, 'quantity': qty }
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
            result = User.update_by_id(current_user.id, push_data={'cart': cart_line})
    response = make_response(
        json.dumps('Produto adicionado às suas compras'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/usuario/carrinho/editar', methods=['POST'])
def edit_cart():
    qty = int(request.json['quantity'])
    if qty < 0:
        response = make_response(
            json.dumps(
                'Não é possível alterar a quantidade para um número negativo'),
            500)
        response.headers['Content-Type'] = 'application/json'
    else:
    #elif qty == 0:
        variant_id = request.json['id']
        cart_item = User.get_cart_item(current_user.id, request.json['id'])
        qty_in_cart = cart_item['cart'][0]['quantity']
        if qty == 0:
            # remove item from cart
            res = User.update_by_id(current_user.id,
                    pull_data={'cart': {'_id': request.json['id'] }})
            # check if the cart has in fact been updated
            if res.modified_count > 0:
                Variant.update_by_id(variant_id, inc_data = {
                    'quantity': qty_in_cart,
                    'reserved': -qty_in_cart
                })
                response = make_response(
                    json.dumps('Produto removido do seu carrinho'), 200)
            else:
                response = make_response(
                    json.dumps('Erro ao remover produto do carrinho'), 500)
        else:
            inc_qty = qty - qty_in_cart
            res = Variant.update_by_id_and_qty(variant_id, inc_qty,
                inc_data = {
                    'quantity': -inc_qty,
                    'reserved': inc_qty })
            if res.modified_count == 0:
                response = make_response(
                    json.dumps('Quantidade indisponível no estoque'), 500)
            else:
                # decrement/increment
                res = User._update_one(
                    {'_id': current_user.id, 'cart._id': request.json['id'] },
                    inc_data={'cart.$.quantity': inc_qty })
                if res.modified_count > 0:
                    response = make_response(
                        json.dumps('Quantidade do produto alterada'), 200)
                else:
                    response = make_response(
                        json.dumps('Erro ao remover produto do carrinho'), 500)
    response.headers['Content-Type'] = 'application/json'
    return response


######################
# end Cart/Orders    #
######################

###############
# Checkout    #
###############

@app.route('/checkout')
@back.anchor
def checkout():
    if current_user.is_anonymous:
        form = LoginForm()
        return render_template(
                'checkoutlogin.html',
                categories=Category.get_all(),
                login_form=form)
    else:
        form = AddressForm()
        #return choose address page
        return render_template('checkout.html',
                form=form,
                card_form=CreditCardForm(),
                categories=Category.get_all())

@app.route('/confirmarcompra', methods=['POST'])
def confirm():
    card = request.json['card']
    cart = request.json['cart']
    # https://github.com/mundipagg/mundipagg-one-python/wiki/Create-a-Transaction
    creditcard_data = creditcard(
        creditcard_number = card['number'],
        creditcard_brand = card['brand'],
        security_code = card['securityCode'],
        holder_name = card['holderName'],
        exp_month = int(card['expMonth']),
        exp_year = card['expYear'])
    total_cart = 0
    for item in cart:
        total_cart += (item['price']*item['quantity'])
    total_cart *= 100

    transaction_collection = [creditcard_transaction(total_cart,creditcard_data)]
    order_id = uuid.uuid4()
    options_request = order(order_reference=order_id)
    sale_request = create_sale_request(
        creditcard_transaction_collection=transaction_collection,
        order=options_request)

    service_client = GatewayServiceClient(
        app.config.get('MUNDIPAGG_KEY'),
        PlatformEnvironment.sandbox,
        HttpContentTypeEnum.json,
        app.config['MUNDIPAGG_ENDPOINT'])

    http_response = service_client.sale.create_with_request(sale_request)
    json_response = http_response.json()
    if json_response['CreditCardTransactionResultCollection'][0]['Success']:
        ns_order = Order.from_form(json_response, cart)
        ns_order.insert()
        User.clean_cart(current_user.id)
        response = make_response(json.dumps('Compra realizada com sucesso!'), 200)
    else:
        response = make_response(json.dumps(''.join([
            'Tivemos um problema com a sua compra. ',
            'Se tiver sido a primeira vez que isso aconteceu, por favor ',
            'tente novamente. Caso contrário, entre em contato conosco'])),
            500)

    response.headers['Content-Type'] = 'application/json'
    return response

###################
# end checkout    #
###################

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

