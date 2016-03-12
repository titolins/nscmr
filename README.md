# nscmr

## Description
nscmr will be an python e-commerce application based on
[satchless](https://github.com/mirumee/satchless),
[flask](http://flask.pocoo.org/) and
[mongodb](https://www.google.com.br/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwjO6pyTz7TLAhWMkJAKHawuB9sQFggdMAA&url=https%3A%2F%2Fwww.mongodb.org%2F&usg=AFQjCNE3DSenqpJf_ccFT8F4W0RQfaGb3w&sig2=jK5NinRr8peGNPjy77U9mw).

As per the above, nscmr is still under development and not ready for use.

## TODO's
### controller
    * see how to correctly
    [send static files](http://flask.pocoo.org/docs/0.10/api/).
    * slugs should be checked against the id of the object to see if they are
      correct!!

### models
    * see python currencies
    * see python countries
    * see python login/[auth](https://github.com/raddevon/flask-permissions)/user management
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
