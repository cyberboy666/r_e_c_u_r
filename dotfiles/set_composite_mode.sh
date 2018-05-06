#!/bin/bash
sudo sed -i "s/sdtv_mode=../sdtv_mode=$1/g" /boot/config.txt
sudo sed -i "s/sdtv_aspect=./sdtv_aspect=$2/g" /boot/config.txt
