# The Heaven
## generate requirements.txt
**pipreqs ./ --encoding=utf8 --force** 

## create a docker container by Dockerfile
**1. docker image build -t imagename .** 

**2. docker run -d -p 80:8888 --name containername imagename** 

## create docker compose by docker-compose.yml
**1. change config.py mysql setting**

**2. docker-compose up -d**

**3. docker exec -it flaskname /bin/bash**

**4. sh dbsetup.sh**

##i18n modify the language
**1. if not folder enter "pybabel init -i messages.pot -d translations -l lan" to init**

**2. generate messages.pot "pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot ."**

**3. translation the messages.po file**

**4. pybabel compile -d translations**