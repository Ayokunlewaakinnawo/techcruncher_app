# Deployment Setup

```
sudo apt-get update
```

build the docker-compose

```
docker-compose build
```

Start up the container

```
docker-compose up -d
```

inspect docker container running 

```
docker ps
docker ps -a
```

enter the techcruncher_django app container bash

```
docker exec -it Docker_container_name bash
```

make migrations and migrate

```
python manage.py makemigrations
python manage.py migrate
```

run to go live;