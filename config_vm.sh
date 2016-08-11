apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927

echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" \
    | tee /etc/apt/sources.list.d/mongodb-org-3.2.list

apt-get -qqy update

apt-get -qqy install git python3.4 python3-pip apache2 \
    libapache2-mod-wsgi-py3 mongodb-org make build-essential libssl-dev \
    zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncurses5-dev libncursesw5-dev xz-utils

usermod -a -G www-data vagrant

rm -rf /var/www
ln -sf /vagrant /var/www

# works, but we are now using ssh agent forward
#su vagrant << EOF
#ssh-keygen -t rsa -b 4096 -C "tito@blinx.com.br" -P "" -f ~/.ssh/id_rsa ;
#eval $(ssh-agent /bin/bash <<< ssh-add ~/.ssh/id_rsa)
#EOF
