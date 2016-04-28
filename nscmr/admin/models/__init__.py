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
    fields = ['email', 'name', 'dob', 'roles', 'addresses', 'wishlist',
            'orders', 'cart']
    defaults = {
        'roles': ['user'],
        'addresses': [],
        'wishlist': [],
        'orders': [],
        'cart': []
    }
    # required fields
    required_fields = ['name', 'password']
    indexes = {
        'email': { 'unique': True },
        'email': ASCENDING,
    }

    @staticmethod
    def from_form(form_data):
        form_data['email'] = form_data['email'].lower()

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

    @classmethod
    def get_by_email(cls, email, to_obj=False):
        return cls._get_one(to_obj, { "email": email })


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

    def get_name(self):
        return self._content['name'].capitalize()


class Product(SlugDocument):
    __collection__ = 'products'
    # category should contain name and _id
    fields = ['name', 'description', 'category', 'meta_description',
            'permalink']

    indexes = {
        'name': { 'unique': True },
        'permalink': { 'unique': True },
        'permalink': ASCENDING,
    }

    @classmethod
    def get_by_category(cls, category_id, to_obj=False):
        return cls._get_many(to_obj, { "category._id": str(category_id) })

    @staticmethod
    def from_form(form_data):
        form_data['name'] = form_data['name'].lower()
        form_data['permalink'] = slugify(form_data['name'])
        return Product(form_data)

    def get_category(self):
        return Category.get_by_id(self._content['category']['_id'],to_obj=True)

    def get_name(self):
        return self._content['name'].capitalize()

    def get_variants(self, to_obj=True):
        return Variant._get_many(to_obj, { "product_id": self.id })


class Variant(Document):
    __collection__ = 'variants'
    fields = ['product_id', 'images', 'sku', 'price', 'attributes', 'quantity']
    # images must have the following format { 'big': <url>, 'thumb': <url> }
    # attributes should contain: size, color, etc.. and any other
    # later on though

    indexes = {
        'product_id': ASCENDING,
    }

    @staticmethod
    def from_form(form_data):
        form_data['sku'] = form_data['sku'].upper()
        if 'attributes' in form_data:
            attrs = {}
            for k,v in form_data['attributes'].items():
                attrs[k.lower()] = form_data['attributes'][k].lower()
            form_data['attributes'] = attrs
        return Variant(form_data)

    def get_product(self):
        return Product.get_by_id(self._content['product_id'])

    def get_price(self):
        major = self._content['price']['major']
        minor = self._content['price']['minor']
        price = major + (float(minor)/100)
        return "{} {}".format(self._content['price']['currency'], price)

