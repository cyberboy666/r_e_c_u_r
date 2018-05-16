# midi support

my investigation into controlling recur with midi will be documented here.

### aim

i want to be able to read midi messages to control recur - the simplest intergration would be loading and triggering clips from midi. other paramters controled over cc or otherwise should be easy to add when required. in a similar way to the keypad controls, i would like the mapping to be read from a json file and use this to run actions.

### cheep midi9to-usb dongle

i have decided to start by trying a cheep [usb-to-midi cable] i got for just over $3.

plugging the midi dongle into the pi , i can see it in `client 20` by calling `aconnect -i` , however when connected to a midi controller (deluge) it is not receiving messages when `aseqdump -p 20` is running (besides a few ghost note off events)

running midiox on my windows machine to test the cable also didnt help, it wouldnt receive any messages and complained about not having enough memory...

something seems wrong with the dongle. it also seems like these cheep dongles are not very reliable or useful anyway according to [sy35er] on a yamahamusic forum

update : by using ableton on my windows i could successfully send midi out off usb and receive it on deluge. still no luck reading midi to usb though. 


### usb midi

next i tried using the deluge to output midi over usb. midiox on windows still wouldnt work , but when i tried `aseqdump -p 20` on the pi it recorded the midi perfectly. i will use usb midi to test this feature on recur. (better adapters exist that convert serial midi to usb midi /could make one with ardunio or teensy!), so that will be a good start

i have decided to try using the [mido] python package for responding to midi input.

### midi clock

besides the obvious triggering of clips and controlling parameters, it has also been suggested that the recur could 'sync' to incoming [midi-clock] messages. these communicate a master tempo by sending 24 pulses (clock messages) every quarter note. this could be useful in play modes where the video changes every bar of music (counting pulses from a start message) or even to approximate slowing/speeding of a clip if the speed control of omx would handle it 

### getting started with mido

i install mido and rtmidi for backend : `pip3 install mido python-rtmidi`,
i called `mido.get_input_names()` and searched the results for the first containing the substring `20:0` (this is the port my devices came up as - will need to investigate further why this is and if it will be the case for all external usb midi devices)

from here i called a polling method that reads the next message coming from that port and if there is one will call into the mapping function (from json file)

i created a midi_action.json mapping in the same format as the key press but with `type (value)` as the keys. eg `note_on 70` is an example, `clock` is another. for now i have mapped exactly the same as with the key presses

this works perfectly for pressing keys on the deluge and seeing the corresponding action on recur. even when pressing keys with the sequencer running (lots of clock messages being sent) it still responds quickly and consistently. however when triggering the same notes from the sequencer, it seems to drop lots on the notes : usually only picking up either note_on or note_off , sometimes both and sometimes neither.

I tried changing the way recur handles the incoming messages (working through a list of unprocessed messages rather than one at a time) , but this didnt help - its not a problem of response time as can be shown by pressing keys with sequencer on. even looking at the raw input to the port on `aseqdump -p 20` i can see some messages missing. i updated the deluge firmware to a stable release but no changes.

however when i tried turning off the clock messages from the deluge , the sequencer messages started coming through clearly ! and it syncs up nicely... how strange.

### further clock debugging

other things to try is learning how to use abelton as a midi controller and see whether it works there with/without clock messages. could also try other gear that can output midi / controllers with recur and try deluge with other computer / gear 

### experimenting with cc

besides figuring out whats up with the incoming clock signal , another thing to experiment with is using a cc knob to control parameters in recur. there is nothing pressing i want for this but could try it with : fades , speed? , length of seeks , seeking? 

i ended up trying cc with some camera parameters. there are plenty more interesting examples of continuous control there. it works well , but it seems like running the methods on every change when they are sequenced / coming in consistently is a bit much for recur to respond in real time.

one idea to reduce this is to only process a incoming cc message if it is outside a range for that channel - ie only action on every 3rd cc change for each control for example. - this works well. updating every 5 cc values had no lag under heavy use but looks quite jumpy. step size of 2 looks smooth but can lag quite a lot. i have it set to 4 atm but can revisit when other features are under cv control etc. 




[usb-to-midi cable]: https://www.aliexpress.com/item/Hot-Selling-1pcs-Keyboard-to-PC-USB-MIDI-Cable-Converter-PC-to-Music-Keyboard-Cord-USB/32813475019.html
[instructable]: http://www.instructables.com/id/PiMiDi-A-Raspberry-Pi-Midi-Box-or-How-I-Learned-to/
[mido]: https://mido.readthedocs.io/en/latest/
[midi-clock]: https://en.wikipedia.org/wiki/MIDI_beat_clock
[sy35er]: https://yamahamusicians.com/forum/viewtopic.php?t=8218
