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
            return redirect(url_for('admin.showPanel'))
        return
    if request.endpoint != 'admin.login':
        return redirect(url_for('admin.login'))


@bp.route('/')
def login():
    return render_template('admin/login.html')

@bp.route('/panel')
def showPanel():
    return render_template('admin/index.html')

@bp.route('/<int:user_id>/profile')
def profile(user_id):
    return "<h1>To be admin profile page</h1>"

