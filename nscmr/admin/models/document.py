# structure inspired by MongoKit, however alot simpler (and supporting
# python3)

from bson import InvalidDocument
from pymongo.errors import DuplicateKeyError
from pymongo import IndexModel

from bson import ObjectId

from datetime import datetime

class DocumentProperties(type):
    """
    Document metaclass for acquiring the collection handler automatically.
    def __new__(cls, name, parents, dct):
        if '__collection__' in dct:
            # get the collection name and set the handler from the db
            dct['collection'] = dct['db'][[dct['__collection__']]]
        return super(DocumentProperties, cls).__new__(cls, name, parents, dct)
    """

    def __init__(self, name, bases, d):
        type.__init__(self, name, bases, d)
        # auto_generating fields..
        if 'fields' in d:
            accessors = {}
            prefixs = ["get_", "set_", "del_"]
            # get custom defined getters, setters and delers
            for k in d.keys():
                v = getattr(self, k)
                for i in range(3):
                    if k.startswith(prefixs[i]):
                        accessors.setdefault(k[4:], [None, None, None])[i] = v
            # add fields to be autogenerated
            d['fields'].append('updated_at')
            for field in d['fields']:
                if field in accessors.keys():
                    continue
                accessors[field] = [None, None, None]
            for name, (getter, setter, deler) in accessors.items():
                if getter is None:
                    getter = lambda self, name=name: self._content.get(name)
                if setter is None:
                    setter = \
                        lambda self,v,name=name:self._content.update({name:v})
                setattr(self, name, property(getter, setter, deler, ""))
            # add the id by hand, considering that it should not have a setter
            # nor a deler (and that the getter is in the document class)
            setattr(self, 'id', property(
                lambda self: self._content.get('_id'), None, None, ""))


