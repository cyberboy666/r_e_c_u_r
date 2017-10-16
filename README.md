# r_e_c_u_r
a diy videolooper for py/pi

#things to do / bugs to fix:

- [ ] reload video on press is broken - the pause after load (when its not loaded in time) seems to not to work

#things iv done on a freshly flashed pi to run/dev r_e_c_u_r

- sudo apt-get install git

- git clone https://github.com/langolierz/r_e_c_u_r.git

- sudo apt-get install gedit

- change keyboard layout :  sudo raspi-config => localiation options => change keyboard layout => generic 104 => english us => english us => the default for => no compose => no then sudo reboot

(for reading video lengths :) sudo apt-get ffmpeg and pip install ffprobe
