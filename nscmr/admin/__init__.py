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

from .models import User, Category, Product

from .forms import (
    NewCategoryForm,
    category_images,
    NewProductForm,
    product_images)


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
        products = Product.get_all()
        form = NewProductForm()
        form.category.choices = [(str(c.id), c.name) for c in categories]
        if form.validate_on_submit():
            print(form.data)
            pass
        return render_template('admin/products.html',
                products=products,
                form=form)

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

    return bp
