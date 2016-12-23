from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    abort,
    url_for,
    current_app,
    session,
    make_response)

from bson.objectid import ObjectId

import os
from datetime import datetime

import httplib2
from apiclient import discovery
from oauth2client import client, crypt, tools
from oauth2client.file import Storage

from pymongo.errors import DuplicateKeyError

from flask.ext.principal import RoleNeed, Permission

from werkzeug.security import generate_password_hash

from .models import User, Category, Product, Variant, Summary, Image

from .helper import slugify

from .forms import (
    NewCategoryForm,
    category_images,
    NewProductForm,
    NewUserForm,
    ImportSheetForm,
    ImageUploadForm)

from .helper import make_thumb

import json

SHEETS_SCOPE = "https://www.googleapis.com/auth/spreadsheets.readonly"

def build_admin_bp():
    bp = Blueprint(
            'admin',
            __name__,
            template_folder='templates',
            static_folder='static',
            )

    admin = Permission(RoleNeed('admin'))

    @bp.before_request
    @admin.require()
    def admin_required():
        pass

    # removed admin login, considering that before_request decorator is really
    # simple to use and eliminates the need for it
    #@bp.route('/')
    #def login():
    #    return render_template('admin/login.html')

    @bp.route('/')
    @bp.route('/painel')
    def index():
        return render_template('admin/index.html')

    @bp.route('/profile')
    def profile():
        return "<h1>To be admin profile page</h1>"


    ######################################
    # CRUD                               #
    ######################################


    ## Create/Read
    @bp.route('/usuarios/gerenciar', methods=['GET', 'POST'])
    def users():
        form = NewUserForm()
        users = User.get_all(to_obj=True)
        if form.validate_on_submit():
            user = User.from_form(form.data)
            try:
                user.insert()
                #flash('Usuário criado com sucesso!')
            except DuplicateKeyError:
                form.email.errors.append(
                    'Já existe um usuário cadastrado com esse email')
            users = User.get_all(to_obj=True)
        return render_template('admin/users.html',
            users=users,
            form=form)

    # Update
    @bp.route('/usuarios/editar', methods=['POST'])
    def edit_users():
        users = json.loads(request.form.get('users'))
        us_modified = 0
        for item in users:
            item_id = item['id']
            data = {}
            for k in item.keys():
                if item[k] not in ('', None):
                    field_data = item[k]
                    if k == 'id':
                        continue
                    elif k in ('name', 'email'):
                        field_data = item[k].lower()
                    elif k == 'dob':
                        field_data = datetime.strptime(item[k], '%Y-%m-%d')
                    elif k == 'password':
                        field_data = generate_password_hash(item[k])
                    data[k] = field_data
            result = User.update_by_id(item_id, data)
            us_modified += result.modified_count
        text = '{} usuário(s) modificado(s)!'.format(us_modified)
        response_json = { 'text': text, 'redirect': url_for('admin.users') }
        response = make_response(json.dumps(response_json), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Delete
    @bp.route('/usuarios/deletar', methods=['POST'])
    def delete_users():
        us_deleted = 0
        for k in request.json['users']:
            if k not in ('', None):
                us_deleted += User.delete_by_id(k).deleted_count
        if us_deleted == 0:
            response = make_response(
                json.dumps('Não foi possível localizar nenhum usuário'), 404)
            response.headers['Content-Type'] = 'application/json'
            return response

        text = '{} usuário(s) deletado(s)'.format(us_deleted)
        response_json = {'text': text, 'redirect':url_for('admin.users')}
        response = make_response(json.dumps(response_json), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    ## Create/Read
    @bp.route('/categorias/gerenciar', methods=['GET', 'POST'])
    def categories():
        categories = Category.get_all(to_obj=True)
        form = NewCategoryForm()
        # Filling the selectfield choices, first we add the none choice
        form.parent.choices = [('None_Nenhuma','Nenhuma')]
        # then we fill it with all available categories
        for c in categories:
            form.parent.choices.append(('_'.join([str(c.id), c.name]), c.name))
        if form.validate_on_submit():
            category = Category.from_form(form.data)
            try:
                category.insert()
                #flash("Categoria criada!")
            except DuplicateKeyError:
                form.name.errors.append(
                    'Já existe uma categoria com esse nome')
            categories = Category.get_all(to_obj=True)
        return render_template('admin/categories.html',
                form=form,
                categories=categories)

    @bp.route('/categorias/deletar', methods=['POST'])
    def delete_categories():
        # implement img deletion!!!!!!
        cs_deleted = ps_deleted = vs_deleted = 0
        for k in request.json['categories']:
            if k not in ('', None):
                products = Product.get_by_category(k)
                for p in products:
                    vs_deleted += Variant.delete_by_product(p['_id']).deleted_count
                ps_deleted += Product.delete_by_category(k).deleted_count
                cs_deleted += Category.delete_by_id(k).deleted_count
        if cs_deleted == 0:
            response = make_response(
                json.dumps('Não foi possível localizar nenhuma categoria'), 404)
            response.headers['Content-Type'] = 'application/json'
            return response

        text = '{} categoria(s), {} produto(s) e {} variante(s) deletado(s)'.\
            format(cs_deleted, ps_deleted, vs_deleted)
        response_json = {'text': text, 'redirect':url_for('admin.categories')}
        response = make_response(json.dumps(response_json), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Update
    @bp.route('/categorias/editar', methods=['POST'])
    def edit_categories():
        categories = json.loads(request.form.get('categories'))
        cs_modified = 0
        for item in categories:
            item_id = item['id']
            data = {}
            unset = {}
            for k in item.keys():
                if item[k] not in ('', None):
                    if k == 'id':
                        continue
                    elif k == 'parent':
                        parent_info = item[k].split('_')
                        if parent_info[0] == 'None':
                            unset[k] = ""
                        else:
                            data['parent._id'] = parent_info[0]
                            data['parent.name'] = parent_info[1]
                        continue
                    elif k == 'name':
                        data[k] = item[k].lower()
                        data['permalink'] = slugify(data[k])
                        continue
                    elif k == 'base_img':
                        try:
                            img_name = item['name']
                        except:
                            img_name = item[k]
                        img = request.files.get(item_id)
                        img_filename = category_images.save(
                                img, name="{}.".format(img_name.lower()))
                        data[k] = category_images.url(img_filename)
                        continue
                    data[k] = item[k]
            result = Category.update_by_id(item_id, data, unset)
            # if we have edited the category name (and thus permalink as well),
            # we need to update such info in this categories' products and
            # respective summary
            if 'name' in data.keys():
                p_data = {
                    'category.name': data['name'],
                    'category.permalink': data['permalink'],
                }
                Product.update_by_category(item_id, p_data)
                Summary.update_by_category(item_id, p_data)

            cs_modified += result.modified_count
        text = '{} categoria(s) modificada(s)!'.format(cs_modified)
        response_json = { 'text': text, 'redirect': url_for('admin.categories') }
        response = make_response(json.dumps(response_json), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    ## Create/Read
    @bp.route('/produtos/gerenciar', methods=['GET', 'POST'])
    def products():
        categories = Category.get_all(to_obj=True)
        import_form = ImportSheetForm()
        form = NewProductForm()
        form.category.choices = [
            ('_'.join([str(c.id), c.permalink, c.name]),
            c.name) for c in categories ]
        # need to do this so we don't get a can't encode exception on
        # validation (and to avoid yet another custom validation..)
        if form.shipping.weight.data not in (None, ''):
            form.shipping.weight.data = float(form.shipping.weight.data)
        if form.validate_on_submit():
            product, product_summary = Product.from_form(form.data)
            try:
                product.insert()
                product_summary._content['_id'] = product._content['_id']
                product_summary.insert()
            except DuplicateKeyError:
                form.name.errors.append(
                    'Já existe um produto com esse nome')
            # then we check for the has_variants data. If it's false, we'll
            # create a single variant with all additional product info (sku,
            # price, images, etc..)
            if not form.has_variants.data:
                print(form.data)
                variant, var_summary = Variant.from_form(form.data, product)
                variant.insert()
                var_summary['_id'] = variant.id
                Summary.update_by_id(product.id, push_data=\
                    { 'variants': var_summary })
            # If, however, the product has several variants, we'll need to
            # iterate them and create all of them.
            else:
                attributes = {}
                for var in form.variants:
                    variant, var_summary = Variant.from_form(var.data, product)
                    variant.insert()
                    var_summary['_id'] = variant.id
                    Summary.update_by_id(product.id, push_data=\
                        { 'variants': var_summary })
                    for k in variant.attributes.keys():
                        if k not in attributes.keys():
                            attributes[k] = []
                        if variant.attributes[k] not in attributes[k]:
                            attr = '_'.join([
                                str(variant.id),
                                variant.attributes[k]
                            ])
                            attributes[k].append(attr)
                # update product with all of it's available variations
                Product.collection.update_one(
                    {'_id': product.id },
                    {'$set':
                        {'attributes': attributes }
                    })

            # import flash
            #flash("Produto criado!")
        return render_template('admin/products.html',
                form=form,
                import_form=import_form)


    #Read
    @bp.route('/produtos/json', methods=['GET'])
    def get_products():
        products = Product.get_all(to_obj=True)
        data = []
        if len(products) > 0:
            for p in products:
                data.append(p.as_dict())
        result = { 'data': data }
        response = make_response(json.dumps(result), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    @bp.route('/produtos/imagem', methods=['DELETE'])
    def remove_images():
        for img in request.json['imgs']:
            Variant.remove_image(request.json['variant_id'], img)

        response = make_response("", 200)
        response.headers['Content-Type'] = 'application/json;utf-8'
        return response

    @bp.route('/produtos/imagem', methods=['PUT'])
    def add_images():
        for img in request.json['imgs']:
            Variant.add_image(request.json['variant_id'], img)

        response = make_response("", 200)
        return response

    @bp.route('/produtos/imagem/<string:var_id>', methods=['GET'])
    def get_variant_images(var_id):
        imgs = []
        var = Variant.get_by_id(var_id, to_obj=True).as_dict()
        if 'images' in var.keys() and var['images'] is not None:
            for img in var['images']:
                imgs.append(Image.get_by_id(img, to_obj=True).as_dict())
        print(imgs)
        response = make_response(json.dumps(imgs), 200)
        response.headers['Content-Type'] = 'application/json;utf-8'
        return response

    #Delete
    @bp.route('/produtos/deletar', methods=['POST'])
    def delete_products():
        # implement img deletion!!!!!!
        vs_deleted = ps_deleted = 0
        for field in ['variants', 'products']:
            for k in request.json[field]:
                if k not in ('', None):
                    if field == 'variants':
                        p = Variant.get_by_id(k, to_obj=True).product
                        if str(p.id) not in request.json['products']:
                            vs_deleted += Variant.delete_by_id(k).deleted_count
                            p_attrs = Product.get_by_id(p.id,
                                    to_obj=True).attributes
                            for attr in p_attrs:
                                for value in p_attrs[attr]:
                                    if k in value:
                                        p_attrs[attr].remove(value)
                            Product.update_by_id(p.id, set_data = {
                                'attributes': p_attrs
                            })
                            Summary.update_by_id(p.id, pull_data=\
                                { 'variants': { '_id': ObjectId(k) }})
                            User.remove_from_carts(k)
                            User.remove_from_wishlists(k)
                            if len(p.variants) == 0:
                                ps_deleted += Product.delete_by_id(p.id).\
                                    deleted_count
                                Summary.delete_by_id(p.id)
                    elif field == 'products':
                        variants = Variant.get_by_product(k)
                        for variant in variants:
                            User.remove_from_carts(str(variant.id))
                            User.remove_from_wishlists(str(variant.id))
                        vs_res = Variant.delete_by_product(k)
                        p_res = Product.delete_by_id(k)
                        Summary.delete_by_id(k)
                        vs_deleted += vs_res.deleted_count
                        ps_deleted += p_res.deleted_count
        if ps_deleted + vs_deleted == 0:
            response = make_response(
                json.dumps('Não foi possível localizar nenhum produto'), 404)
            response.headers['Content-Type'] = 'application/json'
            return response

        text = '{} produto(s) e {} variante(s) deletado(s)!'.format(
            ps_deleted, vs_deleted)
        response_json = { 'text': text, 'redirect': url_for('admin.products') }
        response = make_response(json.dumps(response_json), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Edit
    @bp.route('/produtos/editar', methods=['POST'])
    def edit_products():
        ps_modified = vs_modified = 0
        json_data = json.loads(request.form.get('data'))
        for field in ('variants', 'products'):
            for item in json_data[field]:
                item_id = item['id']
                data = {}
                s_data = {}
                for k in item.keys():
                    if item[k] not in ('', None):
                        if k == 'id':
                            continue
                        elif k == 'category':
                            category_fields = item[k].split('_')
                            s_data['category._id'] = data['category._id'] = category_fields[0]
                            s_data['category.name'] = data['category.name'] = category_fields[2]
                            s_data['category.permalink'] = data['category.permalink'] = category_fields[1]
                        elif k == 'price':
                            s_data['variants.$.price'] = data[k] = int(float(item[k])*100)
                        elif k == 'name':
                            s_data[k] = data[k] = item[k].lower()
                            s_data['permalink'] = data['permalink'] = slugify(data['name'])
                        elif k == 'quantity':
                            data[k] = int(item[k])
                        elif k == 'description':
                            data[k] = s_data[k] = item[k]
                        else:
                            data[k] = item[k]
                if field == 'variants':
                    result = Variant.update_by_id(item_id, data)
                    Summary._update_one(
                        {'variants._id': ObjectId(item_id)},
                        set_data=s_data)
                    vs_modified += result.modified_count
                    continue
                result = Product.update_by_id(item_id, data)
                Summary.update_by_id(item_id, s_data)
                ps_modified += result.modified_count
                # remove data unused in summary and update summary

        text = '{} produto(s) e {} variante(s) modificado(s)!'.format(
            ps_modified, vs_modified)
        response_json = { 'text': text, 'redirect': url_for('admin.products') }
        response = make_response(json.dumps(response_json), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    ## Create/Read
    @bp.route('/imagens/gerenciar', methods=['GET', 'POST'])
    def images():
        imgs = Image.get_all()
        form = ImageUploadForm()
        if form.validate_on_submit():
            images = Image.from_form(request.files.getlist('images'))
            try:
                for img in images:
                    img.insert()
                    #product_summary._content['_id'] = product._content['_id']
                    #product_summary.insert()
            except:
                form.images.errors.append(
                    'Erro ao fazer upload de imagem. Por favor, tente de novo')
            #flash("Produto criado!")
        return render_template('admin/images.html',
                form=form,
                imgs=imgs)

    #Read
    @bp.route('/imagens/json', methods=['GET'])
    def get_images():
        imgs = Image.get_all(to_obj=True)
        data = []
        if len(imgs) > 0:
            for img in imgs:
                data.append(img.as_dict())
        response = make_response(json.dumps(data), 200)
        response.headers['Content-Type'] = 'application/json'
        return response



    ######################################
    # end CRUD                           #
    ######################################


    ######################################
    # template default pages             #
    ######################################

    @bp.route('/painel/components/chartjs')
    def chartjs():
        return render_template('admin/components/chartjs.html')

    @bp.route('/painel/components/pricing-table')
    def pricing_table():
        return render_template('admin/components/pricing-table.html')

    @bp.route('/painel/form/ui-kits')
    def ui_kits():
        return render_template('admin/form/ui-kits.html')

    @bp.route('/painel/table/datatable')
    def data_table():
        return render_template('admin/table/datatable.html')

    @bp.route('/painel/table/table')
    def table():
        return render_template('admin/table/table.html')

    @bp.route('/painel/ui-kits/alert')
    def alert():
        return render_template('admin/ui-kits/alert.html')

    @bp.route('/painel/ui-kits/button')
    def button():
        return render_template('admin/ui-kits/button.html')

    @bp.route('/painel/ui-kits/card')
    def card():
        return render_template('admin/ui-kits/card.html')

    @bp.route('/painel/ui-kits/grid')
    def grid():
        return render_template('admin/ui-kits/grid.html')

    @bp.route('/painel/ui-kits/list')
    def list():
        return render_template('admin/ui-kits/list.html')

    @bp.route('/painel/ui-kits/loader')
    def loader():
        return render_template('admin/ui-kits/loader.html')

    @bp.route('/painel/ui-kits/modal')
    def modal():
        return render_template('admin/ui-kits/modal.html')

    @bp.route('/painel/ui-kits/other')
    def other():
        return render_template('admin/ui-kits/other.html')

    @bp.route('/painel/ui-kits/panel')
    def panel():
        return render_template('admin/ui-kits/panel.html')

    @bp.route('/painel/ui-kits/step')
    def step():
        return render_template('admin/ui-kits/step.html')

    @bp.route('/painel/ui-kits/theming')
    def theming():
        return render_template('admin/ui-kits/theming.html')

    @bp.route('/painel/icons/font-awesome')
    def font_awesome():
        return render_template('admin/icons/font-awesome.html')

    @bp.route('/painel/icons/glyphicons')
    def glyphicons():
        return render_template('admin/icons/glyphicons.html')

    @bp.route('/painel/license')
    def license():
        return render_template('admin/license.html')


    ## import sheet from google sheets
    @bp.route('/importar', methods=['POST', 'GET'])
    def import_sheet():
        form = ImportSheetForm()
        flow = client.flow_from_clientsecrets(
                os.path.join(current_app.instance_path,
                                'sheets_api_secret.json'),
                scope=SHEETS_SCOPE,
                redirect_uri=url_for('admin.import_sheet', _external=True))
        flow.user_agent = 'Sheets API'
        if form.validate_on_submit():
            session['sheet_data'] = form.data
            auth_uri = flow.step1_get_authorize_url()
            return redirect(auth_uri)
        else:
            auth_code = request.args['code']
            credentials = flow.step2_exchange(auth_code)
            http = credentials.authorize(httplib2.Http())
            discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
            service = discovery.build('sheets', 'v4', http=http,
                                      discoveryServiceUrl=discoveryUrl)

            result = service.spreadsheets().values().get(
                    spreadsheetId=session['sheet_data']['sheet_id'],
                    range=session['sheet_data']['sheet_name']).execute()
            values = result.get('values', [])
            category = ''
            for v in values:
                if v[1] in ('TOTAL EM ESTOQUE', 'CATEGORIA'):
                    continue
                elif v[1] != '':
                    category = Category.get_by_name(v[1].lower(), to_obj=True)
                    if not category:
                        category = Category.from_form({
                            'name': v[1].lower()
                        })
                        category.insert()
                shipping_info = v[4].split('x')
                if len(shipping_info) != 3:
                    shipping_info = [0,0,0]
                shipping_info.append(float(v[5]) if v[5] != '' else 0)
                form_data = {
                    'has_variants': False,
                    'name':         v[2].lower(),
                    'sku':          v[3].lower(),
                    'category':     '_'.join([
                        str(category.id), category.permalink, category.name]),
                    'shipping': {
                        'width': int(shipping_info[0]),
                        'height': int(shipping_info[1]),
                        'length': int(shipping_info[2]),
                        'weight': shipping_info[3]
                    },
                    'quantity': int(v[6]),
                    'description': v[7],
                    'price': float('.'.join(v[8].split(' ')[1].split(',')))

                }
                product, summary = Product.from_form(form_data)
                product.insert()
                summary._content['_id'] = product._content['_id']
                summary.insert()
                variant, var_summary = Variant.from_form(form_data, product)
                variant.insert()
                var_summary['_id'] = variant.id
                Summary.update_by_id(product.id, push_data=\
                        {'variants': var_summary})
            del(session['sheet_data'])

        return redirect(url_for('admin.products'))

    return bp
