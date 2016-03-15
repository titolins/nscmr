from flask import Blueprint
from flask import render_template, redirect, request, abort, url_for
from flask import session as login_session

bp = Blueprint(
        'admin',
        __name__,
        template_folder='templates',
        static_folder='static',
        )

@bp.before_request
def admin_required():
    ''' Function to restrict access to admin area.
    '''
    if 'username' in login_session:
        if login_session['user_access_level'] != 1 and \
                request.endpoint != 'admin.login':
            return abort(403)
        elif login_session['user_access_level'] == 1 and \
                request.endpoint == 'admin.login':
            return redirect(url_for('admin.index'))
        return
    if request.endpoint != 'admin.login':
        return redirect(url_for('admin.login'))


@bp.route('/')
def login():
    return render_template('admin/login.html')

@bp.route('/painel')
def index():
    return render_template('admin/index.html')

@bp.route('/painel/categorias')
def categories():
    return "To be categories panel"

@bp.route('/<int:user_id>/profile')
def profile(user_id):
    return "<h1>To be admin profile page</h1>"



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
