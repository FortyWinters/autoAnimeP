#!/bin/bash

docker-compose down

sudo rm -rf log var

docker rmi autoanime-autoanime:latest
docker rmi linuxserver/qbittorrent:latest
docker rmi mysql:latest