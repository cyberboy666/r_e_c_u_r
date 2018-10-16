# beta access , notes and limitations of v2

while at signal culture the concept of what recur could do underwent a large enough change that it will likely become v2 once im ready to release it offically in this form. however i dont know how long that will take and want it to be possible for current users to try / test / play with the new stuff before then. (warts and all !)

you can read the highlevel overview / roadmap of what v2 is about in the [signal_culture_and_future_plans] doc.

this doc will explain how to try out and use the new features, and also keep track of the known issues and my thoughts/ plans to fix them. if any testers find addational bugs i will keep track of them here.

## flashing the new img.

when i have created and uploaded the new img you can download it from here and flash to your sd card in the same way as before (note in case anyone was using a 4gg sd card before, you will need more than that now im pretty sure)

## recieving updates

with this new img recur should be exactly as usable as before in the default configuration, with the options to enable some new features if you want. (incase you are on the fence about trying it).

- a new option in the OTHER subsetting is availabe called UPDATE_CODE. this means if you are on a network (either plug in ethenet cable or connect to your home wifi) you can get any updates/bugfixes i push up. i will try to push fixes for any critical bugs asap so pls help me  find em lol

## c_a_p_t_u_r 

piCaptureSd1 compatabilty is now built in (this sets the sensor mode, autowhite balance and exposure to optimise picaptures input )to captur, you can now see a 'TYPE' option in capture subsetting which allows to switch between these settings and standand piCamera settings. also included in same menu is PICAPTURE_INPUT , which should allow software switching between differnet sources on the card.

FUTURE NOTE: if i or anyone ever wants to try with a piCaptureHd1 (or that other hdmi-to-pi board floating around) custom settings for these could be added here...

## i_n_c_u_r

### hardware

the program is now set up to read inputs from more external devices. i have been working with a little circuit that connects to the gpio pins. i hope to have a little pcb that can be attached as an option. more info about this will be available soon. here is the schematic i am using. it is just a standand midi-serial to RX , plus a MCP3008 a2d taking 4 linear pots and 4 (0-5v) cv inputs.

the GPIO pins i am using are:

- 2 -> 5v 
- 6 -> GND
- 10 -> RX
- 17 -> 3v3
- 35 -> DOUT
- 36 -> CS
- 38 -> DIN
- 40 -> CLK

NOTE: any of the 5v,3v3, GND could be used, (and infact any 4 pins for SPI too with a small code change since its using softwareSPI right now. those pins are also possible with hardwareSPI although i couldnt get this working with the lcd-driver - might investigate this further if the performance over spi becomes the bottle neck  )

i will write more about how to wire this up when/if a pcb is ready. because of the lcd-screen/picapture using the gpio header, i decided the easist way to access the pins was to solder wires from a IDE cable onto the bottom of the pi board. this wasnt so difficult even with my limited soldering skills... and then the IDE socket can be plugged in and out of the incur circuit as desired. 
 
### software

reading from the a2d can be enabled with the ANALOG_INPUT option in the OTHER subsetting. these mappings are made in the [analog_action_mapping.json], i would only have this on when using it as it will increase load etc. the response speed can be tweeked a bit from analog_input.py , although the current python archetcure does limit how fast these read. moving this to openframeworks is one way i am thinking about to improve this.

din-midi input over serial is now also an option. in the MIDI subsetting the INPUT option now cycles through usb , serial and disabled. again i would only have these listening if midi was being used. 

another new MIDI option is called CYCLE_PORT - this is kind of vague, but i noticed when attaching a midi controller over usb (a broken Edirol PCR50 for what its worth..) that three midi ports were created but only one was receiving the data from controller , and it wasnt the port recur listened to by default. if you are  trying to use a usb-midi device thats connecting but not working , it is worth trying CYCLE_PORT and see if that helps ....

## c_o_n_j_u_r

this is the biggest and least stable addition to vanilla recur. basically i wanted to experiment with replacing the OMXPLAYER backend for loading and controllingvideo playback with OPENFRAMEWORKS videoplayers (talking over OSC). 

the existing stable OMXPLAYER backend option is still avaliable and is the default. if you want to try c_o_n_j_u_r you will need to switch backends in the OTHER subsetting.

once in this mode, you can try loading and switching a sample just as before (ie press `0` , watch for `NEXT LOADED` then hit `->`), 

if the video is a box in bottom left corner OF thinks its in dev mode , selecting the OF_SCREEN_SIZE option in OTHER subsetting a few times should fix this (i just need python to  tell of when dev mode is changing - should fix soon)

most of the usual sampling fuctions should work same as before. loading , switching , pausing , rand-start etc. at this point some of the VIDEO settings such as BACKGROUND_COLOUR and SCREEN_MODE do not work here. (it is possible to implement these but low prioty for me rn...)  

it seems like sampling video through openframeworks is more demanding on cpu than omxplayer. from running some tests, my SD videos through composite out run fine but even 720 etc starts to lag (unlike omxplayer which either plays full fps or nothing , of can slow right down when its struggling ). __i would recommend using this for SD video only__

### shaders

cycling `DSPY` now also has a `SHADERS` mode. this gives a similar folder_nav view as BROWSER but is used for selecting glsl-fragment-shader files (usaully .frag). entering (`square`) on a shader file loads it (first line of  DSPLY). the loaded shader can now be toggled on and off by pressing `FN + 6` 

if a shader is marked 'gen' it will replace currently playing sample (similar to captur's preview), if it is marked 'pro' the sample will become processed through the shader.

if a shader has parameters that can be set by recur these will be displayed next to the loaded shaders name and type in SHADER display mode. (eg `x0:00 x1:78`). params are best controlled with continuos inputs (cv/pots/midi-cc) but can also be set on numpad:

- entering (`square`) on the loaded shader will change the CONTROL_MODE to SHADER_PARAM. from here a param should appear highlighted. the value of param is changed with `<` and `>` , the selected param changed with `[` and `]` and the SHADER_PARAM mode is exited with `square` (finer control could be set with a small code change...)

see [this page] for more info on writing shaders for conjur. if a shader output is white it has probably failed to link (ie glsl hasnt compiled for some reason) i hope to improve the handling of errors from openframeworks in future.

## c_o_n_j_u_r + c_a_p_t_u_r

running live input through a processing shader is an exciting possiblity once you have live input and processing shaders already. this also is responsable for aprox half my time/stress while at SC !

to process the captur input with a glsl-shader it needs to be read from openframeworks using ofxRPiCameraGrabber addon rather than the piCapture python package. for all other sampling / previewing uses i recommend using the python (default) option , (even if you are in openframeworks-backend mode, you can still capture/sample as before, and process these samples etc)

- to truely process live input you need to switch the USE_OF_CAPTURE to on, (and make sure VIDEO_BACKEND is openframeworks ) , depending on the capture state before this you might also need a soft reset (RESTART_PROGRAM in OTHER ) , now when you start capture preview it should be running through openframeworks ! any processing  shaders run now will effect this input !

- note : the sample-playback seems to be heavily impacted by of having created the capture object. this means currently if you go back to samples after starting of_capture it will likely be laggy. this is a big issue and i hope to fix it asap (releasing the capture resources when its not being used). for now a quick switch of VIDEO_BACKEND or hitting the soft RESTART_PROGRAM will fix it...



[signal_culture_and_future_plans]: /signal_culture_and_future_plans.md
[analog_action_mapping.json] : ../json_objects/analog_action_mapping.json
[this page]: https://github.com/langolierz/c_o_n_j_u_r/notes_on_shader_formats.md
