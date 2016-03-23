from datetime import datetime
from bson.objectid import ObjectId

from werkzeug.security import check_password_hash, generate_password_hash

from nscmr.admin.models.document import Document
from nscmr import login_manager

from nscmr.admin.helper.validators import min_length


@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)


class User(Document):
    '''User class

    :content - form data received as dictionary
    '''
    __collection__ = 'users'
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
        # used as timestamp substitute for datatime.now() and use a tz
        date = datetime.utcnow()

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
        user = User(form_data)
        return user

    @property
    def dob(self):
        if self.content['dob'] is not None:
            return "{:%d/%m/%Y}".format(self.content['dob'])
        return None

    @property
    def name(self):
        return self.content['name']

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.content['_id'])

    def save(self):
        # validate is working, but for now it may be better to disable it
        # (mainly because of the password validation -- it must only be
        # validated on creation or password update...)
        # besides that, we are already using wtforms for validation, so it
        # seems like a bit too much for now...
        #self.validate()
        self.collection.insert_one(self.content)

    def check_password(self, password):
        return check_password_hash(self.content['password'], password)

    def __eq__(self, other):
        '''
        Compares two user objects by their id's
        '''
        if isinstance(other, User):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        '''
        Inequality comparator
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

    def __repr__(self):
        return str(self.content)
