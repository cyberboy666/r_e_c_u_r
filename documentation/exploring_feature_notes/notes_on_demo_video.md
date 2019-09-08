# notes on demo video

recur is quite hard to demo in general because it has three parts that need to be recorded - and synced - for it to make sense :
the _live_ , showing which buttons are pressed; the _screen_ , showing the ui - it is too hard to see from live ; and the resulting _video_ output.

since this is the second time i have tried to do this i wanted to leave some notes for futrue me - or anyone else who might want to demo similar.

## recording

i used my cellphone to record _live_ - at 720, used `recordmydesktop --no-sound` application on the raspberry pi to record the _screen_ and this time a usb3-intesity-shuttle to record _video_

the video out went through a tbc - ave5, taking the svideo out from the mixer - not sure if it made any differnece. then the huge raw files were compressed to mp4 my vlc to be edited
cellphone video was already compressed and compadiable with adobe premeire 6 where i did editing. the recordmydesktop output was ogv which i converted online - freefileconvert.com as vlc messed up the timestamp.
the colour from recordmydesktop is tinted pink which can be altered in premeire.

i synced the three channels by allining a button push that changes state of video out and screen
