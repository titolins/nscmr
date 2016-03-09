########################################################################
#####  Address                     #####################################
########################################################################
#####                                                      #############
#####                                                      #############
#####  Address in memory model class for use during the    #############
#####  development of nscmr.                               #############
#####                                                      #############
#####  Classes:                                            #############
#####     Address                                          #############
#####     AddressFactory                                   #############
#####                                                      #############
#####                                                      #############
#####                                          2016-03-09  #############
#####                                                      #############
########################################################################


class AddressFactory(object):
    def getUserAddresses(self, user_id):
        # study countries, states and phones (should they be their own models?)
        return [
                Address(
                    user_id, 'home', 'example street, 123', 'nghbd', 'city',
                    '0000000', 'country', 'state', '0000 00 00000000'),
                Address(
                    user_id, 'office', 'example street, 123', 'nghbd', 'city',
                    '0000000', 'country', 'state', '0000 00 00000000'),
                ]


class Address(object):
    def __init__(self, user_id, title, street_address_1, street_address_2, city,
            postal_code, country, state, phone=None):
        self.user_id = user_id
        self.title = title
        self.street_address_1 = street_address_1
        self.street_address_2 = street_address_2
        self.city = city
        self.postal_code = postal_code
        self.country = country
        self.state = state
        self.phone = phone


if __name__ == '__main__':
    pass
