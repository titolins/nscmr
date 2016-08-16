apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys \
    58118E89F3A912897C070ADBF76221572C52609D

echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > \
    /etc/apt/sources.list.d/docker.list
echo "deb http://repo.mongodb.org/apt/debian wheezy/mongodb-org/3.2 main" \
    > /etc/apt/sources.list.d/mongodb-org-3.2.list

apt-get -qqy update

apt-get -qqy install npm apt-transport-https ca-certificates docker-engine \
    git make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils libjpeg-dev mongodb-org ruby

gem install sass

# install pyenv and pip so we may use the dev server if needed
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
exec $SHELL
pyenv install 3.4.5
pyenv global 3.4.5

# works, but we are now using ssh agent forward
#su vagrant << EOF
#ssh-keygen -t rsa -b 4096 -C "tito@blinx.com.br" -P "" -f ~/.ssh/id_rsa ;
#eval $(ssh-agent /bin/bash <<< ssh-add ~/.ssh/id_rsa)
#EOF

