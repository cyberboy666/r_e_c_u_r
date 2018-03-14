# documenting the exact steps to creating the r_e_c_u_r raspbian image

- downloaded the latest (2017-11-29) raspbian-raspbian-lite image from offical site.

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
 sudo apt-get install -y raspberrypi-ui-mods git python3-tk ttf-mscorefonts-installer omxplayer libdbus-glib-1-dev dbus-python python3-pip
 
 pip3 install dbus-python omxplayer-wrapper
 ```

- pull down recur code : `git clone https://github.com/langolierz/r_e_c_u_r.git`

- used `sudo nano ~/.config/lxsession/LXDE-pi/autostart` to add these lines : 
```
@unclutter -display :0 -d -idle 3 -root -noevents
@xset s off
@xset s noblank
@xset -dpms
@bash /home/pi/r_e_c_u_r/dotfiles/launcher.sh
```
(im not sure exactly what each part does and if it works but is suppose to stop screensaver / hide cursor / remove on screen power warnings etc)

- i then went into pi item -> Preferences and set a black background , small task bar , no screensaver  and went into the file explorer -> Edit -> Preferences -> Volume Managment -> unchecked 'show available options for removable media ...' 
