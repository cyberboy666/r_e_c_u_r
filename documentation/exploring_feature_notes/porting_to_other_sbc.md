# porting to other sbc

a collection of thoughts / research / attempts at porting r_e_c_u_r

## attempting to port r_e_c_u_r to an orange pi plus

i bought an [orange pi plus] at the same time as my raspberry pi 3 , thinking that since they are 
similarly spec-ed (orange pi is a little weaker but also much cheaper ~18US vs ~38USD i payed for rpi3) this might be an interesting alternative to offer.

i (naively) figured since opi claim to support raspbian as an os, that this might be as simple as installing the same dependencies outlined in the [preparing image] notes and maybe some fiddling with the lcd-screen drivers...

it seems like the only raspbian image for orange pi plus was a fork of wheezy distro from 2015 with pre-installed desktop. this is not supported or updated by orange pi and seems to be a token gesture to compete on paper with raspberry pi. with this image i managed to install some dependencies, but the dbus packages needed for the omx wrapper couldnt be installed (i think the os was too old). also their is no config.txt on orangepi so settings like composite video out and different hdmi modes was going to be more difficult (not to mention the lcd screen driver)

## porting to armbian

however what is supported and updated is an os called armbian , which (similar to raspbian)
is a version of debian (or linux) made for ARM dev boards. if i can get r_e_c_u_r working on opi running latest armbian , it might also work on a bunch of other sbc including other orange pis, ondroids , banana pi etc (beaglebone's run straight debian so perhaps i should see if it works there too)

given that the software dependencies are available in these alternative os (im not sure if they are yet but will just have to try it) some other problems to solve when trying to port r_e_c_u_r to other sbcs are:

- connecting a lcd screen / playing video to one framebuffer while running python on another. 
[Kaspars Dambis' blog] describes how to configure a similar lcd display to mine on an orange pi zero running armbian so hopefully this could help porting it to orange pi pc
- playing the video through one framebuffer (hdmi or composite) while the python code displays on another (lcd screen)
this kindof 'just worked' for me on raspberry pi running rasbian but i dont know how it will translate...
- video playback might be weaker depending on the gpu acceleration of these alternative boards 
(omxplayer is accelerated for rpi but probably not for these others). also things like h.2 video codex
licencing things etc might come into it
- configuring different hdmi and composite video settings. (pi seems to do this particularly well)

## conclusion for now

some more research into this is required , but at this point it seems like the extra effort to get recur running on other smc's might not be worth the savings in cost or flexibility.

r_e_c_u_r is an embedded solution and the choice of hardware (raspi3) is tied to the application : 

- lcd screen drivers
- omxplayer w acceleration
- (future features using pi camera / capture devices)

right now rpi3 still seems like the best tool for the job and the benefits of running cross-boards are
not enough to distract from improving this implementation. (perhaps a future recur independent of omxplayer might benefit more from running on main debian / armian)

## r_e_c_u_r on other raspberry pi boards

as an aside, i am still hopeful that r_e_c_u_r will run on rpi2 and/or zero with little to no changes required. this might be a more useful and achievable port to focus on for now.




[orange pi plus]: https://www.aliexpress.com/item/Orange-Pi-PC-linux-and-android-mini-PC-Beyond-Raspberry-Pi-2/32448079125.html?spm=a2g0s.9042311.0.0.kWJI0G
[preparing image]: ./preparing_image.md
[Kaspars Dambis' blog]: https://kaspars.net/blog/linux/spi-display-orange-pi-zero
