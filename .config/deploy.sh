#!/usr/bin/env bash
sudo rm -rf /etc/nginx/sites-enabled/*
sudo cp -f /srv/OnlineShop/.config/nginx-app-https.conf /etc/nginx/sites-available/nginx-app.conf
sudo ln -sf /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/nginx-app.conf
sudo cp -f /srv/OnlineShop/.config/uwsgi.service /etc/systemd/system/uwsgi.service

sudo systemctl daemon-reload
sudo systemctl enable uwsgi
sudo systemctl restart uwsgi nginx
sudo systemctl status uwsgi nginx --no-pager