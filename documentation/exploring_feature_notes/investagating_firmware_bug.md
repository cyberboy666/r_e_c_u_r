## firmware bug

at some point i must have updated the raspi firmware. this caused the recur application to present a bug that makes it basically unusable:

### the bug

the video freezes / lags often , usually at the same spot : 10s in, 2minutes in etc. when a video is reload (ie another video player created underneath current one) the current video usually freezes.

### investigation

- i tried checking out an old version of recur code to rule out a change on my code causing it. this still behaves the same way

- i created a new version of recur from the newest (april) version of stretch. this also displays the bug.

- finally i created a new version of recur from the older version (november) and made sure to not install any of the new packages (midi / capture). this worked without the bug on an old version of the code ! wahoo. i now tried installing those new packages and running the update code. still working !

- next i created an image of this working recur. (known issues with the image so far : screen saver is on, our home wifi is included)

- the firmware that is working is `uname -a : Linux raspberrypi 4.9 59-v7+ #1047 SMP Sun Oct 29 ...`

- next i will try a `sudo apt update` and `sudo apt upgrade` to rule out a package update causing the bug - can confirm its still working after apt upgrades ! must be the firmware :

- the gpu firmware (not sure the exact dif..) is obtained from `sudo /opt/vc/bin/vcgencmd version` and is `Oct 24 2017 .. a3d7660e6749e75e2c4ce4d377846abd3b3be283 (clean) (release) `

the new firmware says its : `754029b1cb414a17dbd786ba5bee4fc936332255` which is what i started typing into `sudo rpi-update 754029b`

now `uname -a` reads `.. 4.9.60-v7+ #1048 .. Fri Nov 3` and the player still works. `sudo /opt/vc/bin/vcgencmd version` says `Nov 3 .. 1bcf9152... (clean) (release)`

pushed forward to v 4.14.20 which failed. pushing back: did this a few times. got it working on 4.9.78 but failing on 4.9.80. looks like it might be this issue : https://www.raspberrypi.org/forums/viewtopic.php?t=195178 - just need to figure out how to turn it off for testing

found it ! i have the latest firmware version and by adding `audio_pwm_mode=0` to the config it now plays as before . phew what a relief ! 

gonna create new version of the image with this fixed , the wifi removed and the screensaver disabled.
