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


class Document(object, metaclass=DocumentProperties):
    '''
    Base document class/interface for pymongo

    Methods/attributes to be overridden by child classes are:
        :required_fields - states which fields are required
        :validators - dictionary containing:
                {field_name: [validator,error_msg]}
        (if using validation, which was disabled as of now considering that we
        are using wtforms validation already)
        :from_form - used to parse form_data into the object
        :save

    '''
    required_fields = None
    validators = None

    def __init__(self, content):
        self.content = content

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
                if field not in self.content:
                    raise InvalidDocument("Campo necessário '{}' não existe".\
                            format(field))
        # apply actual validators
        if self.validators is not None:
            for field in self.validators:
                if not self.validators[field][0](self.content[field]):
                    raise InvalidDocument(self.validators[field][1])

    def get_id(self):
        return str(self.content['_id'])

    def save(self):
        # validate is working, but for now it may be better to disable it
        # (mainly because of the password validation -- it must only be
        # validated on creation or password update...)
        # besides that, we are already using wtforms for validation, so it
        # seems like a bit too much for now...
        #self.validate()

        # try to insert the document into the db
        try:
            self.collection.insert_one(self.content)
        # if it already exists, update the 'updated_at' field and replace it
        # entirely
        except DuplicateKeyError:
            self.content['updated_at'] = datetime.utcnow()
            self.collection.replace_one({'_id': self.get_id()}, self.content)

    def __str__(self):
        return str(self.content)

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
