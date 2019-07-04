# how to use r_e_c_u_r

## getting started

- prepare a usb with some videos you want to sample
- connect the hdmi output or composite (via [3.5mm trrs]) to the display you want to use
- power the raspberry pi. you should see red lights on the pi board, the lcd display light up and the r_e_c_u_r splash screen on your video output
- after a few moments the interface should appear on lcd screen.
- the `DSPLY` key can be used to cycle through _display_modes_

## controlling the sampler

## controls

![keys][keys]

the controls on r_e_c_u_r work by mapping `keys` to `actions`. this map can be fully customised by editing the respective json file.

the default layout uses a hard mapping for every key except the `<` - `>` - `■` in red. this means every other key triggers the same actions independent of the state r_e_c_u_r is in.

the _control keys_ ,`<` - `>` - `■` use a soft mapping. the action they trigger depends on the state , displayed on screen as `control_mode` in red.

these let you navigate and select folders, video files and settings when in `BROWSER` / `SETTINGS` mode, and by default control video playback (seek forward and back, pause/play) of the currently playing [NOW] sample in `SAMPLER` mode.

the display modes `SAMPLER`, `BROWSER` and `SETTINGS` are cycled by using the `DSPLY` key.

some actions are accessible through a _function_ layer, toggled by the `FN` key.

other controls include:

- `→` is used to switch the [NEXT] loaded sample to the [NOW] current sample
- loading the sample in slot `x` into [NEXT]; where `x` is a key from `0` to `9`
- cropping the current sample to start  (`[`) or end (`]`) at the current time
- cycling forward (`PRV BNK`) or back (`NXT BNK`) through the banks of sampleS , or clearing a bank (`CLR BNK`)
- ~~`< SPD` and `> SPD` are used to decrease and increase the speed of the currently playing clip (note not implemented yet)~~

some keys are empty to leave room for future features and user experimentation. i encourage you to modify your keymap or add custom actions you would like to use.

## parts of the lcd display

![display_image][display_image]

## `PLAYER` display

![player_example][player_example]

this section displays information about what is in the video player : the position from the start and the end of currently playing video (yellow), what slot is playing [NOW] and what slot is loaded [NEXT] 

## `SAMPLER` display mode

![sampler_example][sampler_example]

this is the main display mode for using r_e_c_u_r. from this view you can see details of all the samples loaded into the sampler. a `bank` contains 10 `slots` labelled `0` - `9`. pressing the corresponding `key` will load the `sample` in this `slot` to start when the current sample finishes. the `slot` of the currently playing sample is highlighted.

## `BROWSER` display mode

![browser_example][browser_example]

this is where you can load samples from your usb or internal Videos folder into the `SAMPLER`

- in this mode ,  the `<` and `>` keys will move the selection up and down
- folders are displayed ending in `|` for closed and `/` for open , the depth is displayed as indentation
- pressing the `■` key while a folder is selected toggles it open/closed
- pressing the `■` key while a video is selected loads it into the next available slot (note : you can see the first slot a video is loaded into on right column)

## `SETTINGS` display mode

![settings_example][settings_example]

this is where you can configure r_e_c_u_r's settings.

- navigate the menu with `<` and `>` keys like above
- pressing `■` on a setting will either cycle through it's `options` or run an `action` depending on its type

## `MESSAGE DISPLAY`

the bottom line shows the `control_mode` by default, but is also for messages:

- shows a yellow bar when _function_ layer is selected
- shows a blue bar for `INFO` messages
- shows a red bar for `ERROR` messages - full message and trace for these can be found in the log files

![message_example][message_example]

# extensions

the feature set of this project has grown beyond the simple 'seamless' video player it started out as. with more options inevitability comes more complexity and confusion. feel free to try whatever extensions interest you and ignore the rest.

## capture

live video-input is possible for `preview` and `recording`. this can be enabled in the `SETTINGS` display mode. you need to ensure the capture type is set correctly : from `piCamera`, `piCaptureSd1` or `usb`. 

