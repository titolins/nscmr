# nscmr

## Description
nscmr will be an python e-commerce application based on [flask] and [mongodb].

As the admin panel, we chose [flat admin v.2] because of it's neat design :)
(probably our best choice so far hehe)

As per the above, nscmr is still under development and not ready for use.

## Instructions
* Create instance and uploads folder
* Generate secret key
* Install npm:
    * install bower and then install jquery, bootstrap font-awesome and angular:
    ```
    sudo npm install -g bower
    # bower needs to be initialized in the uppermost nscmr folder
    cd nscmr
    bower init
    # may be required to create a symlink, as per the below
    ln -s /usr/bin/nodejs /usr/bin/node
    bower install -S jquery bootstrap font-awesome angular angular-ui-mask \
        angular-i18n
    ```
    * copy glyphicon fonts to static dir:
    ```
    mkdir static/fonts
    cp bower_components/bootstrap/fonts/* static/fonts/
    cp bower_components/font-awesome/fonts/* static/fonts/
    ```
* Install docker:
    ```
    apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys \
        58118E89F3A912897C070ADBF76221572C52609D
    echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > \
        /etc/apt/sources.list.d/docker.list

    apt-get update && apt-get install docker-engine

    ```
* Create a volume to store the db data and the app container:
    ```
    docker volume create --driver local --name dbdata
    docker build -t nscmr .
    ```
* Run the nscmr docker container indicating the volume and mongodb path:
    ```
    docker run -v dbdata:/var/lib/mongodb -d -p 8000:80 --name nscmr nscmr
    ```
* Lastly, we have to get a shell of the container to start the mongod:
    ```
    $ docker exec -it nscmr /bin/bash

    # service mongod start
    # exit

    $
    ```

### Updating
* To update the application you must stop the currently running container,
    remove it, delete it's image, then rebuild it and restart the container:
    ```
    docker stop nscmr
    docker rm nscmr
    docker rmi nscmr
    docker built -t nscmr .
    docker run -v dbdata:/var/lib/mongodb -d -p 8000:80 --name nscmr nscmr
    ```
* Access a tty to start the mongod again:
    ```
    $ docker exec -it nscmr /bin/bash

    # service mongod start
    ```

### App modes
The app may be run in development, testing or production modes. To trigger the
correct configuration for each mode, the user must point the APP_CONFIG_FILE
environment variable to the corresponding config file, as per the below:
```
# running in development mode
APP_CONFIG_FILE=$APP_ROOT/nscmr/nscmr/config/development.py python runserver.py

# running in testing mode
APP_CONFIG_FILE=$APP_ROOT/nscmr/config/testing.py python runserver.py

# running in production mode
APP_CONFIG_FILE=$APP_ROOT/nscmr/config/production.py python runserver.py
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
    * slugs should be checked against the id of the object to see if they are
      correct!!
    * create custom error in case of wrong login/password

#### user
    * implement ssl support.
    * change datetime.utcnow() @ User.from_form and Document.insert to use the
      correct tz.
    * implement address (and phone?) form field(s) and it's validations.

##### cart
    * cart should be a subdocument of user? yes!!

### DB
    * read about storing payment options on db -> _postponed to another moment_
    * [configure indexes]
        * indexes should be created on the background in production and only if
            they don't already exist.
    * mongodb references
        * [manual ref vs dbref]
        * [mongo ref docs]
    * read about user input validation:
        * should we validate only on form or when saving to db too?\
        * implement javascript/[html validation] on forms

### templates
    * rearrange flash messages in fullwidthheader.html
    * add 'add to wishlist' button to products
    * incorporate admin css into studio duvet (registration page)
        * Think if user page should not use card as well (instead of sidebar)
        * Use the already existing js to make the transitions in user page
            (jquery or bootstrap??) - basically delete user.js
    * incorporate different js and styles under main files and remove styles
        and scripts blocks
    * use flask-assets on the admin bp.

### forms
    * better validation feedback on edition fields
    * manage to pass generic form errors (when of wrong email/login, e.g.) to
        be rendered above fields..

### tracking
    * after building the initial db, configure [Flask-Analytics].

## Development
    * Current dev server on digital ocean

## Known bugs
    * not working.. ;)

[flask]:http://flask.pocoo.org/
[mongodb]:https://www.mongodb.org/
[flat admin v.2]:https://github.com/tui2tone/flat-admin-bootstrap-templates

[send static files]:http://flask.pocoo.org/docs/0.10/api/
[auth]:https://github.com/raddevon/flask-permissions
[login/user management]:https://blog.openshift.com/use-flask-login-to-add-user-authentication-to-your-python-application/
[configure indexes]:https://docs.mongodb.org/manual/tutorial/create-indexes-to-support-queries/
[manual ref vs dbref]:http://dba.stackexchange.com/questions/82970/mongodb-manual-references-vs-dbref
[mongo ref docs]:https://docs.mongodb.org/manual/reference/database-references/#document-reference://docs.mongodb.org/manual/reference/database-references/#document-references

[Flask-Analytics]:https://github.com/citruspi/Flask-Analytics
[html validation]:https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5/Constraint_validation
