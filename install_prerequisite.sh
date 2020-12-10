#!/bin/bash

#This is for base tag of image syneblock/quorum-master:base
apt-get update
add-apt-repository ppa:jonathonf/python-3.6 -y
add-apt-repository ppa:libreoffice/ppa -y
apt-get update
apt install -y libreoffice
apt-get install -y python3.6
apt-get -y install python3-pip
apt-get install tesseract-ocr -y
apt-get install tesseract-ocr-eng -y
apt-get install -y pdftohtml
apt-get install -y libgtk2.0-dev
apt-get install -qq -y libdb-dev libleveldb-dev libsodium-dev zlib1g-dev libtinfo-de
apt-get install -y build-essential
apt-get install software-properties-common python-software-properties -y
#apt-get install -y wget
#apt-get install -y curl
apt-get install -y jq
apt-get install -y psmisc
apt-get install -y iputils-ping
#add-apt-repository ppa:ethereum/ethereum -y
apt-get update
#apt-get install solc -y
#apt-get install -y bsdmainutils
#apt-get install -y openjdk-11-jdk
#apt-get -y install maven
#apt-get -y install net-tools