- `piCamera` , which reads from raspberry pi's CSI is a performant, realiable and cheap (see build docs) way to get video input although limited to camera-feed / rescanning
- `piCaptureSd1` is a more professional solution for intergrating quality, low latency arbituary composite-video input for ras pi
- `usb` ; with this setting the raspberry pi attempts to read video from an attached usb source. intergration, quality and performance is less predictable for this but i have had success using cheap capture cards and old web cams.

with `capture` enabled in the settings you can toggle `preview` by pressing the `⦿` key. the capture input will take prioty over any video-samples playing.
pressing `FN + ⦿` will toggle record. this can be enabled with or without `preview` on. the state of capture is displayed on the `PLAYER` display between the NOW and NEXT player infomation
after a `recording` is stopped the state will be `saving..` for a moment while the raw video-footage is converted. then the sample is accessable from `video/internal_recordings/<date>-<count>.mp4` in browser. recur will also automatically map this new recording to your current bank if there is space

NOTE: for users of _piCaptureSd1_: please ensure you have the composite video source active and plugged in to the HAT __before__ powering on recur. there seems to occationally be issues with recongising the hardware otherwise and a reboot is required.

## user-inputs

the _usb-numpad_ is a convenient way to manually trigger __discrete actions__ within recur (any usb-keyboards can also be used). this is fine for basic sample loading and swtiching however more advance features benifit from __continuous control__ of parameters.
this is where alternative user-input options are needed.
(another use is to sequence recur using external gear)

### usb-midi

this is by far the easiest way to control recur externally / with continuous control. all you need is to plug in a controller into one of recurs existing usb-sockets and set`midi` to `usb` in the `SETTINGS` display mode. you should see a message with the name of your device pop up. the midi-map can be configured in the same way as key-mappings.

### i_n_c_u_r pcb

for anyone interested in a diy 'standalone' solution i designed a pcb that allows continous control via `analog input` (four knobs and four 0-5v cv inputs) + `serial-midi`. the build guide for this can be found here. they can also be enabled in the `SETTINGS` 

### shaders

(fragment) shaders are small text-files of glsl-code that tell your graphics card what to draw. these can be used to create your own colours, shapes and patterns on the screen. this is a good resource for getting started writing shaders. recur can `load` a shader in a similar way to loading a sample, and allows you to update its `parameters` in real time.

ensure that `shaders` is enabled in the settings and then use `DSPLY` to cycle to the `SHADER` display mode.
here you can navigate folders and files using `<` `>` and `■` same as `BROWSER/SETTINGS`. selecting a shader (`■`) will `load` it, and pressing `FN + 6` will toggle it on and off.

- `0-input`: these shaders use no input, everything you see is _generated_ by the code and graphics card
- `1-input`: shaders can also _process_ video. when active your current output will be passed through this shader (can be from a `video sample` or `capture preview`) this is similar to the _effects_ on your v4 mixer except now you can create, customize and share them too !
- `2-input`: allows you to perform fades, wipes and keys between two video-input sources - eg between `capture preview` and a `video sample` or even two `video samples` (notes below on how to set this up)

the shader `parameters` are best controlled by _continuous inputs_ ( see user-inputs above) however can also be set by the numpad (somewhat clumsily):
- pressing `■` on a shader will `load` it; pressing `■` on the _loaded_ shader enters `SHADER_PARAM` control mode (written in red at bottom)
- from here you can cycle through the params `[` and `]`, and change the current amount with `<`, `>`. (`FN + <` and `FN + >` change the delta)
- pressing `■` will exit `SHADER_PARAM` control mode back to `NAV_SHADER`

### loop vs parallel playing mode

[3.5mm trrs]: https://www.adafruit.com/product/2881
[display_image]: display_parts.jpg
[player_example]: player_example.jpg
[browser_example]: browser_example.jpg
[sampler_example]: sampler_example.jpg
[settings_example]: settings_example.jpg
[keys]: ./vectorfront_keys.png
[message_example]: ./message_example.jpg
