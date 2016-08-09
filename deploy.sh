#!/bin/bash


echo 'to be executed inside the host machine'
sudo rsync -avz ./* /var/www/nscmr
sudo chown www-data:www-data -R /var/www/nscmr/
sudo find . -type d -exec chmod 775 {} \;
sudo find . -type f -exec chmod 664 {} \;

### obs
# should also change the conf file (indicating the correct user folder in
# python-path parameter, copy it to the apache sites-available folder and
# activate it.. (could probably do other stuff as well)
