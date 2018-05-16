# video input

### background

a common feature of audio samplers is the ability to 'live sample' ie have a line in to the device and use this to record a sample directly onto it - usually to be played back again immediately  as part of a performance.

from what i can tell some hardware video samplers also offer this feature. it would be interesting to explore the possibility of this with recur. some ways to record video into recur include:

- a usb dongle / external capture card
- using a pi camera for live video or rescanning off a screen
- piCapture : a custom video card built for pi to use the pi cam protocol

the first option seems fiddly and difficult / a compromise. i might be interested in trying to capture with a Blackmagic Intensity Shuttle if i get one some day...

options 2 and 3 both seem plausible, and hopefully will be interchangeable once things are working (piCapture claims to act exactly like a piCam so should painless). also this allows both a cheap/hacky solution (rescanning through $2 camera) or a more professional option ($130 addition) and i can start experimenting now with a cheep cam before investing in the expensive piCapture.

i know piCam and piCapture recommend using python and there is libraries for this

### things to find out

i want to know how plausible it would be to add live sampling to my current recur stack (gpio lcd screen, omxplayer video backend).

some things i want know are:

- how to set up the piCam on raspberry pi
- how to record the input from the piCam onto the pi
- will these files play back in omx/recur
- can you preview the stream on the hdmi/composite output ?
- can you preview the stream on the lcd display ? 
- can this preview be adjusted / resized etc ?
- can you adjust params of camera ? in real time ? framerate , brightness , contrast , zoom etc ? 
- how does rescanning look ?
- how could i control piCaptures additional params ?
- is there any reason to think piCapture wouldnt be interchangable with a working piCam feature ?

### research

[cheep cameras] for raspi can be bought from china with 5 mega pixels / recording 1080p video for around $5usd. i have borrowed a camera ~~which i think is a night-vision version~~ to experiment with , although should order one of these myself.

i started by reading the [picamera] python package docs. this seemed to have lots of options regarding recording video , including starting and stopping both previews and video recordings , the ability to set the resolution , framerate , shutter speed of the camera , switching preview to full screen or setting the size and position of it. 

also a bunch of parameters that might be of interest including brightness , colour effect , contrast , flips and rotations , preview alpha , saturation , sharpness. these apear to be controllable in real time while previewing or recording.

it seems like the output from the camera is raw (without frame per second meta data) h264 and to play the video back at correct speed will need a program to wrap it in an mp4 container :
```
$ sudo apt-get install gpac
...
$ MP4Box -add input.h264 output.mp4
```

the [faq] also addresses the 'can i preview to the lcd screen' question : looks like no - at least not without copying the exact framebuffer , similar to my experiments displaying omx on the lcd screen. (this still might be possible in the world of openCv but off the table for now! - or maybe not even then - this [adafruit] tutorial talks about the limitations of displaying on a tft screen - "accelerated software will never appear on the PiTFT (it is unaccelerated framebuffer only)" ) 



### research continued : piCapture

[picapture] is a video capture card designed for the raspberry pi to emulate the piCamera and take advantage of the pi's hardware acceleration. it comes as a 'hat' that also uses ic2 (or serial)
to communicate. there is a python package to access these additional options. 

these come in two types :

- standard def - composite and s-video in , $139usd
- hi def - hdmi and component in $159usd

im not sure which one i would like to try, but they sound cool ! would need to check the pins dont clash with the display but i think these should work together nicely !

### getting started with piCamera

following the picamera docs , i will/have :

- plugged in the camera
- turned on camera in the config
- tried take an image
- installed package with `sudo apt-get install python3-picamera`
- run `sudo apt-get update` and  `sudo apt-get upgrade` (for firmware)
- trying some simple python commands with camera
- write some experimental recur code

first hitch : i enabled the camera in the raspi-config , but it seems like the switching screens driver overrides this , ~~so will have to update this too !~~ fixed this by adding a line to the config.txt

besides that the preview / different parameters and effects work as expected. next step is to try recording something , converting it to mp4 and playing back on omxplayer.

i have installed `sudo apt-get install gpac` and am using `subprocess.Popen` to run the `MP4Box` command from inside python. this way i can poll back into it and map the video only when its finished converting to stop blocking in the meantime. i also updated the display to show when the camera is previewing and recording. this all worked smoother than i expected.

i also made a (surprisingly small) change to the browser to show the pi's videos folder next to the external devices. this will be useful for using the recordings saved and for copying files onto recurs disk. (the copying feature has been de-prioritized since it can be done manually with mouse/keyboard and could be risky / might want a confirmation window ...)

another thing still to think about is how to protect from overfilling the sd card / external storage. 
- i have done this by checking before starting to record and every 10 seconds during recording if the disk space is under 10mb in which case it warns and stops the recording.

also displaying info when camera is not attached and catching other types of errors... 
- this will be handled by  bool enabling the capture. if it can not detect the camera it will not allow this to be enabled.

[picamera]: http://picamera.readthedocs.io/en/release-1.0/api.html
[faq]: https://picamera.readthedocs.io/en/release-1.13/faq.html
[adafruit]: https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi/easy-install-2

[cheep cameras]: https://www.aliexpress.com/item/5MP-Camera-Module-Flex-Cable-Webcam-Video-1080-720p-For-Raspberry-Pi-2-3-Model-B/32860830711.html
[picapture]: https://lintestsystems.com/products/picapture-sd1
