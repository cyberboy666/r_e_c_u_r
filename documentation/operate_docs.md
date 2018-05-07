# how to use r_e_c_u_r

## getting started

- prepare a usb with some videos you want to sample
- connect the hdmi output or composite (via [3.5mm trrs]) to the display you want to use
- power the raspberry pi. you should see red lights on the pi board, the lcd display light up and the r_e_c_u_r splash screen on your video output
- after a few moments the interface should appear on lcd screen.
- the `DSPLY` key can be used to cycle through _display_modes_

## controls

![keys][./vectorfront_keys.png]

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

(put image and info here)

[3.5mm trrs]: https://www.adafruit.com/product/2881
[display_image]: display_parts.jpg
[player_example]: player_example.jpg
[browser_example]: browser_example.jpg
[sampler_example]: sampler_example.jpg
[settings_example]: settings_example.jpg
