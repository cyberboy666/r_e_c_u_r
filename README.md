# r_e_c_u_r

 an open diy video sampler
 
 ![vectorfront][vectorfront]
 
__r_e_c_u_r__ is an embedded python/openframeworks application on _raspberry pi3_ that uses `input` from the _keypad_ to control  `video` while displaying a simple text ui on a _rpi lcd screen_ 

## in-depth video demo

[![video-walkthrough][video-thumbnail]](http://www.youtube.com/watch?v=FKKDr7pLpp0)

## features

- seamlessly loop video through rpi's HDMI or composite out
- intuitively _browse_ video files from external and internal disk and map them into __r_e_c_u_r__
- load and trigger video samples from numbered slots in the _sampler_ bank
- dynamically set and clear the start/end points of each sample as it plays
- control and sequence all inputs and more with midi-usb
- many sampler modes for varied playback including: repeat, one-shot, gated, random, fixed-length, random-start and more 
- exhaustive and extendable _settings_ menu  to suit your use

## extensions

as of _V2.0_ the __r_e_c_u_r__ platform has been extended in a number of directions to complement live performance and  _\_recur\__ , the original video playing engine:

- _\_captur\__ : input live video via CSI or USB , for live sampling and processing
- _\_conjur\__ : glsl shader engine, map and trigger shader files and control parameters in real time; generate video or process and mix existing sources
- _\_detour\__ : in-memory frame sampling (up to 500 frames), video scrubbing, playback speed and direction control, finger drumming
- toggling internal feedback + strobe effect 

_NOTE: most of the new V2.0 features are optimised for sd composite video output. Some of these extensions will work over HDMI but they are not fully supported - especially the live video input struggles_

### extension video walkthroughs

- [![conjur_walkthrough][conjur_thumbnail]](https://www.youtube.com/watch?v=ah2HY1fuv8w)
- [![captur_walkthrough][captur_thumbnail]](https://www.youtube.com/watch?v=e7m_YHEFahs)
- [![detour_walkthrough][detour_thumbnail]](https://www.youtube.com/watch?v=e9vrzn7c9R8)

## main objectives:

- *Affordable* : reducing the entry cost to performing with video
- *Extendable* : laying the foundations (of a user interface and code style) that can be easily iterated on by the community
- *Simple* : easy to operate (abstracted completely from ‘driving’ a raspi ) , easy to build (no technical computer install-y or circuit-y knowledge required to diy) , easy to develop (human readable code, inviting amateur/first time coders to contribute)

## documentation:

- [operating] - how to use r_e_c_u_r
- [building] - how to diy r_e_c_u_r
- [developing] - how to contribute to r_e_c_u_r

many other things documented on the [wiki]

## status

The nature of this project is to be open-ended and community driven. my r_e_c_u_r already solves the problems i initially built it for. what happens next depends on how it is used and received by you. if you like the idea please let me know / get involved !

## contact, donation and thanks

langolierz@gmail.com

you can find me (and others) at https://scanlines.xyz , an online diy av community space. theres a r_e_c_u_r channel in the chatroom: https://chat.scanlines.xyz/channel/r_e_c_u_r
there is also a facebook user group : https://www.facebook.com/groups/114465402691215/

all feedback is appreciated. if you want to donate to this project you can do so with the above email via paypal : everything i receive will go into improving __r_e_c_u_r__. cheers to Leo Browning for the 3d modelling and vector art and to Ben Caldwell for heaps of help with the code!

[vectorfront]: ./enclosure/vectorfront_keys.png
[video-thumbnail]: https://github.com/langolierz/r_e_c_u_r/wiki/images/video-thumbnail.jpg
[conjur_thumbnail]: https://github.com/langolierz/r_e_c_u_r/wiki/images/conjur_video_thumbnail.jpg
[captur_thumbnail]: https://github.com/langolierz/r_e_c_u_r/wiki/images/captur_video_thumbnail.jpg
[detour_thumbnail]: https://github.com/langolierz/r_e_c_u_r/wiki/images/detour_video_thumbnail.jpg
[operating]: https://github.com/langolierz/r_e_c_u_r/wiki/operate_docs
[building]: https://github.com/langolierz/r_e_c_u_r/wiki/build_docs
[developing]: https://github.com/langolierz/r_e_c_u_r/wiki/develop_docs
[wiki]: https://github.com/langolierz/r_e_c_u_r/wiki
