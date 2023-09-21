#!/bin/bash

# sudo usermod -aG docker $USER

mkdir -p docker/qBittorrent/config
mkdir -p docker/qBittorrent/download
mkdir -p docker/mysql/data
mkdir -p docker/mysql/config

cp config_file/my.cnf docker/mysql/config/my.cnf
cp init.sql docker/mysql/init.sql

docker-compose up -d