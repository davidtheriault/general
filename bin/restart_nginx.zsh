#!/bin/zsh
# Written by David Theriault
# script to make starting / restarting
# nginx easier when otherwise
# prompted for mulitple pems

echo "enter your pem"
read -s pass
# check if nginx is already running
if [ -e /usr/local/var/run/nginx.pid ]; then
    echo "restarting nginx"
    restart_nginx.exp $pass reload 
else
    echo "starting nginx"
    restart_nginx.exp $pass start 
fi
