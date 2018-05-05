# how to build a r_e_c_u_r - diy enclosure

disclaimer - this is a cheap and diy approach to getting a r_e_c_u_r video sampler in your hands. if you like the device and think its worth some $$ for more professional hardware (mechanical keys, aluminum panels etc) hmu, i can add you the `boutique enclosure` wishlist.

## get some parts

these are the parts you need to get. to reduce shipping costs to nz i sourced them through aliexpress.com but you could equally get them from ebay or elsewhere.

### main parts:

- [raspberry pi3] *37 USD*

- [raspberry pi screen] *12 USD*

- [usb keypad] *9 USD*

![main parts][main parts]

other bits and pieces:

- 4x m2 and 6x m3 screws, 6mm is long enough - i ended up using 4 2-gauge and 6 4-gauge self tapping screws instead which were easier to get into the plastic case.

- 4 gb or greater mircoSD card

- a stable 5volt, 1A microUsb power supply

## print some things

- i 3d printed my enclosure using these files for the top and bottom. if you dont have access to a printer you can upload these files to a popular printing service in you region (eg ...)

- 2d print these [key stickers] if you want to use the default key mapping, or modify the svg file (in inkscape or something) to create your own. you could print them onto vinyl, label paper or just normal paper  and attach with with double sided tape...

## put it together

- using [etcher] (or otherwise) flash the micro sd with my modified image of rasbian (or follow these [instructions to install] from scratch.)

- insert sd card into pi

- attach the lcd screen via the pi header pins so it fits exactly ontop of the pi. (some little spacers could be used to support the top corners of the screen)

- use the 4 small screws to attach pi+screen to the bottom piece of enclosure

- fasten the keypad to the bottom; i used some double sided tap along raised strips

- use the 6 large screws to hold the top panel to the bottom

you are done ! wasnt that easy ?

## try it out !

( [operate docs] )

[raspberry pi3]:https://www.aliexpress.com/item/RS-Version-2016-New-Raspberry-Pi-3-Model-B-Board-1GB-LPDDR2-BCM2837-Quad-Core-Ras/32789942633.html?spm=a2g0s.9042311.0.0.FkRWty
[main parts]: build_all.jpg
[raspberry pi screen]:https://www.aliexpress.com/item/3-5-Inch-TFT-LCD-Moudle-For-Raspberry-Pi-2-Model-B-RPI-B-raspberry-pi/32707058182.html?spm=a2g0s.13010208.99999999.262.bV4EPV
[usb keypad]:https://www.aliexpress.com/item/2-4G-Wireless-Keyboard-USB-Numeric-Keypad-19-Keys-Mini-Digital-Keyboard-Ultra-Slim-Number-Pad/32818206308.html?spm=a2g0s.9042311.0.0.FkRWty
[key stickers]: https://docs.google.com/document/d/1vhXv5QTfyUqsZuMdQu1lh2dMfEk5HMNVyp8uhrc-I2w/edit?usp=sharing
[etcher]: https://etcher.io
[operate docs]: ./operate_docs.md
[instructions to install]: ../dotfiles/README.md 