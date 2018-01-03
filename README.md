# r_e_c_u_r
a diy videolooper for py/pi

# things to do / bugs to fix:

- [ ] ~~reload video on press is broken - the pause after load (when its not loaded in time) seems to not to work
- [ ] mkv files break coz length lookup fails-~~

# things iv done on a freshly flashed pi to run/dev r_e_c_u_r

- sudo apt-get install git

- git clone https://github.com/langolierz/r_e_c_u_r.git

- sudo apt-get install gedit

- change keyboard layout :  sudo raspi-config => localiation options => change keyboard layout => generic 104 => english us => english us => the default for => no compose => no then sudo reboot

~~(for reading video lengths :) sudo apt-get install ffmpeg and pip install ffprobe (needed a sudo apt-get update in there the second time too)~~

note that to set up the file to browser you will have to create a fle called path_to_browser.json and put in it "your/path/to/browser"

## setting up the lcd screen:

download from waveshare and follow instructions: :LCD-show-170703.tar.gz , sudo raspi-config => more options => expand filesysem. boot option => Desktop autologin.

copy driver and run 'tar xvf LCD-show-*.tar.gz', cd LCD-show/ => chmod =x LCD35-show => ./LCD35-show
