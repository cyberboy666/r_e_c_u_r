# documenting the exact steps to creating the r_e_c_u_r raspbian image

- downloaded the latest (~~2017-11-29~~ 2018-04-18) raspbian-raspbian-lite image from offical site.

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
 sudo apt-get install -y raspberrypi-ui-mods git python3-tk omxplayer libdbus-glib-1-dev python3-pip unclutter python3-picamera gpac 
 
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

these are suppose to stop screensaver / hide cursor / remove on screen power warnings etc

- i then went into pi item -> Preferences and set a black background , small task bar , no screensaver  and went into the file explorer -> Edit -> Preferences -> Volume Managment -> unchecked 'show available options for removable media ...' 

and made taskbar auto hide...

created internal storage folder in ~/Videos

splash screen : can set a custom splash screen by setting an image at `/usr/share/plymouth/themes/pix/splash.png` , i made a copy of the original, and then copied my own from a flash stick...

## lcd display drivers

these are the drivers for the waveshare displays that work on the cheep lcd i ordered online ( [LCD-show-170703] ).

my screen only needs the LCD35-show-180 and LCD-hdmi scripts. after running both of these scripts the drivers can be deleted since the recur code then handles the switching.

## lines added to config.txt

- commenting out hdmi_force to allow composite output: `#hdmi_force_hotplug=1`

- add these lines to the config:
```
## gives more memory to the gpu for playing 1080 videos (might need to adjust this when using older pis with less memory)
gpu_mem=448
## enables the raspi camera
start_x=1
## fixes bug with playback freezing
audio_pwm_mode=0

## persisting composite settings
sdtv_mode=0
sdtv_aspect=1

## switch for enabling lcd screen (the next line is being used even if its commented out)
##no_waveshare_overlay
```

## changes to the cmdline.txt

`quiet splash logo.nologo plymouth.ignore-serial-consoles` for quiet boot with splash screen 

## flashing

first remove my wifi connection !

i will flash the device using the unix command `dd` on a raspberry pi.

- i want my image to not contain empty space so it can fit on smaller sd cards (4gigs)

- first check how much space is needed and name of device : `df -h`

- `dd if=/dev/mmcblk0 of=/media/pi/FLASH DRIVE/recur.img`
- `gzip -k recur.img` (to keep original)

going to copy and zip in one (with larger byte size) :

`sudo dd bs=4M if=/dev/mmcblk0 | gzip > /media/pi/FLASH DRIVE/r_e_c_u_r.img.gz`

## removing empty space on pi image

i had another go at this and might have had some success using [pishrink], following the instructions on readme exactly , i managed to reduce a 3.8gg image down to 2.9gg and then zipped down to 1.15gg, (this would be more useful with larger cards though).

- the flow is using dd to copy the image from the pi to an external drive `dd if=/dev/mmcblk0 of=/media/pi/FLASH DRIVE/recur.img`

- then use pishrink to reduce this image `sudo pishrink.sh recur.img` <- try without auto disk expand ?

- then gzip to zip this : `sudo gzip recur.img`

[pishrink]:https://github.com/Drewsif/PiShrink
[LCD-show-170703]: www.waveshare.com/w/uplosd/0/00/LCD-show-170703.tar.gz
