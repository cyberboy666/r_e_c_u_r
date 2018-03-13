# documenting the exact steps to creating the r_e_c_u_r raspbian image

- downloaded the latest (2017-11-29) raspbian-raspbian-lite image from offical site.

- flashed it to my sd using etcher

- set up auto console login and changed keyboard layout using `sudo raspi-config`

- following the beginning of [this](https://gist.github.com/kmpm/8e535a12a45a32f6d36cf26c7c6cef51) guide,
set up wifi and ran all updates: 

`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf` Add the bottom of the file
```
network={
  ssid="YOUR_SSID"
  psk="YOUR_PASSWORD"
}
```

then `sudo apt update` and `sudo apt upgrade`

- since im trying to run this as light as possible , i dont think i need pixel installed for tkinter to work
according to [this](https://die-antwort.eu/techblog/2017-12-setup-raspberry-pi-for-kiosk-mode/) link all we
need is a x server and window manager. ~~install these as per the kiosk-mode guide: 
`sudo apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox`~~
 UPDATE : seems my screen drivers dont work with openbox out of the box - i dont think its worth taking rabbithole just to save some space / load time. will procede with pixel as described above:
 `sudo apt-get install -y raspberrypi-ui-mods`
 
- install git `sudo apt-get install git`

- install the dbus wrapper and its prereqs : `sudo apt-get install libdbus-glib-1-dev` and `sudo apt-get install python3-pip`
and `pip3 install dbus-python` and `pip3 install omxplayer-wrapper`

- install tkinter : `sudo apt-get install python3-tk`

- install omx `sudo apt-get install omxplayer`

- pull down recur code : `git clone https://github.com/langolierz/r_e_c_u_r.git`

- should come with pixel ~~i also installing xterm `sudo apt-get install xterm` for debugging perposes.. dont think it will be needed
on finished image...~~

- ~~installing udisk-glue for mounting usb as described [here](https://jmeosbn.github.io/blog/minimal-raspbian-pi/#configure-automount-for-usb-drives)
: `sudo apt-get install udisks-glue policykit-1` and ` sudo sed -i '/^match disks /a\    automount = true' /etc/udisks-glue.conf`
now just need to start it on boot by adding it to ~/.bash_profile with along with startx :
`sudo nano ~/.bash_profile` and add lines `sudo -u pi udisks-glue` and 
`[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && startx -- -nocursor`~~

- ~~now launch r_e_c_u_r when openbox starts : `sudo nano /etc/xdg/openbox/autostart` and add
```
xset s off &
xset s noblank &
bash /home/pi/r_e_c_u_r/dotfiles/launcher.sh &
```
~~

