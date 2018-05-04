#!/bin/bash
sudo sed -i "s/dev\/fb1/dev\/fb0/g"  /usr/share/X11/xorg.conf.d/99-fbturbo.conf
sudo sed -i "s/dtoverlay=waveshare35a:rotate=270/##no_waveshare_overlay/g" /boot/config.txt
sudo reboot



