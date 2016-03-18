from datetime import datetime
from bson.objectid import ObjectId

from nscmr import db
from nscmr import login_manager

# should i create manager classes or even classes representing the documents
# instead of this approach?
collection = db.users

#########
# Helpers
#########


def get_user_by_id(user_id):
    return User(collection.find_one({'_id': user_id}))


def persist_user(user_form):
    '''Try to persist a user into the db

    :user_form - form submitted via post request
    '''
    # substitute for datatime.now() and use a tz
    date = datetime.utcnow()
    # use email as _id and delete email so we don't get repeated fields
    user_form['_id'] = user_form['email']
    # converts date object to datetime, as pymongo only support the later
    user_form['dob'] = datetime.combine(user_form['dob'], datetime.min.time())
    del(user_form['email'])
    # delete next
    del(user_form['next'])
    collection.insert_one(user_form)
    return User(user_form)


#############
# Flask-Login
#############


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


class User(dict):
    '''User class for Flask-Login

    This class is the same as the Flask-Login UserMixin class, but has been
    implemented as a dictionary considering that we are using pymongo driver
    directly.
    '''
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
        return str(self['_id'])

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