class Document(object, metaclass=DocumentProperties):
    '''
    Base document class/interface for pymongo

    Methods/attributes to be overridden by child classes are:
        :fields - fields for which we should autogenerate properties for ease
            of access. To define custom behavior for setters and/or getters,
            simply define a get_{attribute_name} or set_{attribute_name} method
            and this will be passed as property
        :defaults - dictionary containing the default value for the document
            fields declared above.
        :required_fields - states which fields are required
        :validators - dictionary containing:
                {field_name: [validator,error_msg]}
            these two attributes should be overriden if using the document
            class validation, which is not being used as of now, considering
            that we are using wtforms validation already)
        :indexes - indexes to be created on the respective collection
        :from_form - used to parse form_data into the object

    Methods supplied:
        :get_by_id - static method used for retrieving a document by it's id
        :validate - validates fields based on the required_fields and
            validators class attributes. not in use right now, as per the
            above
        :create_indexes - create the collection indexes as specified in the
            indexes list

        :insert - tries to insert a new document in the db
        :update - updates an already existing document
        :__str__
        :__eq__
        :__ne__
    '''
    collection = None
    fields = []
    defaults = {}
    required_fields = []
    validators = {}
    indexes = []

    def __init__(self, content):
        self._content = content

    @staticmethod
    def from_form(form_data):
        return NotImplemented

    @staticmethod
    def as_dict(objects):
        '''
        wrapper method for object results
        this method will return a dictionary with the documents id's as keys
        of another dict with it's fields

        despite being an wrapper of the objects result set (which itself is a
        wrapper of the cursor result) - so a wrapper of a wrapper, the
        advantage here is that we get the properties of the documents, that
        may, or may not, be in the db (or even if it is in the db, the format
        of the property should be friendlier - see the price of the variant to
        get a grip of what we're talking about)
        '''
        result = {}
        for o in objects:
            result[str(o.id)] = {}
            for k in o._content.keys():
                if k != '_id':
                    result[str(o.id)][k] = getattr(o, k)
        return result

    @classmethod
    def create_indexes(cls):
        if cls.indexes not in ([],):
            indexes = []
            for k,v in cls.indexes.items():
                if type(v) is dict:
                    indexes.append(IndexModel(k, **v))
                else:
                    indexes.append(IndexModel([(k, v,)]))
            cls.collection.create_indexes(indexes)

    @classmethod
    def _update_one(cls, query={}, set_data={}, unset_data={}, push_data={},
            pull_data={}, inc_data={}, upsert=False):
        data = { '$currentDate': { 'updated_at': True } }
        if any(set_data):
            data['$set'] = set_data
        if any(unset_data):
            data['$unset'] = unset_data
        if any(push_data):
            data['$push'] = push_data
        if any(pull_data):
            data['$pull'] = pull_data
        if any(inc_data):
            data['$inc'] = inc_data
        return cls.collection.update_one(query, data, upsert)

    @classmethod
    def _update_many(cls, query={}, set_data={}, unset_data={}, push_data={},
            pull_data={}, inc_data={}, upsert=False):
        data = { '$currentDate': { 'updated_at': True } }
        if any(set_data):
            data['$set'] = set_data
        if any(unset_data):
            data['$unset'] = unset_data
        if any(push_data):
            data['$push'] = push_data
        if any(pull_data):
            data['$pull'] = pull_data
        if any(inc_data):
            data['$inc'] = inc_data
        return cls.collection.update_many(query, data, upsert)

    @classmethod
    def update_by_id(cls, doc_id, set_data={}, unset_data={}, push_data={},
            pull_data={}, inc_data={}, upsert=False):
        if isinstance(doc_id, ObjectId):
            query = { '_id': doc_id }
        else:
            query = { '_id': ObjectId(doc_id) }
        return cls._update_one(query, set_data, unset_data, push_data,
                pull_data, inc_data, upsert)

    @classmethod
    def _delete_one(cls, query):
        return cls.collection.delete_one(query)

    @classmethod
    def delete_by_id(cls, doc_id):
        if isinstance(doc_id, ObjectId):
            return cls._delete_one({'_id': doc_id})
        return cls._delete_one({'_id': ObjectId(doc_id)})

    @classmethod
    def _delete_many(cls, query):
        return cls.collection.delete_many(query)

    @classmethod
    def _get_one(cls, to_obj, query, projection={}):
        result = \
            (cls.collection.find_one(query, projection) if any(projection) \
                else cls.collection.find_one(query))
        if result is None or not to_obj:
            return result
        return cls(result)

    @classmethod
    def get_by_id(cls, doc_id, projection={}, to_obj=False):
        if isinstance(doc_id, ObjectId):
            return cls._get_one(to_obj, {'_id': doc_id}, projection)
        return cls._get_one(to_obj, {'_id': ObjectId(doc_id)}, projection)

    @classmethod
    def _get_many(cls, to_obj, query=None):
        if to_obj:
            return [cls(document) for document in cls.collection.find(query)]
        return cls.collection.find(query)

    @classmethod
    def get_all(cls, to_obj=False):
        return cls._get_many(to_obj)

    def update(self, set_data={}, unset_data={}, push_data={}, pull_data={},
            upsert=False):
        return self.update_by_id(self.id, set_data=set_data,
            unset_data=unset_data, push_data=push_data, pull_data=pull_data,
            upsert=False)

    def validate(self):
        # validates existence of fields first
        if self.required_fields is not None:
            for field in self.required_fields:
                if field not in self._content:
                    raise InvalidDocument("Campo necessário '{}' não existe".\
                            format(field))
        # apply actual validators
        if self.validators is not None:
            for field in self.validators:
                if not self.validators[field][0](self._content[field]):
                    raise InvalidDocument(self.validators[field][1])

    def get_id(self):
        return str(self._content['_id'])

    def insert(self):
        # set timestamps for all
        # creation time is already present on mongo ObjectId
        d = datetime.utcnow()
        setattr(self, 'updated_at', d)
        self.collection.insert_one(self._content)

    def update(self):
        self._content['updated_at'] = datetime.utcnow()
        self.collection.replace_one({'_id': self.get_id()}, self._content)

    def delete(self):
        self.delete_by_id(self.id)

    def set_defaults(self):
        for field in self.fields:
            if getattr(self, field) in (None, [], {}):
                if field in self.defaults:
                    setattr(self, field, self.defaults[field])

    def __str__(self):
        return str(self._content)

    def __eq__(self, other):
        '''
        Compares two objects by their id's
        '''
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented

    def __ne__(self, other):
        '''
        Inequality comparator
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


class SlugDocument(Document):
    @classmethod
    def get_by_permalink(cls, permalink, to_obj=False):
        return cls._get_one(to_obj, {'permalink': permalink})

