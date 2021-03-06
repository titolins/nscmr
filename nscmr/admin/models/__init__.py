from datetime import datetime
from bson.objectid import ObjectId
from pymongo import ASCENDING

from flask import current_app, session
from flask.ext.login import current_user

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from nscmr.admin.models.document import Document, SlugDocument

from nscmr.admin.helper import slugify

from ..forms import product_images, category_images

from ..helper import make_thumb

from markdown import markdown


class User(Document):
    '''User class
    '''
    __collection__ = 'users'
    fields = ['email', 'name', 'dob', 'roles', 'addresses', 'wishlist',
        'cart', 'oauth', 'orders']
            #'orders']
    defaults = {
        'roles': ['user'],
        'addresses': [],
        'wishlist': [],
        'orders': [],
        'cart': {}
    }
    # required fields
    required_fields = ['name', 'email', 'password']
    indexes = {
        'email': { 'unique': True },
        #'email': ASCENDING,
    }

    @staticmethod
    def from_form(form_data):
        data = {
            'roles': ['user'],
            'oauth': {},
            'addresses': [],
            'wishlist': [],
            'cart': { 'items': [] },
            'name': form_data['name'].lower(),
            'email': form_data['email'].lower() }#,
            #'orders': [] }
        form_keys = form_data.keys()
        keys = []
        for k in form_keys:
            if k not in ('confirm', 'has_address', 'name', 'email'):
                keys.append(k)
        if 'oauth' in keys:
            data['oauth'] = {
                form_data['oauth']['provider'].lower(): {
                    'user_token': form_data['oauth']['userToken'],
                }
            }
        else:
            for k in keys:
                if form_data[k] not in (None, ''):
                    if k == 'dob':
                        # converts date object to datetime,
                        # as pymongo only support the latter
                        field_data = datetime.combine(
                            form_data[k],
                            datetime.min.time())
                    elif k == 'password':
                        # hash password
                        field_data = generate_password_hash(form_data[k])
                    elif k == 'is_admin':
                        if form_data[k]:
                            data['roles'].append('admin')
                        continue
                    elif k == 'address':
                        if form_data['has_address']:
                            address = {
                                k: v.lower() for k,v in form_data[k].items() \
                                    if k is not 'street_number' }
                            address['street_number'] = \
                                form_data[k]['street_number']
                            address['_id'] = ObjectId()
                            data['addresses'] = [ address, ]
                        continue
                    else:
                        field_data = form_data[k]
                    data[k] = field_data
        return User(data)

    @staticmethod
    def get_by_email(email, to_obj=False):
        return User._get_one(to_obj, { "email": email })

    @staticmethod
    def get_cart_item(id_, var_id, to_obj=False):
        return User._get_one(to_obj,
            {
                '_id': id_ if isinstance(id_, ObjectId) else ObjectId(id_),
                'cart.items._id': var_id
            },
            {
                '_id': 0,
                'cart.items.$': 1
            })['cart']['items'][0]

    @staticmethod
    def clean_cart(id_):
        user = User.get_by_id(id_)
        for item in user['cart']['items']:
            Variant.update_by_id(
                item['_id'],
                inc_data={
                    'reserved': -(item['quantity'])
                })
        return User.update_by_id(id_, set_data={'cart':{}})

    @staticmethod
    def remove_from_wishlists(var_id):
        return User._update_many({}, pull_data={'wishlist':{'_id': var_id}})

    @staticmethod
    def remove_from_carts(var_id):
        return User._update_many({}, pull_data={'cart.items':{'_id': var_id}})

    @staticmethod
    def update_address_by_id(addr_id, set_data):
        return User._update_one(
            {"addresses._id": addr_id if isinstance(addr_id, ObjectId) \
                else ObjectId(addr_id) },
            set_data=set_data)

    @staticmethod
    def get_address_by_id(addr_id):
        return User._get_one(
            False,
            {'addresses._id': addr_id if isinstance(addr_id, ObjectId) \
                else ObjectId(addr_id)},
            {
                'addresses.$': 1,
                '_id': 0,
            })['addresses'][0]

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_dob(self):
        if 'dob' in self._content and self._content['dob'] is not None:
            return "{:%d/%m/%Y}".format(self._content['dob'])
        return None

    def check_password(self, password):
        return check_password_hash(self._content['password'], password)

    def get_orders(self):
        return Order.get_by_user_id(self.id)


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

    @staticmethod
    def get_by_name(name, to_obj=False):
        return Category._get_one(to_obj, { "name": name })

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

    @staticmethod
    def get_summary_by_variant(var_id, to_obj=False):
        return Summary._get_one(to_obj,
            {
                'variants._id': var_id if isinstance(var_id, ObjectId) else \
                    ObjectId(var_id)
            },
            {
                'name': 1,
                'permalink': 1,
                'category': 1,
                'variants': { '$elemMatch': {'_id': var_id } }
            })

    @staticmethod
    def insert_variant_img(var_id, img):
        return Summary._update_one(
            query={
                'variants._id':
                        var_id if isinstance(var_id,ObjectId) else \
                                ObjectId(var_id)
            },
            push_data={
                'variants.$.images': img
            }
        )

    @staticmethod
    def remove_variant_img(var_id, img):
        return Summary._update_one(
            query={
                'variants._id':
                        var_id if isinstance(var_id,ObjectId) else \
                                ObjectId(var_id)
            },
            pull_data={
                'variants.$.images': {'id': img }
            }
        )

