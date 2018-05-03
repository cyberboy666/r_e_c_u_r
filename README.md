# r_e_c_u_r
 an open diy py/pi based video sampler
 
 ![vectorfront][vectorfront]
 
__r_e_c_u_r__ is an embedded python application on _raspberry pi3_ that uses `input` from the _keypad_ to control omxplayer's `video out` while displaying a simple text user interface on the _rpi lcd screen_ 

## features

- seamlessly loop video through rpi's HDMI or composite out
- intuitively _browse_ video files on an external usb or internally and map them into __r_e_c_u_r__
- load and trigger video samples from numbered slots in the _sampler_ bank
- dynamically set and clear the start/end points of each sample as it plays
- control and sequence all inputs and more with midi-usb
- optional extention for live sampling through the pi camera input
- many sampler modes for varied playback including: repeat, one-shot, gated, random, fixed-length, random-start and more 
- exhaustive and extendable _settings_ menu  to suit your use

### other feature ideas

i started a [board] of some features i would like to explore 

## main objectives:

- *Affordable* : reducing the entry cost to performing with video
- *Extendable* : laying the foundations (of a user interface and code style) that can be easily iterated on by the community
- *Simple* : easy to operate (abstracted completely from ‘driving’ a raspi ) , easy to build (no technical computer install-y or circuit-y knowledge required to diy) , easy to develop (human readable code, inviting amatuer/first time coders to contribute)

## documentation:

- [operating] - how to use r_e_c_u_r
- [building] - how to build r_e_c_u_r
- [developing] - how to contribute to r_e_c_u_r

## status

The nature of this project is to be open-ended and community driven. my r_e_c_u_r already solves the problems i intially built it for. what happens next depends on how it is used and recieved by you. if you like the idea please consider getting involved.

- the only _hardware_ option currently avaliable is the `diy enclosure`; this is designed be low cost, hackable and accessable. you can modify and 3d print/laser cut your own case, the recommended keypad and lcd parts are the cheapest i could find (with some compromises), basically aiming to get these in the hands of as many other diy-er as interested. if there is any interest i have plans to offer a limited `boutique enclosure` option at some point - professional custom cut aluminum cover , hand wired mechanical keys , real vinyl printed stickers, no compromises! (another future idea : a eurorack version based on raspi3 compute)

## contact and donation

langolierz@gmail.com

all feedback is apreciated. if you want to donate to this project you can do so with the above email via paypal : everything i receive will go into making __r_e_c_u_r__ better.

[vectorfront]: ./documentation/vectorfront.png
[board]: https://trello.com/b/mmJJFyrp/feature-ideas
[operating]: documentation/operate_docs.md
[building]: documentation/build_docs.md
[developing]: documentation/develop_docs.md
