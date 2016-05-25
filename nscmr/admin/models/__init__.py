from datetime import datetime
from bson.objectid import ObjectId
from pymongo import ASCENDING

from flask import current_app

from werkzeug.security import check_password_hash, generate_password_hash

from nscmr.admin.models.document import Document, SlugDocument

from nscmr.admin.helper import slugify

from ..forms import product_images, category_images

from ..helper import make_thumb

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
    required_fields = ['name', 'email', 'password']
    indexes = {
        'email': { 'unique': True },
        #'email': ASCENDING,
    }

    @staticmethod
    def from_form(form_data):
        data = { 'roles': ['user'] }
        for k in form_data.keys():
            if k in ('name', 'email'):
                field_data = form_data[k].lower()
            elif k == 'dob' and form_data[k] is not None:
                # converts date object to datetime, as pymongo only support the latter
                field_data = datetime.combine(form_data[k],datetime.min.time())
            elif k == 'password':
                # hash password
                field_data = generate_password_hash(form_data[k])
            elif k == 'confirm':
                # delete confirm field
                continue
            elif k == 'is_admin':
                print(form_data[k])
                if form_data[k]:
                    data['roles'].append('admin')
                continue
            else:
                field_data = form_data[k]
            data[k] = field_data

        return User(data)

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
        #'permalink': { 'unique': True },
        'permalink': ASCENDING,
        'parent._id': ASCENDING,
    }

    @staticmethod
    def from_form(form_data):
        data = {}
        for field in form_data.keys():
            if field == 'name':
                field_data = form_data[field].lower()
                data['permalink'] = slugify(field_data)
            elif field == 'parent':
                parent_info = form_data[field].split('_')
                if parent_info[0] != "None":
                    field_data = {
                        '_id': parent_info[0],
                        'name': parent_info[1],
                    }
                else:
                    continue
            elif field == 'base_img':
                img_filename = category_images.save(form_data[field],
                    name="{}.".format(form_data['name']))
                field_data = category_images.url(img_filename)
            else:
                field_data = form_data[field]
            data[field] = field_data
        return Category(data)

    @staticmethod
    def get_by_parent(parent_id, to_obj=False):
        return Category._get_many(to_obj, { "parent._id": str(parent_id) })

    def get_name(self):
        return self._content['name'].capitalize()


class Summary(Document):
    '''
    Summary collection for single querying on category pages
    '''
    __collection__ = 'summary'

    indexes = {
        'variants._id': ASCENDING,
    }

    @staticmethod
    def get_by_category(category_id, to_obj=False):
        return Summary._get_many(to_obj, { "category._id": str(category_id) })

    @staticmethod
    def update_by_category(category_id, set_data):
        return Summary._update_many({'category._id':str(category_id)},set_data)


class Product(SlugDocument):
    __collection__ = 'products'
    # category should contain name and _id
    fields = ['name', 'description', 'category', 'meta_description',
            'permalink', 'attributes', 'variants']

    indexes = {
        'name': { 'unique': True },
        #'permalink': { 'unique': True },
        'permalink': ASCENDING,
        'category._id': ASCENDING,
    }

    @staticmethod
    def get_by_category(category_id, to_obj=False):
        return Product._get_many(to_obj, { "category._id": str(category_id) })

    @staticmethod
    def update_by_category(category_id, set_data):
        return Product._update_many({'category._id':str(category_id)},set_data)

    @staticmethod
    def delete_by_category(category_id):
        return Product._delete_many({'category._id':category_id})

    @staticmethod
    def from_form(form_data):
        product_data = {}
        summary_data = {}
        for field in form_data.keys():
            if field == 'name':
                product_data[field] = form_data['name'].lower()
                product_data['permalink'] = slugify(product_data['name'])
                summary_data[field] = product_data[field]
                summary_data['permalink'] = product_data['permalink']
            elif field == 'category':
                category_info = form_data[field].split('_')
                product_data[field] = { 
                    '_id': category_info[0],
                    'name': category_info[2],
                    'permalink': category_info[1] }
                summary_data['category'] = {
                    '_id': category_info[0],
                    'permalink': category_info[1] }
            elif field in ('description', 'meta_description'):
                product_data[field] = form_data[field]
            # skip variants related info
            else:
                continue
        summary_data['variants'] = []
        return Product(product_data), Summary(summary_data)

    def get_category(self):
        return Category.get_by_id(self._content['category']['_id'],to_obj=True)

    def get_name(self):
        return self._content['name'].capitalize()

    def get_variants(self, to_obj=True):
        return Variant._get_many(to_obj, { "product_id": self.id })

    def as_dict(self):
        p_dict = {}
        p_dict['id'] = str(self.id)
        for field in self.fields:
            field_data = None
            if field == 'updated_at':
                continue
            elif field == 'variants':
                vs = []
                for v in self.variants:
                    vs.append(v.as_dict())
                field_data = vs
            elif field == 'category':
                field_data = self.category.name
            else:
                field_data = getattr(self, field)
            p_dict[field] = field_data
        return p_dict


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
    def from_form(form_data, product):
        var_data = {}
        summary_data = {}
        for field in form_data.keys():
            if field in ('has_variants','variants','category','attr_1_value',
                    'attr_2_value'):
                continue
            elif form_data[field] not in (None, ''):
                if field == 'sku':
                    var_data[field] = form_data['sku'].lower()
                elif field in ('attr_1_name', 'attr_2_name'):
                    field_value = \
                        form_data['attr_{}_value'.format(field.split('_')[1])]
                    if field_value not in ('', None):
                        if 'attributes' not in var_data.keys():
                            var_data['attributes'] = {}
                        var_data['attributes'][form_data[field].lower()] = \
                            field_value.lower()
                elif field == 'images':
                    field_data = []
                    for img in form_data[field]:
                        if img.filename not in ('', None):
                            img_filename = "{}.".format(product.permalink)
                            # save the regular image
                            img_filename = product_images.save(img,
                                name=img_filename)
                            # get it's url
                            img = product_images.url(img_filename)
                            # create the thumbnail and get it's url
                            thumb = product_images.url(make_thumb(img_filename,
                                product_images.default_dest(current_app)))
                            # create this image dict and append to the whole
                            img_dict = {'full': img, 'thumb': thumb}
                            field_data.append(img_dict)
                            if 'image' not in summary_data.keys():
                                summary_data['image'] = img_dict['thumb']
                    var_data[field] = field_data
                elif field == 'price':
                    var_data[field] = {
                        'currency': 'BRL',
                        'major': int(form_data['price']),
                        'minor': int((form_data['price']*100)%100)
                    }
                    summary_data[field] = \
                        "{0:.2f}".format(form_data['price']).replace('.',',')
                else:
                    var_data[field] = form_data[field]

                var_data['product_id'] = product.id
        return Variant(var_data), summary_data


    @staticmethod
    def delete_by_product(product_id):
        if isinstance(product_id, ObjectId):
            return Variant._delete_many({'product_id':product_id})
        return Variant._delete_many({'product_id':ObjectId(product_id)})

    def get_product(self):
        return Product.get_by_id(self._content['product_id'], to_obj=True)

    def get_price(self):
        major = self._content['price']['major']
        minor = self._content['price']['minor']
        price = major + (float(minor)/100)
        if self._content['price']['currency'] == 'BRL':
            return "{} {}".format('R$', price)
        return "{} {}".format(self._content['price']['currency'], price)

    def as_dict(self):
        v_dict = {}
        v_dict['id'] = str(self.id)
        for field in self.fields:
            if field in ('updated_at', 'created_at', 'product_id'):
                continue
            v_dict[field] = getattr(self, field)
        return v_dict


