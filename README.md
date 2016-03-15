# nscmr

## Description
nscmr will be an python e-commerce application based on
[satchless](https://github.com/mirumee/satchless),
[flask](http://flask.pocoo.org/) and
[mongodb](https://www.google.com.br/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwjO6pyTz7TLAhWMkJAKHawuB9sQFggdMAA&url=https%3A%2F%2Fwww.mongodb.org%2F&usg=AFQjCNE3DSenqpJf_ccFT8F4W0RQfaGb3w&sig2=jK5NinRr8peGNPjy77U9mw).

As per the above, nscmr is still under development and not ready for use.

## Instructions
* Install pip
* Install requirements
```pip install -r requirements.txt```

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

The configuration for each mode is located in the nscmr.config module.

NOTE: Please note that the examples below are all using flask's development
server. This is ok for development (and perhaps testing) but not for
production! This is just an example on how to trigger the correct configuration
for the desired app's mode.


## TODO's
### controller
    * see how to correctly
    [send static files](http://flask.pocoo.org/docs/0.10/api/).
    * slugs should be checked against the id of the object to see if they are
      correct!!

### models
    * see python currencies
    * see python countries
    * see python [login/user management](https://blog.openshift.com/use-flask-login-to-add-user-authentication-to-your-python-application/)/[auth](https://github.com/raddevon/flask-permissions)
    * see python phone

#### user / cart
    * cart should be a subdocument of user? remember mongodb has no joins.

#### category
    * category model should have a reference to parent and to ancestors (makes
      it really easy to create subcategories).

### DB
    * read about storing payment options on db

### templates
    * rearrange flash messages in fullwidthheader.html
    * add 'add to wishlist' button

## Development
Current development server is being hosted at
[pythonanywhere.com](http://tls.pythonanywhere.com).

## Known bugs
    * not working.. ;)
