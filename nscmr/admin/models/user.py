from datetime import datetime
from bson.objectid import ObjectId

from werkzeug.security import check_password_hash, generate_password_hash

from nscmr.admin.models.document import Document
from nscmr import login_manager

from nscmr.admin.helper.validators import min_length


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


class User(Document):
    '''User class
    '''
    __collection__ = 'users'
    fields = ['name', 'dob']
    # required fields
    required_fields = ['name', 'password']
    PASS_LEN = 8
    # field validators - dict containing ==> field: [validator, error_msg]
    validators = {
        'password': [
            min_length(PASS_LEN),
            "Campo 'password' deve conter ao menos {} caracteres".\
                    format(PASS_LEN)]
    }

    @staticmethod
    def from_form(form_data):
        # used as timestamp. substitute for datatime.now() and use a tz
        form_data['created_at'] = form_data['updated_at'] = datetime.utcnow()

        # use email as _id and delete email so we don't get repeated fields
        form_data['_id'] = form_data['email']
        del(form_data['email'])

        # converts date object to datetime, as pymongo only support the latter
        if form_data['dob'] is not None:
            form_data['dob'] = form_data(
                form_data['dob'], datetime.min.time())

        # hash password
        form_data['password'] = generate_password_hash(
            form_data['password'])
        # delete confirm field
        del(form_data['confirm'])

        user = User(form_data)
        return user

    def get_dob(self):
        if 'dob' in self._content and self._content['dob'] is not None:
            return "{:%d/%m/%Y}".format(self._content['dob'])
        return None

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def check_password(self, password):
        return check_password_hash(self._content['password'], password)


