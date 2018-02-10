# r_e_c_u_r
 an open diy py/pi based video sampler
 
 __r_e_c_u_r__ is an embedded python application on _raspberry pi3_ that uses `input` from the _keypad_ to control omxplayer's `video out` while `displaying` a simple text user interface on the _rpi lcd screen_  

## features

- seamlessly loop video through rpi's HDMI out
- intuitively _browse_ video files on a usb and map them into __r_e_c_u_r__
- load and trigger video samples from numbered slots in the _sampler_ bank
- monitor the current samples playback and the sampler banks details on the lcd display
- dynamicly set and clear the start/end points of each sample as it plays
- configure the _settings_ menu to suit your use case

(more coming soon)

### feature requests

i started a [board] of features i would like to explore 

## main objectives:

- *Affordable* : reducing the entry cost to performing with video
- *Extendable* : laying the foundations (of a user interface and code style) that can be easily iterated on by the community
- *Simple* : easy to operate (abstracted completely from ‘driving’ a raspi ) , easy to build (no technical computer install-y or circuit-y knowledge required to diy) , easy to develop (human readable code, inviting amatuer/first time coders to contribute)

## documentation:

- [operating] - how to use r_e_c_u_r
- [building] - how to build r_e_c_u_r
- [developing] - how to contribute to r_e_c_u_r

## contact

langolierz@gmail.com

[board]: https://trello.com/b/mmJJFyrp/feature-ideas
[operating]: documentation/operate_docs.md
[building]: documentation/build_docs.md
[developing]: documentation/develop_docs.md
