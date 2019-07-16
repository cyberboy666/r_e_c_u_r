# r_e_c_u_r
 an open diy py/pi based video sampler
 
 ![vectorfront][vectorfront]
 
__r_e_c_u_r__ is an embedded python application on _raspberry pi3_ that uses `input` from the _keypad_ to control omxplayer's `video out` while displaying a simple text user interface on the _rpi lcd screen_ 

## in-depth video demo

[![video-walkthrough][video-thumbnail]](http://www.youtube.com/watch?v=FKKDr7pLpp0)

## features

- seamlessly loop video through rpi's HDMI or composite out
- intuitively _browse_ video files from external and internal disk and map them into __r_e_c_u_r__
- load and trigger video samples from numbered slots in the _sampler_ bank
- dynamically set and clear the start/end points of each sample as it plays
- control and sequence all inputs and more with midi-usb
- c_a_p_t_u_r : optional extension for live sampling through the pi camera input
- many sampler modes for varied playback including: repeat, one-shot, gated, random, fixed-length, random-start and more 
- exhaustive and extendable _settings_ menu  to suit your use

### other feature ideas

i started a [board] of some features i would like to explore 

## main objectives:

- *Affordable* : reducing the entry cost to performing with video
- *Extendable* : laying the foundations (of a user interface and code style) that can be easily iterated on by the community
- *Simple* : easy to operate (abstracted completely from ‘driving’ a raspi ) , easy to build (no technical computer install-y or circuit-y knowledge required to diy) , easy to develop (human readable code, inviting amateur/first time coders to contribute)

## documentation:

- [operating] - how to use r_e_c_u_r
- [building] - how to diy r_e_c_u_r
- [developing] - how to contribute to r_e_c_u_r

## status

The nature of this project is to be open-ended and community driven. my r_e_c_u_r already solves the problems i initially built it for. what happens next depends on how it is used and received by you. if you like the idea please let me know / get involved !

## contact, donation and thanks

langolierz@gmail.com

also facebook user group : https://www.facebook.com/groups/114465402691215/

all feedback is appreciated. if you want to donate to this project you can do so with the above email via paypal : everything i receive will go into improving __r_e_c_u_r__. cheers to Leo Browning for the 3d modelling and vector art and to Ben Caldwell for heaps of help with the code!

[vectorfront]: ./documentation/vectorfront_keys.png
[video-thumbnail]: ./documentation/video-thumbnail.jpg
[board]: https://trello.com/b/mmJJFyrp/feature-ideas
[operating]: documentation/operate_docs.md
[building]: documentation/build_docs.md
[developing]: documentation/develop_docs.md
