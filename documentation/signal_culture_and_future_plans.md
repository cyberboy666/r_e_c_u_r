
# signal culture + future plans

this is an update on the progress and new ideas as a direct result of my residency at signal culture (sept-oct 2018) and an outline of some of my future plans with this project

the initial hack that became recur was in response to a specific hole in my video-hardware workflow (~dec2017). the encouragement and enthusiasm for the idea on VideoCircuits was enough to motivate me to tidy and share recur_v1 on github/fb (may2018). a dozen or so people building this and talking about it was satisfying but i had no immediate plans to continue developing for it, besides maintenance, bugfixes, simple user requests etc...

however after being invited to a 3-week toolmaker residency in Owego NY i felt encouraged and enabled to explore some bigger new ideas for the instrument.

the name __r_e_c_u_r__ refers to the video sampling/looping feature at the core of this device. as the scope of what it can do is expanded, naming and organizing the (optional) extensions helps define their use.

## c_a_p_t_u_r

_an optional extension for live sampling through the pi camera input_

this was partially included in v1 although limited to inputs from the rpi-camera. while at SC i had the chance to try it with a piCaptureSd1 hat which allows sd video input from composite, component and svideo. some settings have been added to improve the captur image.

- TODO : experiment with capture from usb-webcam and cheep usb capure cards. with prob be lowfi and or laggy but also still fun.

## c_o_n_j_u_r

_an alternative openframeworks backend for extended video control and glsl-shader integration_

this is the largest addition from the v1 release. although omxplayer is a gpu-accelerated videoplayer that is stable and forgiving it is designed as a mediaplayer for watching films etc, not as a platform for creative coding. r_e_c_u_r can sequence omxplayer to playback samples exactly how they are (and seek etc for sublooping) .

openframeworks is more suited for video manipulation and opens a lot of possibilities to how the samples can be played.

### shaders

a few other projects have been based around using a raspberry pi as a visual instrument in another way - instead of focusing on video-clip playback, these play glsl-shaders, fragments of code that run directly on the gpu, allowing the creation of interesting digital visual generation.

although generated in real time, shader-playback is similar to video playback in that you can select a prepared source (video-file or shader-code) and perform with it - trigger when to start and stop, interact with parameters live (video start/stop/alpha/position or user defined shader parameters).

recur already has the ui to browse folders and files, select and map them, to display the relevant infomation, and openframeworks has the ability to load and play shaders much like you would load and play videos. this seemed like a logical and powerful extension to the sampler core.

## i_n_c_u_r

_become subject to (something unwelcome or unpleasant) as a result of one's own behavior or actions_

this is related to extending recurs sequencing/performability by exposing its controls to external manipulation.

usb-midi control over recur actions was in the v1 release including the first example of continuos inputs via midi-cc. this gives control over parameters which otherwise are difficult to interact with on a numpad alone (video/preview alpha). as the amount of control increases so does the need for continuous inputs.

at SC i created a circuit that allows 8 analog inputs (4 pots, 4 0-5v cv) and serial(din)-midi into recur.

## modulation

having defined these different areas of the __r_e_c_u_r__ video instrument, we also have created some powerful combinations (some are trivial/obvious like _i_n_c_u_r_ + _r_e_c_u_r_ for external sequencing of video samples, or _c_a_p_t_u_r_ + _r_e_c_u_r_ for recording live input directly followed by sampling it) others include:

- _i_n_c_u_r_ + _c_o_n_j_u_r_ : shaders can be written to respond in real time based on user input. usually this is in the form of the mouse-x&y position. for recur i have defined normalized parameter inputs that can be used to manipulate any portion of the glsl code. having knobs or cv control over these parameters greatly increases the playablity of the shaders.

- _r_e_c_u_r_ + _c_o_n_j_u_r_ : at first i was thinking of video-files and glsl-shaders as separate sources for creating video. however then i discovered how you can also _use_ a glsl-shader to process a video-file (shaders can take textures as input, one of which can be a video), leading me to make the distinction in recur between _0-input shaders_ and _1-input shaders_ .

- c_a_p_t_u_r_ + _c_o_n_j_u_r_ : not only can _1-input shaders_ accept video as a texture-input, they can also take texture from a live input (a camera or capture card for example). this means recur can also be used to process live video input in (almost) real time.

## direction

what started as a simple solution for seamless prerecorded video playback is starting to look something closer to the video equivalent to audios groovebox - where a (good) groovebox may include sampling, sequencing, synth-presets, audio-effects and live-input/effect-through , this new __r_e_c_u_r__ + _i_n_c_u_r_ + _c_o_n_j_u_r_ + _c_a_p_t_u_r_ may come close to a fully open, customizable and diy digital video groovebox.

## future plans

much of what is outlined above is in varying stages of development. proofs of concepts have been completed, but lots of the new (esp openframework) code is buggy and needs tidying and testing. for example my incur circuit is thrown together on perf-board and soldered straight to the pi...

here are some things im thinking about doing/trying from here:

- get this messy web of features polished enough that its worth creating a new sd img so others can flash and try these software updates out (im including a switch between omxplayer backend to retain existing functionality, and the option to try and test the more experimental openframeworks backend )
- investigate sending external control (midi + analog readings) straight to openframeworks rather than python. this probably involves sacrificing some of the customizablity of mapping any input to any action for a performance increase (as it is i doubt my python code is fast enough to respond to eurorack without noticeable stepping...)
- create another video demo to show these new aspects
- create a new physical version : this time using a raspi compute board on a custom pcb for eurorack standard with cv/trigger in circuits , faceplate and using the numpad detached via wifi (probably 20hp)
- hopefully have the software running stable enough and a buildpipe thats slightly more optimized than 'wait 9 hours for the case to print' so that small assembled runs become feasible for getting these to non-diy-ers
- investigate the feasibility of creating even more accessible stripped version (composite only?) on the raspi0 (probably not feasible but iv been constantly surprized at what gpu accelerated sbc's can do!)
- collaborate on creating some workshops for: _intro to video hardware instruments : some hacky open diy projects_ ...
