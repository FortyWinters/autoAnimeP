#!/bin/bash

# sudo usermod -aG docker $USER

mkdir -p var/qBittorrent/config
mkdir -p var/qBittorrent/download
mkdir -p var/mysql/data
mkdir -p var/mysql/config

mkdir -p var/autoAnime/config_file
mkdir -p var/autoAnime/src

cp config_file/my.cnf var/mysql/config/my.cnf
cp config_file/init.sql var/mysql/init.sql

# docker-compose up -d