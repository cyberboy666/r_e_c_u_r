# license info

## software

i have chosen to [license] r_e_c_u_r's software under [GPL-3.0] for the following reasons:

- i agree with the copy-left philosophy and want to empower the users, ensuring it remains (as intended) an open community project.
- although i have not modified any existing open-source projects to create r_e_c_u_r , it does run on top of many dependencies, some of which have GPL licenses (omxplayer in particluar). i wish to respect the sentiment of these developers, even if not required legally.
- for low-level utility tools with numerous, varied uses, a permissive open-source licence like MIT can empower other developers to create and license without restrictions. however r_e_c_u_r is an embedded top level application that is unlikely to be useful in any other context

this licence only applies to the code in this repo. see below for a list of external programs that r_e_c_u_r uses and their respective repos/sites for more infomation.

## hardware

besides the application code licensed above , i would like all original hardware designs licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License]. this includes the enclosure design , custom key stickers and assembly. it does __not__ apply to, and i am __not__ the copyright holder for _Raspberry Pi 3 Model B_ , _3.5 Inch TFT LCD Module For Raspberry Pi_ , _Generic Wireless USB Numeric Keypad_ or any other third party extension / accessory.

# program dependencies

dependency | use | licence
--- | --- | ---
rasbian | the os on pi | based on debian , made up of different licensed programs
python | lanuage | open-source , gpl-compatible
omxplayer | the media player | GPL-2.0
omx python wrapper | for controlling omxplayer | LGPL
dbus-python | dependacy for omx wrapper | permissive, non-copyleft
tkinter | the ui display | BSD
picamera | interface with capture | BSD
mido | interface with midi | MIT
python-rt-midi | midi backend | MIT / modified MIT
gpac (mp4box) | creating mp4 file | LGPL
mscorefonts | the current display font (may need to change this) | freeware under a [proprietary license]
git | used to install and update | GPL-2.0

## some research / thoughts about how licences work and interact.

it will be best to replace the mscorefonts with something open...

i have not modified any of the programs that are used in recur. they are all being used either under a permissive license or as part of the operating system. i can license my program however i choose, i can not license (for example) an img that contained gpl-2.0 programs with a non gpl compatable license.

there are no restrictions on selling a product under any of these licenses.

some [interesting discussion] around difference between modifying a gpl program and using one as a dependancy , 
- if it is part of the os it is ok.
- if it is not 2-way interacting / sharing datastructures etc - just an input -> output usage it is ok

there is no restrictions to permissive installer scripts downloading gpl licensed programs (or even the freeware fonts it seems) 

[license] : ../LICENSE.md
[GPL-3.0]: https://www.gnu.org/licenses/gpl-3.0.en.html
[proprietary license]: https://en.wikipedia.org/wiki/Core_fonts_for_the_Web
[markings]: https://wiki.creativecommons.org/wiki/Marking/Creators/Marking_third_party_content
[interesting discussion]: https://softwareengineering.stackexchange.com/questions/289785/can-i-distribute-a-gpl-executable-not-a-library-in-a-closed-source-application
[Creative Commons Attribution-ShareAlike 4.0 International License]: https://creativecommons.org/licenses/by-sa/4.0/
