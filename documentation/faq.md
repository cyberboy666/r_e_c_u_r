
# frequently asked questions

a place to document the questions and thoughts asked about r_e_c_u_r so far. if you have any other questions please ask them in the fb group or get in touch directly.

## what kind of lcd screens can i use for recur _display_

the cheep 3.5 lcd screen i suggest in the [build] guide is already set up (with drivers etc) to work with the card img i have shared. this is the easiest option as it will be straight plug-and-play.

however it will be possible to config some other lcd screens to work. the _video output_ uses framebuffer0 on either the hdmi or composite output (i have not heard of these outputting simultaneously ). for this reason you cannot use a lcd screen that connects via hdmi for the display. the default _display_ uses framebuffer1 over the gpio pins. any lcd screen that receives video over gpio should work with recur given the correct drivers (note: some hdmi displays still use gpio for power / touch info; these will not work as a display)

besides _gpio_ and _hdmi_ , the third option to connect a lcd display is over _dsi_ (used by official raspi display). i have not tried this and am not sure if it would (or could) work for recur. i would be keen to hear thoughts / experiments if anyone has one, or have a go at this at some point...

## can i use a pi2/pi1/pi0 for this ?

im not sure. will update here when i have a chance to try... the pi3 is the highest spec available right now, and for playing hd videos seamlessly it is already at its limit. an older model might work fine for composite but would struggle sooner with hd content. besides gpu , i think a pi2 should _run_ recur out of the box. would be keen to try recur composite playback on the pi0

## how do i connect composite out / why is my composite cable just outputting corruption ?

you will need the correct 3.5mm TRRS to RCA cable. the [correct cable] has video on fourth pole and ground on third. if your cable is outputting junk / not working it is possible you (like me) have gotten the wrong type: [my cable] had ground on the fourth pole and video on the third (most digital cameras are wired this way) i fixed this by cutting an old rca cable and swapping the ground / video around

## can i use a usb keyboard / some other usb keypad to control recur ?

yes ! the key mapping has been abstracted out to a .json file that can be edited to allow different input options. the flashed img maps the keys for the keypad i recommend (from [build] docs) to the letters a - s with the [.keymap] . the a - s keys are then assigned in the [keypad_action_mapping.json] to their corresponding actions.

if you are using a full usbkeyboard, you should be able to just press a - s keys for corresponding actions , and rearrange the letters in mapping for your own custom mapping.

you can also flatten out the FN actions and add new actions (such as shortcuts / hotkeys) to map to the extra keys. hopefully more info about this will be on the [develop page] at some point. 

## i want to edit a keymapping or do something on the pi without looking at the lcd screen

i also get sick of looking at the lil screen for developing , from the OTHER settings you can run DEV_MODE_RESET , when it reboots the hdmi is the main output and your video out should be in a smaller window.

## i keep getting a yellow lightening bolt in the upper right corner ?

this is the pi signaling it is underpowererd. running video and the lcd screen and powering a harddrive and a camera etc etc starts to add up. i havnt had any problems using a 2a supply..

## how can i access / delete files i have created using capture ?

these are saved to the user Videos folder at path : `/home/pi/Videos/recordings`

to get to these you will probably need a usb keyboard (a usb mouse can help too)

- if you are happy with command line this can be accessed by pressing ctrl+alt+f1 from keyboard (ctrl+alt+f7 will return to recur)
- if you would rather navigate from a mouse, the recur program can be exited by pressing `.` key. moving the mouse to bottom of screen should bring up raspi toolbar where filebrowser can be opened etc

### note : also you can copy videos to the `internal storage` folder inside this Videos folder if space on the sd allows

## when i use the hdmi out on my tv/projector/screen the video keeps dropping out ?

yes - this seems to be the pi responding to running out of memory when two videos are loaded at 1080 resolution on some displays. to fix this you need to change the `HDMI_MODE` setting to `CEA 4 HDMI`, this sets the pi output to 720 which should play without dropout (even playing 1080 videos)

## my video files do not show up in the browser ?

at the moment recur will filter out all files that do not have a '.mp4' (recommended), '.mkv', '.mov' or '.avi' file extension in their name. (so you can not try to map .docx, .jpeg /other obvs non-video files) ..perhaps there is a better way to tell if a file is video without reading the extension ?

## when playing short loops <=3s or manually switching players quickly sometimes the player crashes / gets stuck `LOADING` ...

hmm - this does happen sometimes. in my experience pressing the video key you want to load again then the switch key will get the video playing again. I havnt been able to create crashes that require a reset, but if you do please let me know.

## when setting the start/end points of a clip there is a small lag before starting the next cycle .. can i improve this ?

this could happen because your cycle is too short to allow the NEXT video to load before NOW has finished. making your cycle a little longer could make a difference here.

HOWEVER, i have also noticed that this lag can happen even with longer clips sometimes and i dont know why. it seems that resetting the `start` point can sometimes fix it. i wish i could figure out why this happens... if you have any insight hmu ! i feel like this could be improved if understood ! (this could be a limitation of seeking in a H264 container ... )

[correct cable]: https://www.adafruit.com/product/2881
[my cable]: https://www.aliexpress.com/item/4-poles-3-5mm-Mini-AV-Male-to-3RCA-Female-M-F-Audio-Video-Cable-Stereo/32769544207.html
[.keymap]: /dotfiles/.keymap
[keypad_action_mapping.json]: /json_objects/keypad_action_mapping.json
[develop page]: /documentation/develop_docs.md
[build]: /documentation/build_docs.md

