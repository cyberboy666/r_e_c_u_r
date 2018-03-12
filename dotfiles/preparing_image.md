# documenting the exact steps to creating the r_e_c_u_r raspbian image

- downloaded the latest (2017-11-29) raspbian-raspbian-lite image from offical site.

- flashed it to my sd using etcher

- set up auto console login and changed keyboard layout using `sudo raspi-config`

- following the beginning of [this](https://gist.github.com/kmpm/8e535a12a45a32f6d36cf26c7c6cef51) guide,
set up wifi and ran all updates

- since im trying to run this as light as possible , i dont think i need pixel installed for tkinter to work
according to [this](https://die-antwort.eu/techblog/2017-12-setup-raspberry-pi-for-kiosk-mode/) link all we
need is a x server and window manager. install these as per the kiosk-mode guide

- install git `sudo apt-get install git`

- install the dbus wrapper : `apt-get install libdbus-glib-1-dev` and and `apt-get install python3-pip`
and `pip3 install dbus-python`

install tkinter : `sudo apt-get install python3-tk`

- pull down recur code : `git clone https://github.com/langolierz/r_e_c_u_r.git`

- i also installing xterm `sudo apt-get install xterm` for debugging perposes.. dont think it will be needed
on finished image...

- installing udisk-glue for mounting usb as described [here](https://jmeosbn.github.io/blog/minimal-raspbian-pi/#configure-automount-for-usb-drives)
: `apt-get install udisks-glue policykit-1` and `sed -i '/^match disks /a\    automount = true' /etc/udisks-glue.conf`
now just need to start it on boot
