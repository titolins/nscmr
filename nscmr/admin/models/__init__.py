from datetime import datetime
from bson.objectid import ObjectId

from werkzeug.security import check_password_hash, generate_password_hash

from nscmr.admin.models.document import Document

from nscmr.admin.helper.validators import min_length


class User(Document):
    '''User class
    '''
    __collection__ = 'users'
    fields = ['name','dob','roles','addresses','wishlist','orders','cart']
    defaults = {
        'roles': ['user'],
        'addresses': [],
        'wishlist': [],
        'orders': [],
        'cart': []
    }
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

        # init object and set default values
        user = User(form_data)
        user.set_defaults()
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


class Category(Document):

    __collection__ = 'categories'

    fields = ['name', 'parent', 'ancestors', 'thumbnail', 'header']

    indexes = {
        'name': { 'unique': True },
    }

    @staticmethod
    def from_form(form_data):
        return NotImplemented


class Product(Document):
    __collection__ = 'products'
    fields = ['name', 'description', 'price', 'size', 'thumbnail',
            'background', 'category']

    @classmethod
    def get_by_category(cls, category_id, to_obj=False):
        return cls._get_many(to_obj, { "category._id": category_id })

    @staticmethod
    def from_form(form_data):
        return NotImplemented

    def get_category(self):
        return Category(self._content.get('category'))

