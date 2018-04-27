## firmware bug

at some point i must have updated the raspi firmware. this caused the recur application to present a bug that makes it basicly unusable:

### the bug

the video freezes / lags often , usually at the same spot : 10s in, 2minutes in etc. when a video is reload (ie another video player created underneath current one) the current video usually freezes.

### investigation

- i tried checking out an old version of recur code to rule out a change on my code causing it. this still behaves the same way

- i created a new version of recur from the newest (april) version of stretch. this also displays the bug.

- finally i created a new version of recur from the older vesrion (november) and made sure to not install any of the new packages (midi / capture). this worked without the bug on an old version of the code ! wahoo. i now tried installing those new packages and running the update code. still working !

- next i created an image of this working recur. (known issues with the image so far : screen saver is on, our home wifi is included)

- the firmware that is working is `Linux raspberrypi 4.9 59-v7+ #1047 SMP Sun Oct 29 ...`

- next i will try a `sudo apt update` and `sudo apt upgrade` to rule out a package update causing the bug
