#!/bin/bash

sudo sed -i "s/dev\/fb0/dev\/fb1/g"  /usr/share/X11/xorg.conf.d/99-fbturbo.conf
sudo sed -i "s/##no_waveshare_overlay/dtoverlay=waveshare35a:rotate=270/g" /boot/config.txt
sudo reboot


