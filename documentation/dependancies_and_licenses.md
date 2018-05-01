
the more features i add to recur the more dependancies on other software i create. i want to add a license for my work on recur and acknowledge the software it uses , and the license they use.

also need to decide whether my design needs a license outside of the software.

from wikipedia on [gpl]:
`the licensing depends only on the used libraries and software components and not on the underlying platform`


dependancy | use | license
--- | --- | ---
rasbian | the os on pi | based on debian , made up of different licensed programs
python | lanuage | open-source , gpl-compatible
omxplayer | the media player | GPL-2.0
omx python wrapper | for controlling omxplayer | LGPL
dbus-python | dependacy for omx wrapper | permissive, non-copyleft
tkinter | the tui display | bsd
picamera | interface with capture | bsd
mido | interface with midi | mit
python-rt-midi | midi backend | mit / modified mit
gpac (mp4box) | creating mp4 file | lgpl
mscorefonts | the current display font (may need to change this) | freeware under a [proprietary license]
git | used to install and update | GPL-2.0

besides the fonts which are a special case (and some low level black box chips on raspi), all other software is open source.

i have not modified any of the programs that are used in recur. they are all being used either under a permissive license or as part of the operating system. i can license my program however i choose, i can not license (for example) an img that contained gpl-2.0 programs with a non gpl compatable license.

there are no restrictions on selling a product under any of these licenses.

some [interesting discussion] around difference between modifying a gpl program and using one as a dependancy 

there is no restrictions to permissive installer scripts downloading gpl licensed programs (or even the freeware fonts it seems) 

for the non-software side of recur (the case etc) it can be licensed under cc , with apropriate [markings] for third party content (ie screen , usb keypad , raspberry pi)

[gpl]: https://en.wikipedia.org/wiki/GNU_General_Public_License#Use_of_licensed_software
[proprietary license]: https://en.wikipedia.org/wiki/Core_fonts_for_the_Web
[markings]: https://wiki.creativecommons.org/wiki/Marking/Creators/Marking_third_party_content
[interesting discussion]: https://softwareengineering.stackexchange.com/questions/289785/can-i-distribute-a-gpl-executable-not-a-library-in-a-closed-source-application
