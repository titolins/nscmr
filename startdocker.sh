#!/bin/bash

docker run -v dbdata:/var/lib/mongodb -v $SSH_AUTH_SOCK:/ssh-agent --env \
    SSH_AUTH_SOCK=/ssh-agent -d -p 80:80 --name nscmr nscmr

docker exec -it nscmr service mongod start

sudo docker exec -it nscmr rm -rf /app/nscmr/static/.webassets-cache

