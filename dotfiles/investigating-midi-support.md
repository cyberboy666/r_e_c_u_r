# midi support

my investigation into controlling recur with midi will be documented here.

i have decided to start by using a cheep [usb-to-midi cable] i got for just over $3. i believe it is possible to read midi in off an i/o pin (that can read serial) which might be desirable in some cases but this is a good start for now.

i want to be able to read midi messages from this input to control recur - the simplest intergration would be loading and triggering clips from midi. other paramters controled over cc or otherwise should be easy to add when required. in a similar way to the keypad controls, i would like the mapping to be read from a json file and use this to run actions.





[usb-to-midi cable]: https://www.aliexpress.com/item/Hot-Selling-1pcs-Keyboard-to-PC-USB-MIDI-Cable-Converter-PC-to-Music-Keyboard-Cord-USB/32813475019.html
