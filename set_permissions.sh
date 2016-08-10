#!/bin/bash

APP_DIR=/var/www/nscmr

chgrp -R www-data $APP_DIR
find $APP_DIR -type d -exec chmod 775 {} \;
find $APP_DIR -type f -exec chmod 664 {} \;
chmod +x *.sh


