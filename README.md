 
# AOTS

## Setup postgres

This is only necessary if you want to run in production

start postgres comand line
```
sudo -u postgres psql
```

create the database, user and connect them
```
CREATE DATABASE aotsdb;
CREATE USER aotsuser WITH PASSWORD 'password';
ALTER ROLE aotsuser SET client_encoding TO 'utf8';
ALTER ROLE aotsuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE aotsuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE aotsdb TO aotsuser;
```

list all databases:
```
\l
```

connect to our database and list all tables:
```
\c aotsdb
\dt
```

to drop the database and recreate it when you want to completely reset everything (the user does not get deteled in this process):
```
DROP DATABASE aotsdb;
CREATE DATABASE aotsdb;
GRANT ALL PRIVILEGES ON DATABASE aotsdb TO aotsuser;
```

exit the psql
```
\q
```

## Instaling Django

This will install AOTS using a python virtualenv to avoid conflicts with other packages.

### 1. Prerequisits

You need the python-dev package and virtualenv
```
sudo apt-get install python-dev
pip install virtualenv
```

### 2. Create the virtual environment

Create a new virtual python environment for AOTS and activate it
```
virtualenv aotsenv
source aotsenv/bin/activate
```

if this fails with an error similar to: Error: unsupported locale setting
do:
```
export LC_ALL=C
```

### 3. Clone AOTS from github
```
git clone https://github.com/vosjo/AOTS.git
```

### 4. Install the requirements
```
cd AOTS
pip install -r requirements.txt
```

## Running AOTS localy

To run AOTS localy, using the simple sqlite database and the included server:

### 1. setup the database
```
python manage.py makemigrations users
python manage.py makemigrations stars
python manage.py makemigrations observations
python manage.py makemigrations analysis
python manage.py migrate
```

In case you want a fresh start, run:

```
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```
and drop the database or remove the db.sqlite3 file

### 2. create a admin user
```
python manage.py createsuperuser
>>> Username: admin
>>> Email address: admin@example.com
>>> Password: **********
>>> Password (again): *********
>>> Superuser created successfully.
```

### 3. start the development server
```
python manage.py runserver
```

## Running AOTS in development using a postgres database

Instructions modified from: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

### 1. change the settings.py script
```
DEBUG = False

ALLOWED_HOSTS = ['a15.astro.physik.uni-potsdam.de', '141.89.178.17', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'aotsdb',
        'USER': 'aotsuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'
```

### 2. setup the database
```
python manage.py makemigrations users
python manage.py makemigrations stars
python manage.py makemigrations observations
python manage.py makemigrations analysis
python manage.py migrate
```

In case you want a fresh start, run:

```
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```
and drop the database or remove the db.sqlite3 file

### 3. create a admin user
```
python manage.py createsuperuser
>>> Username: admin
>>> Email address: admin@example.com
>>> Password: **********
>>> Password (again): *********
>>> Superuser created successfully.
```

### 4. collect static files
```
python manage.py collectstatic
```



## setup gunicorn

### create socket

```
sudo nano /etc/systemd/system/gunicorn_aots.socket
```

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/home/aots/www/aots/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

```
sudo nano /etc/systemd/system/gunicorn_aots.service
```

```
[Unit]
Description=AOTS gunicorn daemon
Requires=gunicorn_aots.socket
After=network.target


[Service]
User=aots
Group=www-data
WorkingDirectory=/home/aots/www/aots/AOTS
ExecStart=/home/aots/www/aots/aotsenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/home/aots/www/aots/run/gunicorn.sock \
          AOTS.wsgi:application

[Install]
WantedBy=multi-user.target
```

start gunicorn and set it up to start at boot
```
sudo systemctl start gunicorn_aots.socket
sudo systemctl enable gunicorn_aots.socket
```

check status of gunicorn with and the log files with:
```
sudo systemctl status gunicorn_aots.socket
sudo journalctl -u gunicorn_aots.socket
```
check that a gunicorn.sock file is created:
```
ls /home/aots/www/aots/AOTS/AOTS/run/
>>> gunicorn.sock
```

When changes are made to the gunicorn.service file run:
```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn_aots
```

check status
```
sudo systemctl status gunicorn_aots
```

## Configure NGNIX

```
sudo nano /etc/nginx/sites-available/aots 
```

```
server {
    listen 80;
    server_name a15.astro.physik.uni-potsdam.de;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/aots/www/aots/AOTS;
    }
    
    location /media/ {
      root /home/aots/www/aots/AOTS;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/aots/www/aots/run/gunicorn.sock;
    }

}
```

Now, we can enable the file by linking it to the sites-enabled directory:
```
sudo ln -s /etc/nginx/sites-available/aots /etc/nginx/sites-enabled
```

Set the maximum body size for uploads by clients in the ngnix configuration file
```
sudo nano /etc/nginx/nginx.conf
```

add the following text in the http configuration block
```
# set client body size to 10M #
client_max_body_size 10M;
```

test for syntax errors:
```
sudo nginx -t
```

when there are no errors restart ngnix
```
sudo systemctl restart nginx
```

Finally, we need to open up our firewall to normal traffic on port 80
```
sudo ufw allow 'Nginx Full'
```
