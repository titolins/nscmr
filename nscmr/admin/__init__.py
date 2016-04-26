from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    abort,
    url_for,
    current_app)

from pymongo.errors import DuplicateKeyError

from flask.ext.principal import RoleNeed, Permission

from .models import User, Category, Product, Variant

from .forms import (
    NewCategoryForm,
    category_images,
    NewProductForm,
    product_images)

from .helper import make_thumb

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

    # Users
    ## Create
    @bp.route('/usuarios/novo')
    def create_user():
        return "<h1>To be new user</h1>"

    ## Read/Update/Delete
    @bp.route('/usuarios')
    def users():
        return render_template('admin/users.html', users=User.get_all())

    # Categories
    ## Create
    @bp.route('/categorias/nova')
    def create_category():
        return "<h1>To be new category page</h1>"

    ## Read/Update/Delete
    @bp.route('/categorias', methods=['GET', 'POST'])
    def categories():
        categories = Category.get_all(to_obj=True)
        form = NewCategoryForm()
        # Filling the selectfield choices, first we add the none choice
        form.parent.choices = [('None','Nenhuma')]
        # then we fill it with all available categories
        for c in categories:
            form.parent.choices.append((str(c.id), c.name))
        if form.validate_on_submit():
            img_filename = category_images.save(form.base_img.data,
                    name="{}.".format(form.name.data))
            form.base_img.data = category_images.url(img_filename)
            category = Category.from_form(form.data)
            try:
                category.insert()
                #flash("Categoria criada!")
            except DuplicateKeyError:
                form.name.errors.append(
                    'Já existe uma categoria com esse nome')
        return render_template('admin/categories.html',
                form=form,
                categories=categories)

    # Produtos
    ## Create
    @bp.route('/produtos/novo')
    def create_product():
        return "<h1>To be new product page</h1>"

    ## Read/Update/Delete
    @bp.route('/produtos', methods=['GET', 'POST'])
    def products():
        categories = Category.get_all(to_obj=True)
        products = Product.get_all(to_obj=True)
        form = NewProductForm()
        form.category.choices = [('_'.join([str(c.id), c.name]), c.name) \
            for c in categories]
        if form.validate_on_submit():
            # first we build the product data to create the product itself
            c_info = form.category.data.split('_')
            category = {
                '_id': c_info[0],
                'name': c_info[1],
            }
            product_data = {
                'category': category,
                'name': form.name.data,
                'description': form.description.data,
                'meta_description': form.meta_description.data,
            }
            # create and insert product, catching duplicate name errors
            product = Product.from_form(product_data)
            try:
                product.insert()
            except DuplicateKeyError:
                form.name.errors.append(
                    'Já existe um produto com esse nome')
            # then we check for the has_variants data. If it's false, we'll
            # create a single variant with all additional product info (sku,
            # price, images, etc..)
            if not form.has_variants.data:
                # get the id of the just inserted product and create and
                # insert the variant
                var_data = create_variant_data(form.data, product)
                #var_data['product'] = product.id
                variant = Variant.from_form(var_data)
                variant.insert()
            # If, however, the product has several variants, we'll need to
            # iterate them and create all of them.
            else:
                for var in form.variants:
                    var_data = create_variant_data(var.data, product,
                        is_var=True)
                    variant = Variant.from_form(var_data)
                    variant.insert()
            # import flash
            #flash("Produto criado!")
            products = Product.get_all(to_obj=True)
        return render_template('admin/products.html',
                products=products,
                form=form)


    ######################################
    # end CRUD                           #
    ######################################

    ######################################
    # start helpers                      #
    ######################################


    def create_variant_data(form_data, product, is_var=False):
        images = []
        # save the image, create the thumbnail and build the array of
        # the images
        for img in form_data['images']:
            if img.filename not in ('', None):
                # if it's a variant, we use the variant attributes to generate
                # the filename
                if is_var:
                    img_filename = "{}-{}.".format(product.permalink,
                        '_'.join([
                            form_data['attr_1_value'],
                            form_data['attr_2_value']]))
                # else, we just use the permalink
                else:
                    img_filename = "{}.".format(product.permalink)

                # save the regular image
                img_filename = product_images.save(img, name=img_filename)
                # get it's url
                img = product_images.url(img_filename)
                # create the thumbnail and get it's url
                thumb = product_images.url(make_thumb(img_filename,
                            product_images.default_dest(current_app)))
                # create this image dict and append to the whole
                img_dict = {'big': img, 'thumb': thumb}
                images.append(img_dict)
        # construct the price (stopped using floats as per several
        # recommendations, besides pymongo encoding error to decimal
        price = {
            'currency': 'BRL',
            'major': int(form_data['price']),
            'minor': int((form_data['price']*100)%100)
        }
        # build the product and variant data
        var_data = {
            'product_id': product.id,
            'images': images,
            'sku': form_data['sku'],
            'price': price,
            'quantity': form_data['quantity'],
        }
        # if we have multiple variants, we need to get the attributes from the
        # form..
        if is_var:
            attrs = {
                form_data['attr_1_name']: form_data['attr_1_value'],
                form_data['attr_2_name']: form_data['attr_2_value'],
            }
            var_data['attributes'] = attrs

        return var_data


    ######################################
    # end helpers                        #
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

    return bp
