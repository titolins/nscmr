apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys \
    58118E89F3A912897C070ADBF76221572C52609D

echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > \
    /etc/apt/sources.list.d/docker.list

apt-get -qqy update

apt-get -qqy install npm apt-transport-https ca-certificates docker-engine

# works, but we are now using ssh agent forward
#su vagrant << EOF
#ssh-keygen -t rsa -b 4096 -C "tito@blinx.com.br" -P "" -f ~/.ssh/id_rsa ;
#eval $(ssh-agent /bin/bash <<< ssh-add ~/.ssh/id_rsa)
#EOF

# in case we need to use git
git config --global user.email "tito@blinx.com.br"
git config --global user.name "Tito Lins"
