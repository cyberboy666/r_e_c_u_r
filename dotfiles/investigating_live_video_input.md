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

