# nscmr

## Description
nscmr will be an python e-commerce application based on [satchless], [flask]
and [mongodb].

As per the above, nscmr is still under development and not ready for use.

## Instructions
* Install pip
* Install requirements
```
pip install -r requirements.txt
```

### App modes
The app may be run in development, testing or production modes. To trigger the
correct configuration for each mode, the user must set the FLASK_APP_MODE
environment variable, as per the below:
```
# running in development mode
FLASK_APP_MODE=developement python runserver.py

# running in testing mode
FLASK_APP_MODE=testing python runserver.py

# running in production mode
FLASK_APP_MODE=production python runserver.py
```

### Interactive shell
A get_interactive bash script is provided herein for easy access to a
interactive shell for the app. run `./get_interactive help` to see it's usage.

The configuration for each mode is located in the nscmr.config module. If you
don't set any of the above mentioned settings, the app will fallback to it's
default configuration (development currently).

NOTE: Please note that the examples below are all using flask's development
server. This is ok for development (and perhaps testing) but not for
production! This is just an example on how to trigger the correct configuration
for the desired app's mode.


## TODO's
### controller
    * see how to correctly [send static files].
    * slugs should be checked against the id of the object to see if they are
      correct!!
    * create custom error in case of wrong login/password

### models
    * see python currencies
    * see python countries
    * see python [login/user management]/[auth]
    * see python phone

#### user
    * implement password hashing and ssl support.

#### cart
    * cart should be a subdocument of user? remember mongodb has no joins.

#### category
    * category model should have a reference to parent and to ancestors (makes
      it really easy to create subcategories).

### DB
    * read about storing payment options on db
    * read about storing passwords options on db
    * [configure indexes].
    * mongodb references
        * [manual ref vs dbref]
        * [mongo ref docs]

### templates
    * rearrange flash messages in fullwidthheader.html
    * add 'add to wishlist' button to products

### tracking
    * after building the initial db, configure [Flask-Analytics].

## Development
Current development server is being hosted at [pythonanywhere.com].

## Known bugs
    * not working.. ;)

[satchless]:https://github.com/mirumee/satchless
[flask]:http://flask.pocoo.org/
[mongodb]:https://www.mongodb.org/

[send static files]:http://flask.pocoo.org/docs/0.10/api/
[auth]:https://github.com/raddevon/flask-permissions
[login/user management]:https://blog.openshift.com/use-flask-login-to-add-user-authentication-to-your-python-application/
[configure indexes]:https://docs.mongodb.org/manual/tutorial/create-indexes-to-support-queries/
[manual ref vs dbref]:http://dba.stackexchange.com/questions/82970/mongodb-manual-references-vs-dbref
[mongo ref docs]:https://docs.mongodb.org/manual/reference/database-references/#document-reference://docs.mongodb.org/manual/reference/database-references/#document-references

[Flask-Analytics]:https://github.com/citruspi/Flask-Analytics
[python anywhere]:http://tls.pythonanywhere.com
