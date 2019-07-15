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

<details>
<summary>capture</summary>  

## capture

live video-input is possible for _previewing_ and _recording_. this can be enabled in the `SETTINGS` display mode. you need to ensure the capture type is set correctly : choose from `piCamera`, `piCaptureSd1` or `usb`. 

- `piCamera` , which reads from raspberry pi's CSI is a performant, realiable and cheap (see build docs) way to get video input into recur - note: limited to camera / rescanning
- `piCaptureSd1` is a more professional solution for intergrating quality, low latency composite-video input for raspi
- `usb` ; with this setting the recur attempts to read video from an attached usb source. intergration, quality and performance is less predictable but i have tried it using cheap capture cards and old web cams.

with `capture` enabled in the settings you can toggle _preview_ by pressing the `⦿` key. the capture input will take prioty over any video-samples playing.
pressing `FN + ⦿` will toggle sample recording. this can be enabled with or without `preview` on. the state of capture is displayed on the `PLAYER` display between the NOW and NEXT player infomation.
after a `recording` is stopped the displayed state will be `saving..` while the raw video-footage is converted. after this the sample can be loaded from `video/internal_recordings/<date>-<count>.mp4` in _browser_. recur will automatically map new recordings to your current bank if there is space

NOTE: for users of _piCaptureSd1_: please ensure you have the composite video source active and plugged in to the HAT __before__ powering on recur. there seems to occationally be issues with recongising the hardware otherwise and a reboot is required.
</details>

<details>
<summary>user-inputs</summary>
  
## user-inputs

the _usb-numpad_ is a convenient way to manually trigger __discrete actions__ within recur (any usb-keyboards can also be used). this is fine for basic sample loading and switching however more advance features benifit from __continuous control__ of parameters.
this is where alternative user-input options are useful.
(another use is to sequence recur using external gear)

### usb-midi

this is by far the easiest way to control recur externally / with continuous control. plug a controller into one of recurs existing usb-sockets and set _midi_ to __usb__ in the `SETTINGS` display mode. you should see a message with the name of your device pop up. the midi-map can be configured in the same way as key-mappings.

### i_n_c_u_r pcb

for anyone interested in a diy 'standalone' solution i designed a pcb that allows continous control via `analog input` (four knobs and four 0-5v cv inputs) + `serial-midi`. the build guide for this can be found here. they can also be enabled in the `SETTINGS` 
</details>

<details>
<summary>shaders</summary>
  
## shaders

(fragment) shaders are small text-files of glsl-code that tell your graphics card what to draw. these can be used to create your own colours, shapes and patterns on the screen. this is a good resource for getting started writing shaders. recur can `load` a shader in a similar way to loading a sample, and allows you to update its `parameters` in real time.

ensure that `shaders` is enabled in the settings and then use `DSPLY` to cycle to the `SHADER` display mode.
here you can navigate folders and files using `<` `>` and `■` same as `BROWSER/SETTINGS`. selecting a shader (`■`) will `load` it, and pressing `FN + 6` will toggle it on and off.

- `0-input`: these shaders use no input, everything you see is _generated_ by the code and graphics card
- `1-input`: shaders can also _process_ video. when active your current output will be passed through this shader (either from a `video sample` or `capture preview`) this is similar to the _effects_ section on a v4 mixer except now you can create, customize and share them too !
- `2-input`: allows you to perform fades, wipes and keys between two video-input sources - eg between `capture preview` and a `video sample` or two `video samples` (see notes below on how to set this up)

the shader `parameters` are best controlled by _continuous inputs_ ( see user-inputs above) however can also be set by the numpad (somewhat clumsily):
- pressing `■` on a shader will `load` it; pressing `■` on the _loaded_ shader enters `SHADER_PARAM` control mode (written in red at bottom)
- from here you can cycle through the params `[` and `]`, and change the current amount with `<`, `>`. (`FN + <` and `FN + >` change the delta)
- pressing `■` will exit `SHADER_PARAM` control mode back to `NAV_SHADER`
</details>

<details>
<summary>loop vs parallel playing mode</summary>
  
## loop vs parallel playing mode

recur was created to try loop videos seamlessly. it does this by using two video-players and preloading the `NEXT` player while the `NOW` is playing. this is most useful for short samples where a few frames every loop is very noticable. however there are some situations where this is not so important: for example when working with long samples, or when a 1080p video loaded twice maxes out the pi's memory. if you do not require the seamless _switch_ there is now an option `LOOP_TYPE` to choose between _loop_  and _parallel_ .

- `loop` is the default behaviour described above
- `parallel` : in this mode when the current player finishes it takes a moment to load the next sample itself. there is no `SWITCH` action and pressing a `SLOT` key will start loading the corrosponding sample into this player.

introducing __parallel__ mode also allows the possiblity of having two differnet samples playing at the same time (using roughly the same amount of memory as one in _loop_ mode). to access the second (`NEXT`) player press `FN + ->` (player switch). you can tell which player is selected by the colour of the player bar - yellow for now, cyan for next. with _next_ player selected you can load, seek, toggle_pause the same as normal. pressing the `->` key now will 'switch' which player is displaying. (`FN + ■` can manually toggle_show for the current player)

other forms of _mixing_ between the two players can be done using the `2-input` shaders mentioned above.
</details>

<details>
<summary>detour demo (frame-sampling) </summary>
  
## detour demo

d_e_t_o_u_r is a frame-sampler created to address some limitations of sampling with video-files (eg very short loops, instant switching, varying speed and direction). although conceived as a standalone instrument i also wanted (brave) recur users to be able to test it. this is a rough integration with basic (and confusing) ui and crashes (a `RESET_OPENFRAMEWORKS` should recover these) use at your own risk !

to use detour_demo you must have continuous controls (either midi or i_n_c_u_r pcb). after enabling it in the settings you can cycle to __FRAME_SAMPLER__ with `DSPLY` key. information about the state of the program is displayed here.

a __detour__ is an array of frames (imagine pictures in a flip-book). the __mix-shader__ combines sampler-input (output from recur : can be a video sample playing or capture preview) with the current frame from _detour_.

from the __FRAME_SAMPLER__ display:
- pressing `FN + 7` will toggle __FRAME_SAMPLER__ mode on and off
- pressing `■` will _toggle_play_ on the current_detour
- pressing `->` will _toggle_record_ ; this adds the output of _mix-shader_ into the current_detour
- pressing `FN + ->` will _toggle_record_loop_ ; this switches from adding by increasing the size of current_detour _or_ overwriting an existing frame in it
- pressing `0, 1, 2, 3` will switch between different detours. for this demo the total number of frames can not exceed 500
- you can select the _mix-shader_ type with `[` and `]` (it reads from your `2-input` folder)
- `a1` (analog input 1) will mix between the _sampler-input_ and the _current_detour_ (`FN + [` and `FN + ]` are shortcuts for mix=0 and mix=1)
- `a2` will set the _velocity_ of the detour if playing or _position_ if paused
- `a3` will set the _start_ frame of current detour
- `a4` will set the _end_ frame of current detour

this program uses the _mix_shader_ to select the input. there is also the option to use a `1-input` shader in this chain  - either `before` the mix (only on _sampler-input_) or `after` (nice for feedbacky effects). this shader can be selected and toggled in the usual `SHADER` display.
</details>

[3.5mm trrs]: https://www.adafruit.com/product/2881
[display_image]: display_parts.jpg
[player_example]: player_example.jpg
[browser_example]: browser_example.jpg
[sampler_example]: sampler_example.jpg
[settings_example]: settings_example.jpg
[keys]: ./vectorfront_keys.png
[message_example]: ./message_example.jpg