class Product(SlugDocument):
    __collection__ = 'products'
    # category should contain name and _id
    fields = ['name', 'description', 'category', 'meta_description',
            'permalink', 'attributes', 'variants', 'shipping']

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
            elif field == 'description':
                html_description = markdown(
                    form_data[field],
                    extensions=['markdown.extensions.nl2br'])
                product_data[field] = summary_data[field] = html_description
            elif field in ('shipping', 'meta_description'):
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

class Image(Document):
    __collection__ = 'images'
    fields = ['full', 'thumb']
    @staticmethod
    def from_form(form_data):
        field_data = []
        for img in form_data:
            if img.filename not in ('', None):
                filename = secure_filename(img.filename.rsplit('.',1)[0])
                ext = img.filename.rsplit('.',1)[1]
                if ext.lower() == 'jpg':
                    ext = 'jpeg'
                img_filename = "{}.{}".format(
                    filename, ext)
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
                field_data.append(Image(img_dict))

        return field_data

    def as_dict(self):
        i_dict = {}
        i_dict['id'] = str(self.id)
        for field in self.fields:
            if field == 'updated_at':
                continue
            i_dict[field] = getattr(self, field)
        return i_dict

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
                elif field == 'price':
                    var_data[field] = int(form_data['price']*100)
                    summary_data[field] = \
                        "{0:.2f}".format(form_data['price']).replace('.',',')
                else:
                    var_data[field] = form_data[field]

                var_data['product_id'] = product.id
        print(var_data)
        return Variant(var_data), summary_data

    @staticmethod
    def get_by_img(variant_id, img_id, to_obj=False):
        return Variant._get_one(to_obj,
            {
            '_id': variant_id if isinstance(variant_id, ObjectId) else \
                    ObjectId(variant_id),
            'images': img_id,
            })

    @staticmethod
    def remove_image(variant_id, image):
        print(variant_id)
        print(image)
        query = {
            '_id': variant_id if isinstance(variant_id, ObjectId) else \
                   ObjectId(variant_id)
        }
        Variant._update_one(query=query, pull_data={"images":image})
        Summary.remove_variant_img(variant_id, image)


    @staticmethod
    def add_image(variant_id, image):
        if Variant.get_by_img(variant_id, image,to_obj=True) is not None:
            return
        img = Image.get_by_id(image, to_obj=True)
        query = {
            '_id': variant_id if isinstance(variant_id, ObjectId) else \
                   ObjectId(variant_id)
        }
        Variant._update_one(query=query, push_data={"images":image})
        Summary.insert_variant_img(variant_id, img.as_dict())

    @staticmethod
    def delete_by_product(product_id):
        if isinstance(product_id, ObjectId):
            return Variant._delete_many({'product_id':product_id})
        return Variant._delete_many({'product_id':ObjectId(product_id)})

    @staticmethod
    def update_by_id_and_qty(id_, qty, set_data={}, unset_data={},
            push_data={}, pull_data={}, inc_data={}, upsert=False):
        query = {
            '_id': id_ if isinstance(id_, ObjectId) else ObjectId(id_),
            'quantity': { '$gte': qty }
        }
        return Variant._update_one(query, set_data, unset_data, push_data,
            pull_data, inc_data, upsert)

    @staticmethod
    def get_by_product(p_id, to_obj=True):
        return Variant._get_many(to_obj,
            { "product_id":
                p_id if isinstance(p_id, ObjectId) else ObjectId(p_id) })

    def get_product(self):
        return Product.get_by_id(self._content['product_id'], to_obj=True)

    def get_price(self):
        return float(self._content['price']/100)

    def as_dict(self):
        v_dict = {}
        v_dict['id'] = str(self.id)
        for field in self.fields:
            if field in ('updated_at', 'created_at', 'product_id'):
                continue
            v_dict[field] = getattr(self, field)
        return v_dict


class CartLine(object):

    def __init__(self, cart_item):
        variant = Variant.get_by_id(cart_item['_id'], to_obj=True)
        if 'display_image' in variant._content.keys():
            thumb = Image.get_by_id(variant.display_image)['thumb']
        else:
            thumb = Image.get_by_id(variant.images[0])['thumb']

        product = variant.product
        category = product._content['category']
        self._item_info = {
            '_id': cart_item['_id'],
            'name': product.name,
            'permalink': product.permalink,
            'description': product.description,
            'category': {
                '_id': category['_id'],
                'name': category['name'],
                'permalink': category['permalink'],
            },
            'price': variant.price,
            'attributes': variant.attributes,
            'quantity': cart_item['quantity'],
            'thumb': thumb,
            #'shipping': product.shipping
        }

    def __call__(self):
        return self._item_info

class Order(Document):
    __collection__ = 'orders'
    fields = ['cart_info',  'user_id', 'reference', 'address']

    def from_form(form_data, cart, address):
        # parse response_json from mundipagg, add user info and return
        data = {
            'user': { 
                '_id': current_user.id,
                'name': current_user.name,
            },
            'date': form_data['transaction']['date'],
            'reference': form_data['transaction']['reference'],
            'pagseguro_code': form_data['transaction']['code'],
            'status': {
                'code': form_data['transaction']['status'],
                'msg': 'Pagamento confirmado' if \
                        form_data['transaction']['status'] == 3 else \
                        'Pagamento em análise'
            },
            'cart_info': cart,
            'address': address,
        }

        return Order(data)

    @staticmethod
    def get_by_user_id(user_id, to_obj=False):
        return Order._get_many(to_obj, { "user._id": user_id })

    @staticmethod
    def get_by_reference(reference, to_obj=False):
        return Order._get_one(to_obj, { 'reference': reference })

    @staticmethod
    def update_order_status(reference, status_data):
        return Order._update_one(to_obj, set_data={
            'status': status_data
        })

