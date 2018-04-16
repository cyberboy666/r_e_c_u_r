# midi support

my investigation into controlling recur with midi will be documented here.

### aim

i want to be able to read midi messages to control recur - the simplest intergration would be loading and triggering clips from midi. other paramters controled over cc or otherwise should be easy to add when required. in a similar way to the keypad controls, i would like the mapping to be read from a json file and use this to run actions.

### cheep midi9to-usb dongle

i have decided to start by trying a cheep [usb-to-midi cable] i got for just over $3.

plugging the midi dongle into the pi , i can see it in `client 20` by calling `aconnect -i` , however when connected to a midi controller (deluge) it is not receiving messages when `aseqdump -p 20` is running (besides a few ghost note off events)

running midiox on my windows machine to test the cable also didnt help, it wouldnt receive any messages and complained about not having enough memory...

something seems wrong with the dongle. it also seems like these cheep dongles are not very reliable or useful anyway according to [sy35er] on a yamahamusic forum

### serial midi from rpi gpio pin

i believe it is possible to read midi in from an i/o pin (that can read serial) which might be desirable in some cases but this is a good start for now. this [instructable] explains how to input/output midi with the gpios, it looks like the tx/rx (serial?) pins on the pi3 are currently used/covered by the gpio screen that i am using. if i was serious about external circuits interfacing with pi/recur, i might look into using an lcd screen that doesnt use up the gpios. (would also be worth checking if piCapture would work with the gpio screen i have...)

### usb midi

next i tried using the deluge to output midi over usb. midiox on windows still wouldnt work , but when i tried `aseqdump -p 20` on the pi it recorded the midi perfectly. i will use usb midi to test this feature on recur. (better adapters exist that convert serial midi to usb midi /could make one with ardunio or teensy!), so that will be a good start

i have decided to try using the [mido] python package for responding to midi input.

### midi clock

besides the obvious triggering of clips and controlling parameters, it has also been suggested that the recur could 'sync' to incoming [midi-clock] messages. these communicate a master tempo by sending 24 pulses (clock messages) every quarter note. this could be useful in play modes where the video changes every bar of music (counting pulses from a start message) or even to approximate slowing/speeding of a clip if the speed control of omx would handle it 





[usb-to-midi cable]: https://www.aliexpress.com/item/Hot-Selling-1pcs-Keyboard-to-PC-USB-MIDI-Cable-Converter-PC-to-Music-Keyboard-Cord-USB/32813475019.html
[instructable]: http://www.instructables.com/id/PiMiDi-A-Raspberry-Pi-Midi-Box-or-How-I-Learned-to/
[mido]: https://mido.readthedocs.io/en/latest/
[midi-clock]: https://en.wikipedia.org/wiki/MIDI_beat_clock
[sy35er]: https://yamahamusicians.com/forum/viewtopic.php?t=8218
