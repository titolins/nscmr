# structure inspired by MongoKit, however alot simpler (and supporting
# python3)

from bson import InvalidDocument
from pymongo.errors import DuplicateKeyError

from datetime import datetime

# import db so we have access to the collections through the models
from nscmr import db

class DocumentProperties(type):
    """
    Document metaclass for acquiring the collection handler automatically.
    """
    def __new__(cls, name, parents, dct):
        if '__collection__' in dct:
            # get the collection name and set the handler from the db
            dct['collection'] = db[dct['__collection__']]
        return super(DocumentProperties, cls).__new__(cls, name, parents, dct)

    def __init__(self, name, bases, d):
        type.__init__(self, name, bases, d)
        # auto_generating fields..
        if 'fields' in d:
            accessors = {}
            prefixs = ["get_", "set_", "del_"]
            for k in d.keys():
                v = getattr(self, k)
                for i in range(3):
                    if k.startswith(prefixs[i]):
                        accessors.setdefault(k[4:], [None, None, None])[i] = v
            for field in d['fields']:
                if field in accessors.keys():
                    continue
                accessors[field] = [None, None, None]
            for name, (getter, setter, deler) in accessors.items():
                name = name
                if getter is None:
                    getter = lambda self, name=name: self._content[name] if \
                            name in self._content else None
                if setter is None:
                    setter = \
                        lambda self,v,name=name:self._content.update({name:v})
                setattr(self, name, property(getter, setter, deler, ""))


class Document(object, metaclass=DocumentProperties):
    '''
    Base document class/interface for pymongo

    Methods/attributes to be overridden by child classes are:
        :required_fields - states which fields are required
        :validators - dictionary containing:
                {field_name: [validator,error_msg]}
            these two attributes should be overriden if using the document
            class validation, which is not being used as of now, considering
            that we are using wtforms validation already)
        :fields - fields for which we should autogenerate properties for ease
            of access. To define custom behavior for setters and/or getters,
            simply define a get_{attribute_name} or set_{attribute_name} method
            and this will be passed as property
        :from_form - used to parse form_data into the object

    Methods supplied:
        :get_by_id - static method used for retrieving a document by it's id
        :validate - validates fields based on the required_fields and
            validators class attributes. not in use right now, as per the
            above

        :save - tries to insert the document in it's respective collection. If
            the document already exists, we simply update it.
        :__str__
        :__eq__
        :__ne__
    '''
    required_fields = None
    validators = None
    autogen_fields = None

    def __init__(self, content):
        self._content = content

    @staticmethod
    def from_form(self):
        return NotImplemented

    @classmethod
    def get_by_id(cls, doc_id):
        return cls(cls.collection.find_one({'_id': doc_id}))

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

    def save(self):
        # validate is working, but for now it may be better to disable it
        # (mainly because of the password validation -- it must only be
        # validated on creation or password update...)
        # besides that, we are already using wtforms for validation, so it
        # seems like a bit too much for now...
        #self.validate()

        # try to insert the document into the db
        try:
            self.collection.insert_one(self._content)
        # if it already exists, update the 'updated_at' field and replace it
        # entirely
        except DuplicateKeyError:
            self._content['updated_at'] = datetime.utcnow()
            self.collection.replace_one({'_id': self.get_id()}, self._content)

    def __str__(self):
        return str(self._content)

    def __eq__(self, other):
        '''
        Compares two objects by their id's
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
