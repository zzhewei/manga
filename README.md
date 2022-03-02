# The sample of the flask
## If you want to generate requirements.txt
**pipreqs ./ --encoding=utf8 --force** 

## create a docker container by Dockerfile
**1. docker image build -t imagename .** 

**2. docker run -d -p 80:8888 --name containername imagename** 

## create docker compose by docker-compose.yml
**1. change config.py mysql setting**

**2. docker-compose up -d**

**3. docker exec -it flaskname /bin/bash**

**4. sh dbsetup.sh**