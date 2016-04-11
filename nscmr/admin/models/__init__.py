from datetime import datetime
from bson.objectid import ObjectId
from pymongo import ASCENDING

from werkzeug.security import check_password_hash, generate_password_hash

from nscmr.admin.models.document import Document, SlugDocument

from nscmr.admin.helper import slugify


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

    @staticmethod
    def from_form(form_data):
        # use email as _id and delete email so we don't get repeated fields
        form_data['_id'] = form_data['email'].lower()
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


class Category(SlugDocument):

    __collection__ = 'categories'

    fields = ['name', 'parent', 'ancestors', 'base_img', 'permalink',
    'meta_description']

    # supports both dicts to pass constraint indexes such as unique, and simple
    # values to pass single field indexes (compound indexes do not work yet)
    indexes = {
        'name': { 'unique': True },
        'permalink': { 'unique': True },
        'permalink': ASCENDING,
    }

    @staticmethod
    def from_form(form_data):
        # remember to lowercase name and any other stuff
        form_data['name'] = form_data['name'].lower()
        form_data['permalink'] = slugify(form_data['name'])
        return Category(form_data)


class Product(SlugDocument):
    __collection__ = 'products'
    fields = ['name', 'description', 'price', 'size', 'thumbnail',
            'background', 'category', 'permalink']

    indexes = {
        'name': { 'unique': True },
        'permalink': ASCENDING,
    }

    @classmethod
    def get_by_category(cls, category_id, to_obj=False):
        return cls._get_many(to_obj, { "category_id": category_id })

    @staticmethod
    def from_form(form_data):
        return NotImplemented

    def get_category(self):
        return Category.get_by_id(self._content['category_id'])


class Variant(Document):
    __collection__ = 'variants'
    fields = ['product_id', 'attributes']
