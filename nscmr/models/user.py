########################################################################
#####  User class                  #####################################
########################################################################
#####                                                      #############
#####  Base user-related classes to represent app's users. #############
#####                                                      #############
#####  For developing purposes only.                       #############
#####                                                      #############
#####  Classes:                                            #############
#####     UserFactory                                      #############
#####     User                                             #############
#####                                                      #############
#####                                                      #############
#####                                          2016-01-29  #############
#####                                                      #############
########################################################################

from nscmr.models.product import ProductFactory

class UserFactory(object):
    def __init__(self, max_users=2):
        pf = ProductFactory()
        self._max_users = max_users
        self.count = 0
        self.names = [
                'user1',
                'user2',
        ]
        self.emails = [
                'awesome_dude@example.com',
                'badmuthafuka27@example.com',
        ]
        self.passwords = [
                'c00lp455',
                'wooow1876',
        ]
        self.wishlist = pf.getProducts()
        self.addresses = [
                [
                    {
                        'name': 'home',
                        'stAdd': 'example street, 201',
                        'city': 'example city',
                        'country': 'example country',
                        'zipCode': '00000-000',
                    },
                    {
                        'name': 'office',
                        'stAdd': 'example street, 301',
                        'city': 'example city',
                        'country': 'example country',
                        'zipCode': '00000-000',
                    }
                ],
                [
                    {
                        'name': 'home',
                        'stAdd': 'bingo street, 1000',
                        'city': 'cool city',
                        'country': 'country',
                        'zipCode': '99999-666',
                    },
                    {
                        'name': 'office',
                        'stAdd': 'else street, 301',
                        'city': 'city',
                        'country': 'example',
                        'zipCode': '12345-000',
                    }
                ]
        ]

    def getIndex(self):
        i = self.count
        self.count += 1
        return i%self._max_users

    def getId(self):
        return self.count

    def getGender(self):
        return ['m', 'f'][self.count % 2]

    def getNewUser(self, access_level=0, randomize_al=False):
        if randomize_al:
            access_level = self.getIndex()
        return User(
            id_ = self.getId(),
            email = self.emails[self.getIndex()],
            password = self.passwords[self.getIndex()],
            name = self.names[self.getIndex()],
            gender = self.getGender(),
            addresses = self.addresses[self.getIndex()],
            access_level = access_level,
            wishlist = self.wishlist,
        )

    def getRegularUser(self):
        return self.getNewUser(access_level=0)

    def getAdminUser(self):
        return self.getNewUser(access_level=1)


class User(object):
    def __init__(self, id_, email, password, name, gender, addresses, wishlist,
            access_level=0):
        self._password = password
        self._cart = None

        self.id_ = id_
        self.name = name
        self.email = email
        self.gender = gender
        self.password_hash = hash(password)
        self.addresses = addresses
        self.access_level = access_level
        self.wishlist = wishlist

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password
        self.password_hash = hash(password)

    def __str__(self):
        return str(
                {
                    attr: str(getattr(self, attr)) for attr in \
                        dir(self) if not attr.startswith('_')
                })

if __name__ == '__main__':
    uf = UserFactory()
    user = uf.getNewUser()
