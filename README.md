# r_e_c_u_r
 an open diy py/pi based video sampler
 
 ![vectorfront][vectorfront]
 
 __r_e_c_u_r__ is a fully customizable hardware video sampler. the open source embedded python application is built around a _raspberry pi3_ that uses `input` from a _keypad_ to control omxplayer's `video out` while `displaying` a simple text user interface on a _rpi lcd screen_

## features

- seamlessly loop video through rpi's HDMI or composite out
- intuitively _browse_ video files on a usb and map them into __r_e_c_u_r__
- load and trigger video samples from numbered slots in the _sampler_ bank
- dynamically set and clear the start/end points of each sample as it plays
- configure the _settings_ menu to suit your use

### more coming soon:

- ~~composite video out (hopefully)~~
- midi controlled
- more playback modes and options
- optional extention for live sampling

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

### status

The nature of this project is to be open-ended and community driven. my r_e_c_u_r already solves the problems i intially built it for. what happens next depends on how it is used and recieved by you. if you like the idea please consider getting involved. Currently:

- the _software_ is at a MVP status; the basic functionally is there and should work as expected. no doubt there are both known and unknown bugs around the edges (let me know whats impacting you!). this is also only the beginning of whats possible using python on a raspberry pi. i will continue to maintain and improve it, but in what direction and velocity depends on the users

- the only _hardware_ option currently avaliable is the `diy enclosure`; this is designed be low cost, hackable and accessable. you can modify and 3d print/laser cut your own case, the recommended keypad and lcd parts are the cheapest i could find (with some compromises), basicly aiming to get these in the hands of as many other diy-er as interested. i also have plans to offer a limited `boutique enclosure` option at some point in the future - professional custom cut aluminuim cover , hand wired mechanical keys , real vinyl printed stickers, no compromises! this will probably coincide with a larger software release in near future if theres any interest 

## contact

langolierz@gmail.com

[vectorfront]: ./documentation/vectorfront.png
[board]: https://trello.com/b/mmJJFyrp/feature-ideas
[operating]: documentation/operate_docs.md
[building]: documentation/build_docs.md
[developing]: documentation/develop_docs.md
