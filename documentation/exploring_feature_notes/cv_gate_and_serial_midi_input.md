

### serial midi from rpi gpio pin

i believe it is possible to read midi in from an i/o pin (that can read serial) which might be desirable in some cases but this is a good start for now. this [instructable] explains how to input/output midi with the gpios, it looks like the tx/rx (serial?) pins on the pi3 are currently used/covered by the gpio screen that i am using. if i was serious about external circuits interfacing with pi/recur, i might look into using an lcd screen that doesnt use up the gpios. (would also be worth checking if piCapture would work with the gpio screen i have...)

### gpio pins : 

the [adafruit tft display] mentioned above also uses the gpios to connect to the pi - in particular it uses 5 spi pins and two standard pin outs. by cross referencing the [raspi gpio] docs it does not use either of the rx serial pin , which would be needed if i were to receive midi directly (rather than through usb), it also leaves plenty of pins for receiving cv from a [mcp3008] through software spi for example. it is likely that my gpio lcd screen communicates with the pi in a similar way and that i could figure out a way to connect these extensions if desired.

what follows is the interface of cheep lcd from the shop page :

PIN NO.| SYMBOL | DESCRIPTION
--- | --- | ---
1, 17| 3.3V | Power positive (3.3V power input)
2, 4 | 5V | Power positive (5V power input)
3, 5, 7, 8, 10, 12, 13, 15, 16 | NC | NC
6, 9, 14, 20, 25 | GND | Ground
11 | TP_IRQ | Touch Panel interrupt, low level while the Touch Panel detects touching
18 | LCD_RS | Instruction/Data Register selection
19 | LCD_SI / TP_SI | SPI data input of LCD/Touch Panel
21 | TP_SO | SPI data output of Touch Panel
22 | RST | Reset
23 | LCD_SCK / TP_SCK | SPI clock of LCD/Touch Panel
24 | LCD_CS | LCD chip selection, low active
26 | TP_CS | Touch Panel chip selection, low active

from this i should b able to work out which pins i can use for midi in and for analog-to-digital inputs (also piCapture needs some inputs too)

# gpio inputs for recur:

here are the pins needed for different parts of the recur connections:

note that pins 1 to 26 are covered by the lcd screen, even though not all are used by it

## lcd screen 

as stated above, the screen uses the following pins:
- 1 , 17 : 3.3v
- 2, 4 : 5v
- 11 : TP_IQR (for touch panel)
- 18 : LCD_RS
- 19 : LCD_SI
- 21 : TP_SO (touch panel output)
- 22 : reset
- 23 : LCD_SCK
- 24 : LCD_CS
- 26 : TP_CS

## piCapture

piCapture be default will use pins 3, 5, 7 to comunicate 

## serial-midi in

pin 10 (rx) is needed for midi in plus 3.3v (combined with octocoupler 6n138 etc and resistors)

## analog in

using a MCP3008 via hardware SPI, can connect up to 8 analog inputs using pins 35, 36, 38, 40 (SPI1) + 3.3v , can also connect with software SPI with any four pins if more inputs were needed. these inputs can be used for pots/sliders & gate/cv jacks. by default will react to 0-3.3v. if wanting to use larger range than this will need some kind of scaling electronics (tl074d?)

providing 4 pins on under the lcd screen cover can be accessed by the board (and 3.3v can be distributed) i should be able to create a circuit that connects all these inputs to the pi. 


[instructable]: http://www.instructables.com/id/PiMiDi-A-Raspberry-Pi-Midi-Box-or-How-I-Learned-to/
[adafruit tft display]: https://www.adafruit.com/product/2441
[raspi gpio]: https://www.raspberrypi.org/documentation/usage/gpio/
[mcp3008]: https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
