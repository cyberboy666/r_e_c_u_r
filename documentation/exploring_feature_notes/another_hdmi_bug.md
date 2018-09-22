# hdmi drop out bug

some time between when i did compatibility testing , and now - high res videos now often (and consistently cause hdmi drop outs. all 1080 do , and some 720 also) - on my hdmi-to-vga computer display. 

also (possibly related) when trying it on full hdmi projector, it drops out playing all video no matter the resolution ! whats going on ?

some research suggests that not enough power can cause this problem.
 possible fixes / things to rule out include : 
 
 - trying signal-boost in config
 - try overclocking the pi
 - try an old version of the code
 - try an old version of firmware
 - try changing some other config settings (camera mode etc)
 - try creating a new img from old img (with bare minimum) and update piece by piece until it doesnt work.
 
## results:

### vga-hdmi display

- signal boosting didnt help ,
- old version of code didnt help
- old firmware improved a little bit but didnt fix
- changing config etc didnt help
- turning off raspi2fb didnt help

### drastic measures ! :

- flashed a new sd with old raspbian from last year. only installing the minimal to play video.

- while running old code it plays better but not perfect - still drops from time to time but mostly working.
- tried installing some newer dependencies , still running old code :

didnt investigate this route any further

### solved ?

by chance i tried switching the video output to composite and back - ~~somehow after this the hdmi plays 1080 videos just fine. no idea why or when it was introduced , but i created an action to run this on startup and seems fine now. phew.~~ this didnt seems to fix it after all.

i tried setting the hdmi output to 720 instead of 1080 and from here all the videos including 1080 load and play fine. still some dropouts for 1080 video on my vga converter though...


