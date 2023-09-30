#!/bin/bash
# usage:
#   sh clean.sh image autoAnime
#   sh clean.sh image mysql
#   sh clean.sh image qB
#   sh clean.sh

docker-compose down

if [ "$1" = "image" ]; then
    if [ "$2" = "autoAnime" ]; then
        echo remove image: autoanime-autoanime:latest
        docker rmi autoanime-autoanime:latest
    elif [ "$2" = "mysql" ]; then
        echo remove image: autoanime-autoanime:latest
        docker rmi mysql:latest
    elif [ "$2" = "qB" ]; then
        echo remove image: autoanime-autoanime:latest
        docker rmi linuxserver/qbittorrent:latest
    else
        echo image name error, remove all images
        docker rmi autoanime-autoanime:latest
        docker rmi linuxserver/qbittorrent:latest
        docker rmi mysql:latest
    fi
else
    echo remove all images
    docker rmi autoanime-autoanime:latest
    docker rmi linuxserver/qbittorrent:latest
    docker rmi mysql:latest
fi

sudo rm -rf log var