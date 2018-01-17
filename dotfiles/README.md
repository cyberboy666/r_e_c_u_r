# setting up default keyboard layout (optional)

 sudo raspi-config => localiation options => change keyboard layout => generic 104 => english us => english us => the default for => no compose => no then sudo reboot

# Installing packages needed

- sudo apt-get install git
- git clone https://github.com/langolierz/r_e_c_u_r.git
- (omx-python-wrapper)
- sudo apt-get install gedit (optional for editing)

# Key Mapping
key remappings were achieved using the program `xmodmap`, and the most helpful post we found for that was [this stackexchange](https://raspberrypi.stackexchange.com/questions/32085/how-to-remap-caps-lock-to-esc)
you can find the current keymappings using `xmodmap -pke` and for the specifically numpad related keymappings use:

    xmodmap -pke | grep KP > defaultKeymap
    xmodmap -pke | grep Nu >> defaultKeymap

which prints only the default numpad keys to a file for reference later.
keys can be manually remapped using `xmodmap -e "keycode 82=a" for testing.

In order to have the custom keymap work on startup we have added the line `xmodmap ~/r_e_c_u_r/dotfiles/.remap` to the launcher script.

where the file `.remap` has a list of the keycodes that you want to include.

# Start r_e_c_u_r on login/boot

We wanted to set things up to autostart after xdg got going, there are a number of ways of tackling this, mentioned [here](https://www.raspberrypi-spy.co.uk/2014/05/how-to-autostart-apps-in-rasbian-lxde-desktop/).

we ended up using method 2 from that page, which is _user specific_ (ie. if you make more users on your pi you have to repeat this process) and involves editing the autostart config file:

    sudo nano ~/.config/lxsession/LXDE-pi/autostart

and adding the following line to the bottom of the file:

    @bash /home/pi/r_e_c_u_r/dotfiles/launchscript.sh

# setting up driver for cheap 3.5" lcd screen

- first expand your file system : sudo raspi-config => more options => expand filesysem. boot option => Desktop autologin.

- the download and unzip (`tar xvf LCD-show-*.tar.gz`) the [waveshare driver](http://www.waveshare.com/w/upload/0/00/LCD-show-170703.tar.gz) into your `home/pi` dir

- now run scripts in `~/r_e_c_u_r/dotfiles` to switch between LCD display and hdmi output

# hiding boot text

i followed some instructions in top answer [here](https://raspberrypi.stackexchange.com/questions/59310/remove-boot-messages-all-text-in-jessie) - this is a work in progress
