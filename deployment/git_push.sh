#!/bin/bash

source ~/.bash_profile

cd ~/team1-server
sudo cp /etc/nginx/nginx.conf deployment/nginx.conf
sudo cp /etc/nginx/sites-available/clone-linkedin.conf deployment/sites-available/clone-linkedin.conf

git add *

