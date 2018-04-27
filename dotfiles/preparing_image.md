# documenting the exact steps to creating the r_e_c_u_r raspbian image

- downloaded the latest (2017-11-29 ~~2018-04-18~~) raspbian-raspbian-lite image from offical site.

- flashed it to my sd using etcher

- set up auto console login and changed keyboard layout using `sudo raspi-config`

- following the beginning of [this](https://gist.github.com/kmpm/8e535a12a45a32f6d36cf26c7c6cef51) guide,
set up wifi and run all updates: 

`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf` Add the bottom of the file
```
network={
  ssid="YOUR_SSID"
  psk="YOUR_PASSWORD"
}
```

then `sudo apt update` and `sudo apt upgrade` , sudo reboot

- i trieds to get this working without needing pixel installed (using openbox and a few other bits but the drivers for my screens didnt work like this - decided its not worth shaving that yak rn. will procede with a stripped pixel as described above:
 
 - download/install pixel + all the extra things needed for r_e_c_u_r : 
 ```
 sudo apt-get install -y raspberrypi-ui-mods git python3-tk ttf-mscorefonts-installer omxplayer libdbus-glib-1-dev python3-pip unclutter python3-picamera gpac 
 
 pip3 install dbus-python omxplayer-wrapper  mido python-rtmidi
 ```

- now can set up auto desktop login using `sudo raspi-config`

- pull down recur code into home dir ~ : `git clone https://github.com/langolierz/r_e_c_u_r.git`

- used `sudo nano ~/.config/lxsession/LXDE-pi/autostart` to add these lines : 
```
@unclutter -display :0 -idle 0 -root -noevents
@xset s off
@xset s noblank
@xset -dpms
@bash /home/pi/r_e_c_u_r/dotfiles/launcher.sh
```

and remove the line `@point-rpi` 

(im not sure exactly what each part does and if it works but is suppose to stop screensaver / hide cursor / remove on screen power warnings etc)

- i then went into pi item -> Preferences and set a black background , small task bar , no screensaver  and went into the file explorer -> Edit -> Preferences -> Volume Managment -> unchecked 'show available options for removable media ...' 

and made taskbar auto hide...

creating internal storage folder in ~/Videos

splash screen : can set a custom splash screen by setting an image at `/usr/share/plymouth/themes/pix/splash.png` , i made a copy of the original : `sudo cp /usr/share/plymouth/theme/pix/splash-old.png` and then copied my own from a flash stick...

## flashing

first remove my wifi connection !

i am trying to flash the device using the unix command `dd` on a raspberry pi.

- i want my image to not contain empty space so it can fit on smaller sd cards (4gigs)

- first check how much space is needed and name of device : `df -h`

- ~~do i need to mount the device : ??~~

couldnt figure out how to not take entire card (including empty space) , so decided to try entire 4gg card, to a usb and then try compressing in down :

- `dd if=/dev/mmcblk0 of=/media/pi/FLASH DRIVE/recur.img`
- `gzip -k recur.img` (to keep original)

going to copy and zip in one (with larger byte size) :

`sudo dd bs=4M if=/dev/mmcblk0 | gzip > /media/pi/FLASH DRIVE/r_e_c_u_r.img.gz`

## removing empty space on pi image

i had another go at this and might have had some success using [pishrink], following the instructions on readme exactly , i managed to reduce a 3.8gg image down to 2.9gg and then zipped down to 1.15gg (no saving here) , this would be more useful with larger cards though.

- the flow is using dd to copy the image from the pi to an external drive `dd if=/dev/mmcblk0 of=/media/pi/FLASH DRIVE/recur.img`

- then use pishrink to reduce this image `sudo pishrink.sh recur.img`

- then gzip to zip this : `sudo gzip recur.img`

[pishrink]:https://github.com/Drewsif/PiShrink
