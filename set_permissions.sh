#!/bin/bash

$APP_DIR='/var/www'

chgrp -R www-data $APP_DIR
find $APP_DIR -type d -exec chmode 775 {} \;
find $APP_DIR -type f -exec chmode 664 {} \;


