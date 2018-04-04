#!/bin/bash

sudo sed -i "s/sdtv_mode=./sdtv_mode=$1/g" ~/r_e_c_u_r/dotfiles/lcd_display_drivers/LCD-show/boot/config-nomal.txt ~/r_e_c_u_r/dotfiles/lcd_display_drivers/LCD-show/boot/config-35.txt-180 /boot/config.txt
