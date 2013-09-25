#!/bin/bash

# This should be called from /etc/rc.local (that way it has sudo permission)

# Restart the server process
nohup sudo node /home/sean/Websites/FernoTunes/Server/server.js > /home/sean/nohup/FernoTunes.out &