# video input

### background

a common feature of audio samplers is the ability to 'live sample' ie have a line in to the device and use this to record a sample directly onto it - usally to be played back again imedantly as part of a performance.

from what i can tell some hardware video samplers also offer this feature. it would be interesting to explore the possiblity of this with recur. some ways to record video into recur include:

- a usb dongle / external capture card
- using a pi camera for live video or rescanning off a screen
- piCapture : a custom video card built for pi to use the pi cam protical

the first option seems fiddly and difficult / a compromise. i might be interested in trying to capture with a Blackmagic Intensity Shuttle if i get one some day...

options 2 and 3 both seem plausable, and hopefully will be interchangable once things are working (piCapture claims to act exactly like a piCam so should painless). also this allows both a cheap/hacky solution (rescanning through $2 camera) or a more professional option ($130 addation) and i can start experimenting now with a cheep cam before investing in the expensive piCapture.

i know piCam and piCapture recommend using python and there is libraries for this

### things to find out

i want to know how plausable it would be to add live sampling to my current recur stack (gpio lcd screen, omxplayer video backend).

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

[cheep cameras] for raspi can be bought from china with 5 mega pixals / recording 1080p video for around $5usd. i have borrowed a camera which i think is a night-vision version to experiment with , although should order one of these myself.

i started by reading the [picamera] python package docs. this seemed to have lots of options regarding recording video , including starting and stopping both previews and video recordings , the ability to set the resolution , framerate , shutter speed of the camera , switching preview to full screen or setting the size and position of it. 

also a bunch of parameters that might be of interest including brightness , colour effect , contrast , flips and rotations , preview alpha , saturation , sharpness. these apear to be controllable in real time while previewing or recording.

it seems like the output from the camera is raw (without frame per second meta data) h264 and to play the video back at correct speed will need a program to wrap it in an mp4 container :
```
$ sudo apt-get install gpac
...
$ MP4Box -add input.h264 output.mp4
```

the [faq] also addresses the 'can i preview to the lcd screen' question : looks like no - atleast not without copying the exact framebuffer , similar to my experiments displaying omx on the lcd screen. (this still might be possible in the world of openCv but off the table for now! - or maybe not even then - this [adafruit] tutorial talks about the limitations of displaying on a tft screen - "accelerated software will never appear on the PiTFT (it is unaccelerated framebuffer only)" ) 

### an unrelated aside : 

the [adafruit tft display] mentioned above also uses the gpios to connect to the pi - in particular it uses 5 spi pins and two standard pin outs. by cross refferencing the [raspi gpio] docs it does not use either of the rx serial pin , which would be needed if i were to receive midi directly (rather than through usb), it also leaves plenty of pins for receiving cv from a [mcp3008] through software spi for example. it is likely that my gpio lcd screen comunicates with the pi in a similar way and that i could figure out a way to connect these extentions if desired.

### research continued : piCapture





[picamera]: http://picamera.readthedocs.io/en/release-1.0/api.html
[faq]: https://picamera.readthedocs.io/en/release-1.13/faq.html
[adafruit]: https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi/easy-install-2
[adafruit tft display]: https://www.adafruit.com/product/2441
[raspi gpio]: https://www.raspberrypi.org/documentation/usage/gpio/
[mcp3008]: https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
[cheep cameras]: https://www.aliexpress.com/item/5MP-Camera-Module-Flex-Cable-Webcam-Video-1080-720p-For-Raspberry-Pi-2-3-Model-B/32860830711.html
