#!/bin/bash

#This is for base tag of image syneblock/quorum-master:base
sudo apt-get update
#sudo add-apt-repository ppa:jonathonf/python-3.6 -y
sudo add-apt-repository ppa:libreoffice/ppa -y
sudo apt-get update

if [ `apt list -a libreoffice | wc -l ` -eq 1 ]
    then
        echo "Installing Libreoffice"
        sudo apt install -y libreoffice
    fi

if [ `apt list -a python3.6 | wc -l` -eq 1 ]
    then 
        sudo apt install -y python3.6
    fi

if [ `apt list -a python3-pip | wc -l` -eq 1 ]
    then
        sudo apt -y install python3-pip
    fi

if [ `apt list -a tesseract-ocr | wc -l` -eq 1 ]
    then
        sudo apt install tesseract-ocr -y
    fi

if [ `apt list -a tesseract-ocr-eng | wc -l` -eq 1 ]
    then
        sudo apt install tesseract-ocr-eng -y
    fi

if [ `apt list -a pdftohtml | wc -l` -eq 1 ]
    then
        sudo apt install -y pdftohtml
    fi

if [ `apt list -a libgtk2.0-dev | wc -l` -eq 1 ]
    then
        sudo apt install -y libgtk2.0-dev
    fi

if [ `apt list -a libdb-dev | wc -l` -eq 1 ]
    then
        sudo apt install -qq -y libdb-dev libleveldb-dev libsodium-dev zlib1g-dev libtinfo-de
    fi

if [ `apt list -a build-essential | wc -l` -eq 1 ]
    then
        sudo  apt-get install -y build-essential
    fi


if [ `apt list -a software-properties-common | wc -l` -eq 1 ]
    then
        sudo apt-get install software-properties-common python-software-properties -y
    fi
#apt-get install -y wget
#apt-get install -y curl
#apt-get install -y jq
#apt-get install -y psmisc
#apt-get install -y iputils-ping
#add-apt-repository ppa:ethereum/ethereum -y
sudo apt-get update
#apt-get install solc -y
#apt-get install -y bsdmainutils
#apt-get install -y openjdk-11-jdk
#apt-get -y install maven
#apt-get -y install net-tools
pip3 install --upgrade pip
pip3 install -r requirments.txt
