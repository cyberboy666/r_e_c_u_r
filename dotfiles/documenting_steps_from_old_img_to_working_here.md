# documenting all the steps from old img of recur to working with new features

- gonna start with a `sudo raspi-update` and `sudo apt-get update -y; sudo apt-get upgrade - y`

## setup

to set up for adding things i switched the program to dev mode , connected to the wifi and git fetch from ~/r_e_c_u_r ,

## installing openframeworks and setting up conjur app

i had of10 zipped on a flashdrive already (wget errored about insecure connection when i tried to download from the pi..) , so 

- `sudo cp /media/pi/5EB5-664C/of_v0.10.0_linuxarmv6l_release.tar.gz ~/`
- `mkdir openFrameworks` and `tar vxfz of_v0.10.0_linuxarmv6l_release.tar.gz -C openFrameworks --strip-components 1`
- `cd openFrameworks/scripts/linux/debian/` &  `sudo ./install_dependencies.sh`
- and also `sudo apt-get upgrade -y; sudo apt-get update` (these took ageeees ! didnt even finish.. will come back to this)
- `make Release -C ~/openFrameworks/libs/openFrameworksCompiled/project`
- `cd ~/openFrameworks/apps/myApps/` and `git clone https://github.com/langolierz/c_o_n_j_u_r.git`
- `cd ~/openFrameworks/addons/` and `git clone https://github.com/langolierz/ofxRPiCameraVideoGrabber` (will swap this out for main once/if my edits work and get in)
- NOTE also gotta checkout the stretch branch : `git checkout stretch`
- `make ~/openFrameworks/apps/myApps/c_o_n_j_u_r


## installing packages and apps

- `sudo pip3 install Adafruit_GPIO Adafruit_MCP3008 RPi.GPIO pivideo python-osc` (tried to install threading but didnt work...)
 - (note atleast pivideo needs to be installed with sudo.), also needs `sudo pip3 install serial``
- `sudo apt-get install glslviewer`

### installing ttymidi :
- `wget http://www.varal.org/ttymidi/ttymidi.tar.gz` and `tar -zxvf ttymidi.tar.gz`
- `cd ttymidi` and `sudo nano Makefile` then add `-pthread` after -lasound ... 
- then `sudo make` then `sudo make install`

## setup:

need to delete the old settings : `rm json_objects/settings.json` and create a `Shaders` folder, 

i think will need to turn on the i2c and serial interfacing... (and maybe that serial switvhing thing .. oh and the clocking for midi serial ...  )

these amount to the following in the config:
```
dtparam=i2c_arm=on
dtparam=spi=on
enable_uart=1
```
plus this for serial midi : 
```
#setup midi over serial
dtoverlay=pi3-miniuart-bt
dtoverlay=midi-uart0
```








