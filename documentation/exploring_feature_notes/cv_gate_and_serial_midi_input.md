

### serial midi from rpi gpio pin

i believe it is possible to read midi in from an i/o pin (that can read serial) which might be desirable in some cases but this is a good start for now. this [instructable] explains how to input/output midi with the gpios, it looks like the tx/rx (serial?) pins on the pi3 are currently used/covered by the gpio screen that i am using. if i was serious about external circuits interfacing with pi/recur, i might look into using an lcd screen that doesnt use up the gpios. (would also be worth checking if piCapture would work with the gpio screen i have...)

### gpio pins : 

the [adafruit tft display] mentioned above also uses the gpios to connect to the pi - in particular it uses 5 spi pins and two standard pin outs. by cross refferencing the [raspi gpio] docs it does not use either of the rx serial pin , which would be needed if i were to receive midi directly (rather than through usb), it also leaves plenty of pins for receiving cv from a [mcp3008] through software spi for example. it is likely that my gpio lcd screen comunicates with the pi in a similar way and that i could figure out a way to connect these extentions if desired.

[instructable]: http://www.instructables.com/id/PiMiDi-A-Raspberry-Pi-Midi-Box-or-How-I-Learned-to/
[adafruit tft display]: https://www.adafruit.com/product/2441
[raspi gpio]: https://www.raspberrypi.org/documentation/usage/gpio/
[mcp3008]: https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008