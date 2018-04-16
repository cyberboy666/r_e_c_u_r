# midi support

my investigation into controlling recur with midi will be documented here.

i have decided to start by using a cheep [usb-to-midi cable] i got for just over $3. i believe it is possible to read midi in off an i/o pin (that can read serial) which might be desirable in some cases but this is a good start for now. this [instructable] explains how to input/output midi with the gpios, it looks like the tx/rx (serial?) pins on the pi3 are currently used/covered by the gpio screen that i am using. if i was serious about external circuits interfacing with pi/recur, i might look into using an lcd screen that doesnt use up the gpios. (would also be worth checking if piCapture would work with the gpio screen i have...)

i want to be able to read midi messages from this input to control recur - the simplest intergration would be loading and triggering clips from midi. other paramters controled over cc or otherwise should be easy to add when required. in a similar way to the keypad controls, i would like the mapping to be read from a json file and use this to run actions.

plugging the midi dongle into the pi , i can see it in `client 20` by calling `aconnect -i` , however when connected to a midi controller (deluge) it is not receiving messages when `aseqdump -p 20` is running (besides a few ghost note off events)

running midiox on my windows machine to test the cable also didnt help, it wouldnt receive any messages and complained about not having enough memory...







[usb-to-midi cable]: https://www.aliexpress.com/item/Hot-Selling-1pcs-Keyboard-to-PC-USB-MIDI-Cable-Converter-PC-to-Music-Keyboard-Cord-USB/32813475019.html
[instructable]: http://www.instructables.com/id/PiMiDi-A-Raspberry-Pi-Midi-Box-or-How-I-Learned-to/
