#!/bin/bash

source ~/.bash_profile

cd ~/team1-server
git checkout deploy
git pull origin deploy
git pull origin main
sudo cp deployment/nginx.conf /etc/nginx/nginx.conf
sudo cp deployment/sites-available/clone-linkedin.conf /etc/nginx/sites-available/clone-linkedin.conf

pyenv activate clone-linkedin
pip install -r requirements.txt

cd clone_linkedin
python manage.py migrate

python manage.py check --deploy

uwsgi --ini clone-linkedin_uwsgi.ini

sudo nginx -t

sudo service nginx restart

