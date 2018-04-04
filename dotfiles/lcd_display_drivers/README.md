# lcd display drivers

these are the drivers for the waveshare displays that work on the cheep lcd i ordered online ( [LCD-show-170703] ).

my screen only needs the LCD35-show and LCD-hdmi scripts.  a few modifications to these (espically to the boot/config.txt) have been made to allow it to work with composite video and to switch between pal and ntsc.

also some modifications might be needed to hide the boot text. i will document these changes in this file

## changes to config-35.txt-180

## changes to config-normal.txt

## changes to config-nomal.txt

- commenting out hdmi_force to allow composite output: `#hdmi_force_hotplug=1`

## changes to the cmdline.txt

`quiet splash logo.nologo plymouth.ignore-serial-consoles` for quiet boot with splash screen 

[LCD-show-170703]: www.waveshare.com/w/uplosd/0/00/LCD-show-170703.tar.gz
