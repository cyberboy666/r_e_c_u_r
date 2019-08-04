
## BOM

REFERENCE | QUANTITY | DESCRIPTION | PACKAGE | NOTE
--- | --- | --- | --- | ---
R1, R2, R3, R4 | 4 | 1K Resistor | through-hole | -
R5 | 1 | 220 Resistor | through-hole | -
R6 | 1 | 100K Resistor | through-hole | -
R7 | 1 | 470 Resistor | through-hole | -
D1, D2, D3, D4, D5, D6, D7, D8 | 8 | BAT85 Diode | through-hole | -
D9 | 1 | 1N4148 Diode | through-hole | -
U1 | 1 | MCP3008 IC | DIP-16 | you can get these from mouser ,adafruit, even ali
U2 | 1 | 6N138 IC | DIP-8 | -
RV1, RV2, RV3, RV4 | 4 | 1K_LINEAR_POT | ALPHA | tayda ones work although shaft may be too short
J1, J2, J3, J4 | 4 | 3.5MM_JACK | THONKICONN | from thonk or 50pc from modular addict
J5 | 1 | MIDI_DIN_IN | SD-50BV | mouser
J6 | 1 | 1X1_PIN_HEADER | - | -
J7 | 1 | RCA_JACK | RCJ-024 | mouser or ali
J8 | 1 | 20X2_PIN_HEADER | long pins | this needs to be the long "hat" version

### OPTIONAL :
- if you want your ic's in sockets you should buy some DIP-8 /16 also now
- if you only want the _analog_inputs_ and not interested in _serial_midi_, you already have usb midi etc, then you can obmit _R5_, _R6_, _R7_, _D9_, _U2_ from the BOM - see circuit schematic for details

## BUILD

start with the lowest to place components : resistors, diodes, ic's

next i would place the two headers since soldering from the top can be awkward with too many components - __NOTE__ these need to be placed __upside down!__ ,:
- _J8_ needs the pins facing up from top of pcb so the screen can go ontop and raspberry pi can go underneath
- _J6_ also needs to soldered from the top so a jumper from the pi board can be run to bottom of circuit

finally place the pots and jacks.

### rca video-out

if you want RCA video out from the pi on this pcb a jumper needs to be run from _J6_ to the composite video out on the raspberry pi board. on pi0 this is a labelled pin, however on pi3 you will need to solder directly to the board. i used a header-cable, cut one side to be soldered.

need to add some images and links to this guide !

