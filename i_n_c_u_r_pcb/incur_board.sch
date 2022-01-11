EESchema Schematic File Version 4
LIBS:incur_board-cache
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "i_n_c_u_r board"
Date "2019-06-01"
Rev "v5"
Comp "cyberboy666 & user43368831"
Comment1 "created by tim caldwell"
Comment2 "CC-BY-SA"
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L incur_board-rescue:DIN-5_180degree J5
U 1 1 5BC53796
P 6250 1125
F 0 "J5" H 6375 1350 50  0000 C CNN
F 1 "din5" H 6250 875 50  0000 C CNN
F 2 "lib_fp:tht_vertical_din5" H 6250 1125 50  0001 C CNN
F 3 "" H 6250 1125 50  0001 C CNN
	1    6250 1125
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:POT RV1
U 1 1 5BC53B0C
P 3950 2875
F 0 "RV1" V 3775 2875 50  0000 C CNN
F 1 "10k_pot" V 3850 2875 50  0000 C CNN
F 2 "lib_fp:tht_vertical_potentiometer" H 3950 2875 50  0001 C CNN
F 3 "" H 3950 2875 50  0001 C CNN
	1    3950 2875
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:MCP3208 U1
U 1 1 5BC569F6
P 6475 3725
F 0 "U1" H 6275 4250 50  0000 R CNN
F 1 "MCP3008" H 6275 4175 50  0000 R CNN
F 2 "Housings_DIP:DIP-16_W7.62mm_LongPads" H 6575 3825 50  0001 C CNN
F 3 "" H 6575 3825 50  0001 C CNN
	1    6475 3725
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:6N138 U2
U 1 1 5BC57C89
P 7300 1775
F 0 "U2" H 7140 2125 50  0000 C CNN
F 1 "6N138" H 7390 2125 50  0000 C CNN
F 2 "Housings_DIP:DIP-8_W7.62mm_LongPads" H 7590 1475 50  0001 C CNN
F 3 "" H 7590 1475 50  0001 C CNN
	1    7300 1775
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:R R5
U 1 1 5BC58A3C
P 6275 1525
F 0 "R5" V 6355 1525 50  0000 C CNN
F 1 "220" V 6275 1525 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 6205 1525 50  0001 C CNN
F 3 "" H 6275 1525 50  0001 C CNN
	1    6275 1525
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:R R7
U 1 1 5BC58E2E
P 8325 1575
F 0 "R7" V 8405 1575 50  0000 C CNN
F 1 "470" V 8325 1575 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 8255 1575 50  0001 C CNN
F 3 "" H 8325 1575 50  0001 C CNN
	1    8325 1575
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:R R6
U 1 1 5BC58F88
P 8025 2125
F 0 "R6" V 8105 2125 50  0000 C CNN
F 1 "100K" V 8025 2125 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 7955 2125 50  0001 C CNN
F 3 "" H 8025 2125 50  0001 C CNN
	1    8025 2125
	-1   0    0    1   
$EndComp
$Comp
L incur_board-rescue:D D9
U 1 1 5BC591F2
P 6675 1725
F 0 "D9" H 6675 1825 50  0000 C CNN
F 1 "1N4148" H 6675 1625 50  0000 C CNN
F 2 "Diodes_THT:D_DO-35_SOD27_P5.08mm_Vertical_KathodeUp" H 6675 1725 50  0001 C CNN
F 3 "" H 6675 1725 50  0001 C CNN
	1    6675 1725
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:R R1
U 1 1 5BC59626
P 2275 1200
F 0 "R1" V 2355 1200 50  0000 C CNN
F 1 "1K" V 2275 1200 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2205 1200 50  0001 C CNN
F 3 "" H 2275 1200 50  0001 C CNN
	1    2275 1200
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:D D1
U 1 1 5BC5A965
P 1900 975
F 0 "D1" H 1900 1075 50  0000 C CNN
F 1 "BAT46" H 1900 875 50  0000 C CNN
F 2 "Diodes_THT:D_DO-35_SOD27_P5.08mm_Vertical_KathodeUp" H 1900 975 50  0001 C CNN
F 3 "" H 1900 975 50  0001 C CNN
	1    1900 975 
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:D D2
U 1 1 5BC5A9EA
P 1900 1425
F 0 "D2" H 1900 1525 50  0000 C CNN
F 1 "BAT46" H 1900 1325 50  0000 C CNN
F 2 "Diodes_THT:D_DO-35_SOD27_P5.08mm_Vertical_KathodeUp" H 1900 1425 50  0001 C CNN
F 3 "" H 1900 1425 50  0001 C CNN
	1    1900 1425
	0    1    1    0   
$EndComp
Text GLabel 2675 1200 2    60   Input ~ 0
A_IN_0
$Comp
L incur_board-rescue:GND #PWR01
U 1 1 5BC60E2C
P 1450 1800
F 0 "#PWR01" H 1450 1550 50  0001 C CNN
F 1 "GND" H 1450 1650 50  0000 C CNN
F 2 "" H 1450 1800 50  0001 C CNN
F 3 "" H 1450 1800 50  0001 C CNN
	1    1450 1800
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:+5V #PWR02
U 1 1 5BC62929
P 3950 2475
F 0 "#PWR02" H 3950 2325 50  0001 C CNN
F 1 "+5V" H 3950 2615 50  0000 C CNN
F 2 "" H 3950 2475 50  0001 C CNN
F 3 "" H 3950 2475 50  0001 C CNN
	1    3950 2475
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:GND #PWR03
U 1 1 5BC62BE1
P 3950 3275
F 0 "#PWR03" H 3950 3025 50  0001 C CNN
F 1 "GND" H 3950 3125 50  0000 C CNN
F 2 "" H 3950 3275 50  0001 C CNN
F 3 "" H 3950 3275 50  0001 C CNN
	1    3950 3275
	1    0    0    -1  
$EndComp
Text GLabel 4475 2875 2    60   Input ~ 0
A_IN_4
$Comp
L incur_board-rescue:R R2
U 1 1 5BC64EDC
P 2300 2675
F 0 "R2" V 2380 2675 50  0000 C CNN
F 1 "1K" V 2300 2675 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2230 2675 50  0001 C CNN
F 3 "" H 2300 2675 50  0001 C CNN
	1    2300 2675
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:D D3
U 1 1 5BC64EE2
P 1925 2450
F 0 "D3" H 1925 2550 50  0000 C CNN
F 1 "BAT46" H 1925 2350 50  0000 C CNN
F 2 "Diodes_THT:D_DO-35_SOD27_P5.08mm_Vertical_KathodeUp" H 1925 2450 50  0001 C CNN
F 3 "" H 1925 2450 50  0001 C CNN
	1    1925 2450
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:D D4
U 1 1 5BC64EE8
P 1925 2900
F 0 "D4" H 1925 3000 50  0000 C CNN
F 1 "BAT46" H 1925 2800 50  0000 C CNN
F 2 "Diodes_THT:D_DO-35_SOD27_P5.08mm_Vertical_KathodeUp" H 1925 2900 50  0001 C CNN
F 3 "" H 1925 2900 50  0001 C CNN
	1    1925 2900
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:+5V #PWR04
U 1 1 5BC64EEE
P 1925 2150
F 0 "#PWR04" H 1925 2000 50  0001 C CNN
F 1 "+5V" H 1925 2290 50  0000 C CNN
F 2 "" H 1925 2150 50  0001 C CNN
F 3 "" H 1925 2150 50  0001 C CNN
	1    1925 2150
	1    0    0    -1  
$EndComp
Text GLabel 2700 2675 2    60   Input ~ 0
A_IN_1
$Comp
L incur_board-rescue:GND #PWR05
U 1 1 5BC64EF5
P 1475 3275
F 0 "#PWR05" H 1475 3025 50  0001 C CNN
F 1 "GND" H 1475 3125 50  0000 C CNN
F 2 "" H 1475 3275 50  0001 C CNN
F 3 "" H 1475 3275 50  0001 C CNN
	1    1475 3275
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:R R3
U 1 1 5BC654BC
P 2300 4175
F 0 "R3" V 2380 4175 50  0000 C CNN
F 1 "1K" V 2300 4175 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2230 4175 50  0001 C CNN
F 3 "" H 2300 4175 50  0001 C CNN
	1    2300 4175
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:D D5
U 1 1 5BC654C2
P 1925 3950
F 0 "D5" H 1925 4050 50  0000 C CNN
F 1 "BAT46" H 1925 3850 50  0000 C CNN
F 2 "Diodes_THT:D_DO-35_SOD27_P5.08mm_Vertical_KathodeUp" H 1925 3950 50  0001 C CNN
F 3 "" H 1925 3950 50  0001 C CNN
	1    1925 3950
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:D D6
U 1 1 5BC654C8
P 1925 4400
F 0 "D6" H 1925 4500 50  0000 C CNN
F 1 "BAT46" H 1925 4300 50  0000 C CNN
F 2 "Diodes_THT:D_DO-35_SOD27_P5.08mm_Vertical_KathodeUp" H 1925 4400 50  0001 C CNN
F 3 "" H 1925 4400 50  0001 C CNN
	1    1925 4400
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:+5V #PWR06
U 1 1 5BC654CE
P 1925 3650
F 0 "#PWR06" H 1925 3500 50  0001 C CNN
F 1 "+5V" H 1925 3790 50  0000 C CNN
F 2 "" H 1925 3650 50  0001 C CNN
F 3 "" H 1925 3650 50  0001 C CNN
	1    1925 3650
	1    0    0    -1  
$EndComp
Text GLabel 2700 4175 2    60   Input ~ 0
A_IN_2
$Comp
L incur_board-rescue:GND #PWR07
U 1 1 5BC654D5
P 1475 4775
F 0 "#PWR07" H 1475 4525 50  0001 C CNN
F 1 "GND" H 1475 4625 50  0000 C CNN
F 2 "" H 1475 4775 50  0001 C CNN
F 3 "" H 1475 4775 50  0001 C CNN
	1    1475 4775
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:R R4
U 1 1 5BC654EA
P 2325 5650
F 0 "R4" V 2405 5650 50  0000 C CNN
F 1 "1K" V 2325 5650 50  0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2255 5650 50  0001 C CNN
F 3 "" H 2325 5650 50  0001 C CNN
	1    2325 5650
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:D D7
U 1 1 5BC654F0
P 1950 5425
F 0 "D7" H 1950 5525 50  0000 C CNN
F 1 "BAT46" H 1950 5325 50  0000 C CNN
F 2 "Diodes_THT:D_DO-35_SOD27_P5.08mm_Vertical_KathodeUp" H 1950 5425 50  0001 C CNN
F 3 "" H 1950 5425 50  0001 C CNN
	1    1950 5425
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:D D8
U 1 1 5BC654F6
P 1950 5875
F 0 "D8" H 1950 5975 50  0000 C CNN
F 1 "BAT46" H 1950 5775 50  0000 C CNN
F 2 "Diodes_THT:D_DO-35_SOD27_P5.08mm_Vertical_KathodeUp" H 1950 5875 50  0001 C CNN
F 3 "" H 1950 5875 50  0001 C CNN
	1    1950 5875
	0    1    1    0   
$EndComp
$Comp
L incur_board-rescue:+5V #PWR08
U 1 1 5BC654FC
P 1950 5125
F 0 "#PWR08" H 1950 4975 50  0001 C CNN
F 1 "+5V" H 1950 5265 50  0000 C CNN
F 2 "" H 1950 5125 50  0001 C CNN
F 3 "" H 1950 5125 50  0001 C CNN
	1    1950 5125
	1    0    0    -1  
$EndComp
Text GLabel 2725 5650 2    60   Input ~ 0
A_IN_3
$Comp
L incur_board-rescue:GND #PWR09
U 1 1 5BC65503
P 1500 6250
F 0 "#PWR09" H 1500 6000 50  0001 C CNN
F 1 "GND" H 1500 6100 50  0000 C CNN
F 2 "" H 1500 6250 50  0001 C CNN
F 3 "" H 1500 6250 50  0001 C CNN
	1    1500 6250
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:POT RV2
U 1 1 5BC66915
P 3950 4150
F 0 "RV2" V 3775 4150 50  0000 C CNN
F 1 "10k_pot" V 3850 4150 50  0000 C CNN
F 2 "lib_fp:tht_vertical_potentiometer" H 3950 4150 50  0001 C CNN
F 3 "" H 3950 4150 50  0001 C CNN
	1    3950 4150
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:+5V #PWR010
U 1 1 5BC6691B
P 3950 3750
F 0 "#PWR010" H 3950 3600 50  0001 C CNN
F 1 "+5V" H 3950 3890 50  0000 C CNN
F 2 "" H 3950 3750 50  0001 C CNN
F 3 "" H 3950 3750 50  0001 C CNN
	1    3950 3750
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:GND #PWR011
U 1 1 5BC66921
P 3950 4550
F 0 "#PWR011" H 3950 4300 50  0001 C CNN
F 1 "GND" H 3950 4400 50  0000 C CNN
F 2 "" H 3950 4550 50  0001 C CNN
F 3 "" H 3950 4550 50  0001 C CNN
	1    3950 4550
	1    0    0    -1  
$EndComp
Text GLabel 4475 4150 2    60   Input ~ 0
A_IN_5
$Comp
L incur_board-rescue:POT RV3
U 1 1 5BC669D1
P 3950 5425
F 0 "RV3" V 3775 5425 50  0000 C CNN
F 1 "10k_pot" V 3850 5425 50  0000 C CNN
F 2 "lib_fp:tht_vertical_potentiometer" H 3950 5425 50  0001 C CNN
F 3 "" H 3950 5425 50  0001 C CNN
	1    3950 5425
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:+5V #PWR012
U 1 1 5BC669D7
P 3950 5025
F 0 "#PWR012" H 3950 4875 50  0001 C CNN
F 1 "+5V" H 3950 5165 50  0000 C CNN
F 2 "" H 3950 5025 50  0001 C CNN
F 3 "" H 3950 5025 50  0001 C CNN
	1    3950 5025
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:GND #PWR013
U 1 1 5BC669DD
P 3950 5825
F 0 "#PWR013" H 3950 5575 50  0001 C CNN
F 1 "GND" H 3950 5675 50  0000 C CNN
F 2 "" H 3950 5825 50  0001 C CNN
F 3 "" H 3950 5825 50  0001 C CNN
	1    3950 5825
	1    0    0    -1  
$EndComp
Text GLabel 4475 5425 2    60   Input ~ 0
A_IN_6
$Comp
L incur_board-rescue:POT RV4
U 1 1 5BC669E7
P 3950 6700
F 0 "RV4" V 3775 6700 50  0000 C CNN
F 1 "10k_pot" V 3850 6700 50  0000 C CNN
F 2 "lib_fp:tht_vertical_potentiometer" H 3950 6700 50  0001 C CNN
F 3 "" H 3950 6700 50  0001 C CNN
	1    3950 6700
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:+5V #PWR014
U 1 1 5BC669ED
P 3950 6300
F 0 "#PWR014" H 3950 6150 50  0001 C CNN
F 1 "+5V" H 3950 6440 50  0000 C CNN
F 2 "" H 3950 6300 50  0001 C CNN
F 3 "" H 3950 6300 50  0001 C CNN
	1    3950 6300
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:GND #PWR015
U 1 1 5BC669F3
P 3950 7100
F 0 "#PWR015" H 3950 6850 50  0001 C CNN
F 1 "GND" H 3950 6950 50  0000 C CNN
F 2 "" H 3950 7100 50  0001 C CNN
F 3 "" H 3950 7100 50  0001 C CNN
	1    3950 7100
	1    0    0    -1  
$EndComp
Text GLabel 4475 6700 2    60   Input ~ 0
A_IN_7
Text GLabel 5575 3425 0    39   Input ~ 0
A_IN_0
Text GLabel 5575 3525 0    39   Input ~ 0
A_IN_1
Text GLabel 5575 3625 0    39   Input ~ 0
A_IN_2
Text GLabel 5575 3725 0    39   Input ~ 0
A_IN_3
Text GLabel 5575 3825 0    39   Input ~ 0
A_IN_4
Text GLabel 5575 3925 0    39   Input ~ 0
A_IN_5
Text GLabel 5575 4025 0    39   Input ~ 0
A_IN_6
Text GLabel 5575 4125 0    39   Input ~ 0
A_IN_7
$Comp
L incur_board-rescue:GND #PWR016
U 1 1 5BC6B971
P 6675 4600
F 0 "#PWR016" H 6675 4350 50  0001 C CNN
F 1 "GND" H 6675 4450 50  0000 C CNN
F 2 "" H 6675 4600 50  0001 C CNN
F 3 "" H 6675 4600 50  0001 C CNN
	1    6675 4600
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:+5V #PWR017
U 1 1 5BC6BECB
P 6650 2925
F 0 "#PWR017" H 6650 2775 50  0001 C CNN
F 1 "+5V" H 6650 3065 50  0000 C CNN
F 2 "" H 6650 2925 50  0001 C CNN
F 3 "" H 6650 2925 50  0001 C CNN
	1    6650 2925
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:+3V3 #PWR018
U 1 1 5BC6DADF
P 7850 1275
F 0 "#PWR018" H 7850 1125 50  0001 C CNN
F 1 "+3V3" H 7850 1415 50  0000 C CNN
F 2 "" H 7850 1275 50  0001 C CNN
F 3 "" H 7850 1275 50  0001 C CNN
	1    7850 1275
	1    0    0    -1  
$EndComp
Text GLabel 8900 1900 2    60   Input ~ 0
RX
$Comp
L incur_board-rescue:GND #PWR019
U 1 1 5BC6E144
P 7850 2500
F 0 "#PWR019" H 7850 2250 50  0001 C CNN
F 1 "GND" H 7850 2350 50  0000 C CNN
F 2 "" H 7850 2500 50  0001 C CNN
F 3 "" H 7850 2500 50  0001 C CNN
	1    7850 2500
	1    0    0    -1  
$EndComp
Text GLabel 7325 3625 2    39   Input ~ 0
CLK
Text GLabel 7325 3725 2    39   Input ~ 0
D_OUT
Text GLabel 7325 3825 2    39   Input ~ 0
D_IN
Text GLabel 7325 3925 2    39   Input ~ 0
CS
$Comp
L incur_board-rescue:GND #PWR020
U 1 1 5BC72ABB
P 9300 5700
F 0 "#PWR020" H 9300 5450 50  0001 C CNN
F 1 "GND" H 9300 5550 50  0000 C CNN
F 2 "" H 9300 5700 50  0001 C CNN
F 3 "" H 9300 5700 50  0001 C CNN
	1    9300 5700
	1    0    0    -1  
$EndComp
Text GLabel 8675 4075 0    39   Input ~ 0
CLK
Text GLabel 8675 3875 0    39   Input ~ 0
D_OUT
Text GLabel 8675 3975 0    39   Input ~ 0
D_IN
Text GLabel 8675 3575 0    39   Input ~ 0
CS
Text GLabel 10700 5075 2    39   Input ~ 0
RX
$Comp
L incur_board-rescue:+3V3 #PWR021
U 1 1 5BC730AE
P 9800 2850
F 0 "#PWR021" H 9800 2700 50  0001 C CNN
F 1 "+3V3" H 9800 2990 50  0000 C CNN
F 2 "" H 9800 2850 50  0001 C CNN
F 3 "" H 9800 2850 50  0001 C CNN
	1    9800 2850
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:+5V #PWR022
U 1 1 5BC815CC
P 9500 2850
F 0 "#PWR022" H 9500 2700 50  0001 C CNN
F 1 "+5V" H 9500 2990 50  0000 C CNN
F 2 "" H 9500 2850 50  0001 C CNN
F 3 "" H 9500 2850 50  0001 C CNN
	1    9500 2850
	1    0    0    -1  
$EndComp
NoConn ~ 6250 825 
$Comp
L incur_board-rescue:Raspberry_Pi_2_3 J8
U 1 1 5C52F362
P 9700 4275
F 0 "J8" H 10400 3025 50  0000 C CNN
F 1 "2x20_Extra_Tall_Header" H 9375 5175 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical" H 10700 5525 50  0001 C CNN
F 3 "" H 9750 4125 50  0001 C CNN
	1    9700 4275
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:GND #PWR023
U 1 1 5C531C10
P 7825 5625
F 0 "#PWR023" H 7825 5375 50  0001 C CNN
F 1 "GND" H 7825 5475 50  0000 C CNN
F 2 "" H 7825 5625 50  0001 C CNN
F 3 "" H 7825 5625 50  0001 C CNN
	1    7825 5625
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:Conn_01x01 J6
U 1 1 5C531CE6
P 6900 5425
F 0 "J6" H 6900 5525 50  0000 C CNN
F 1 "Conn_01x01" H 6900 5325 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x01_Pitch2.54mm" H 6900 5425 50  0001 C CNN
F 3 "" H 6900 5425 50  0001 C CNN
	1    6900 5425
	-1   0    0    1   
$EndComp
NoConn ~ 8800 3675
NoConn ~ 8800 3775
NoConn ~ 8800 4175
NoConn ~ 8800 4275
NoConn ~ 8800 4375
NoConn ~ 8800 4475
NoConn ~ 8800 4575
NoConn ~ 8800 4675
NoConn ~ 8800 4975
NoConn ~ 8800 5075
NoConn ~ 9400 5575
NoConn ~ 9500 5575
NoConn ~ 9600 5575
NoConn ~ 9700 5575
NoConn ~ 9900 5575
NoConn ~ 10000 5575
NoConn ~ 9800 5575
NoConn ~ 10600 4975
NoConn ~ 10600 4775
NoConn ~ 10600 4675
NoConn ~ 10600 4475
NoConn ~ 10600 4375
NoConn ~ 10600 4275
NoConn ~ 10600 4175
NoConn ~ 10600 4075
NoConn ~ 10600 3875
NoConn ~ 10600 3775
NoConn ~ 10600 3575
NoConn ~ 10600 3475
NoConn ~ 10600 3375
NoConn ~ 9900 2975
$Comp
L incur_board-rescue:PWR_FLAG #FLG024
U 1 1 5C015DC5
P 9300 5600
F 0 "#FLG024" H 9300 5675 50  0001 C CNN
F 1 "PWR_FLAG" V 9300 5750 50  0000 L CNN
F 2 "" H 9300 5600 50  0001 C CNN
F 3 "" H 9300 5600 50  0001 C CNN
	1    9300 5600
	0    -1   -1   0   
$EndComp
$Comp
L incur_board-rescue:PWR_FLAG #FLG025
U 1 1 5C015C23
P 9425 2975
F 0 "#FLG025" H 9425 3050 50  0001 C CNN
F 1 "PWR_FLAG" V 9425 3125 50  0000 L CNN
F 2 "" H 9425 2975 50  0001 C CNN
F 3 "" H 9425 2975 50  0001 C CNN
	1    9425 2975
	0    -1   -1   0   
$EndComp
Connection ~ 6675 1875
Wire Wire Line
	5650 1875 6675 1875
Connection ~ 7850 2350
Wire Wire Line
	8025 2350 7850 2350
Wire Wire Line
	8025 2275 8025 2350
Wire Wire Line
	8025 1675 7600 1675
Wire Wire Line
	8025 1975 8025 1675
Wire Wire Line
	7850 1975 7600 1975
Wire Wire Line
	7850 1975 7850 2350
Connection ~ 8600 1900
Wire Wire Line
	8600 1575 8600 1900
Wire Wire Line
	8475 1575 8600 1575
Wire Wire Line
	7600 1900 7600 1875
Wire Wire Line
	7600 1900 8600 1900
Connection ~ 7850 1575
Wire Wire Line
	7850 1275 7850 1575
Wire Wire Line
	7600 1575 7850 1575
Connection ~ 6675 3075
Wire Wire Line
	6375 3075 6675 3075
Wire Wire Line
	6375 3225 6375 3075
Wire Wire Line
	6675 2925 6650 2925
Wire Wire Line
	6675 2925 6675 3075
Connection ~ 6675 4450
Wire Wire Line
	6375 4450 6675 4450
Wire Wire Line
	6375 4325 6375 4450
Wire Wire Line
	6675 4325 6675 4450
Wire Wire Line
	5875 4125 5575 4125
Wire Wire Line
	5575 4025 5875 4025
Wire Wire Line
	5875 3925 5575 3925
Wire Wire Line
	5575 3825 5875 3825
Wire Wire Line
	5875 3725 5575 3725
Wire Wire Line
	5575 3625 5875 3625
Wire Wire Line
	5875 3525 5575 3525
Wire Wire Line
	5575 3425 5875 3425
Wire Wire Line
	4475 6700 4100 6700
Wire Wire Line
	3950 7100 3950 6850
Wire Wire Line
	3950 6300 3950 6550
Wire Wire Line
	4475 5425 4100 5425
Wire Wire Line
	3950 5825 3950 5575
Wire Wire Line
	3950 5025 3950 5275
Wire Wire Line
	4475 4150 4100 4150
Wire Wire Line
	3950 4550 3950 4300
Wire Wire Line
	3950 3750 3950 4000
Wire Wire Line
	2475 5650 2725 5650
Connection ~ 1500 6025
Wire Wire Line
	1100 5850 1100 6025
Wire Wire Line
	1500 5750 1500 6025
Wire Wire Line
	1100 6025 1500 6025
Connection ~ 1950 5650
Wire Wire Line
	1950 5575 1950 5650
Wire Wire Line
	1950 5125 1950 5275
Wire Wire Line
	1500 5650 1950 5650
Wire Wire Line
	2450 4175 2700 4175
Connection ~ 1475 4550
Wire Wire Line
	1075 4375 1075 4550
Wire Wire Line
	1475 4275 1475 4550
Wire Wire Line
	1075 4550 1475 4550
Connection ~ 1925 4175
Wire Wire Line
	1925 4100 1925 4175
Wire Wire Line
	1925 3650 1925 3800
Wire Wire Line
	1475 4175 1925 4175
Wire Wire Line
	2450 2675 2700 2675
Connection ~ 1475 3050
Wire Wire Line
	1075 2875 1075 3050
Wire Wire Line
	1475 2775 1475 3050
Wire Wire Line
	1075 3050 1475 3050
Connection ~ 1925 2675
Wire Wire Line
	1925 2600 1925 2675
Wire Wire Line
	1925 2150 1925 2300
Wire Wire Line
	1475 2675 1925 2675
Wire Wire Line
	4475 2875 4100 2875
Wire Wire Line
	3950 3275 3950 3025
Wire Wire Line
	3950 2475 3950 2725
Wire Wire Line
	2425 1200 2675 1200
Connection ~ 1450 1575
Wire Wire Line
	1050 1400 1050 1575
Wire Wire Line
	1450 1300 1450 1575
Wire Wire Line
	1050 1575 1450 1575
Connection ~ 1900 1200
Wire Wire Line
	1900 1125 1900 1200
Wire Wire Line
	1450 1200 1900 1200
Wire Wire Line
	7325 3625 7075 3625
Wire Wire Line
	7325 3725 7075 3725
Wire Wire Line
	7325 3825 7075 3825
Wire Wire Line
	7325 3925 7075 3925
Wire Wire Line
	6425 1525 6675 1525
Wire Wire Line
	7000 1525 7000 1675
Wire Wire Line
	9300 5575 9300 5600
Wire Wire Line
	8675 3575 8800 3575
Wire Wire Line
	8675 3875 8800 3875
Wire Wire Line
	8675 3975 8800 3975
Wire Wire Line
	8675 4075 8800 4075
Wire Wire Line
	10600 5075 10700 5075
Wire Wire Line
	7100 5425 7625 5425
Connection ~ 9300 5600
Wire Wire Line
	9800 2975 9800 2850
$Comp
L incur_board-rescue:+5V #PWR026
U 1 1 5BC5E6F9
P 1900 675
F 0 "#PWR026" H 1900 525 50  0001 C CNN
F 1 "+5V" H 1900 815 50  0000 C CNN
F 2 "" H 1900 675 50  0001 C CNN
F 3 "" H 1900 675 50  0001 C CNN
	1    1900 675 
	1    0    0    -1  
$EndComp
Wire Wire Line
	1900 675  1900 825 
NoConn ~ 9600 2975
Wire Wire Line
	9500 2975 9425 2975
Wire Wire Line
	9500 2975 9500 2850
Connection ~ 9500 2975
$Comp
L Connector:Conn_Coaxial J7
U 1 1 5C53771A
P 7825 5425
F 0 "J7" H 7725 5575 50  0000 L BNN
F 1 "rca" H 7900 5550 50  0000 L BNN
F 2 "lib_fp:tht_rca_vertical" H 7825 5425 50  0001 L BNN
F 3 "CUI Inc" H 7825 5425 50  0001 L BNN
F 4 "Manufacturer recommendations" H 7825 5425 50  0001 L BNN "Field4"
F 5 "B" H 7825 5425 50  0001 L BNN "Field5"
	1    7825 5425
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:Audio-Jack-2_Switch J1
U 1 1 5C85719A
P 1250 1300
F 0 "J1" H 1200 1475 50  0000 C CNN
F 1 "mono_jack_3.5mm" H 1475 1225 50  0000 C CNN
F 2 "Connections_Thonkiconn:Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles" H 1500 1400 50  0001 C CNN
F 3 "" H 1500 1400 50  0001 C CNN
	1    1250 1300
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:Audio-Jack-2_Switch J2
U 1 1 5C8572E2
P 1275 2775
F 0 "J2" H 1225 2950 50  0000 C CNN
F 1 "mono_jack_3.5mm" H 1500 2700 50  0000 C CNN
F 2 "Connections_Thonkiconn:Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles" H 1525 2875 50  0001 C CNN
F 3 "" H 1525 2875 50  0001 C CNN
	1    1275 2775
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:Audio-Jack-2_Switch J3
U 1 1 5C85775E
P 1275 4275
F 0 "J3" H 1225 4450 50  0000 C CNN
F 1 "mono_jack_3.5mm" H 1500 4200 50  0000 C CNN
F 2 "Connections_Thonkiconn:Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles" H 1525 4375 50  0001 C CNN
F 3 "" H 1525 4375 50  0001 C CNN
	1    1275 4275
	1    0    0    -1  
$EndComp
$Comp
L incur_board-rescue:Audio-Jack-2_Switch J4
U 1 1 5C857A0C
P 1300 5750
F 0 "J4" H 1250 5925 50  0000 C CNN
F 1 "mono_jack_3.5mm" H 1525 5675 50  0000 C CNN
F 2 "Connections_Thonkiconn:Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles" H 1550 5850 50  0001 C CNN
F 3 "" H 1550 5850 50  0001 C CNN
	1    1300 5750
	1    0    0    -1  
$EndComp
NoConn ~ 6550 1125
NoConn ~ 5950 1125
Wire Wire Line
	6675 1575 6675 1525
Connection ~ 6675 1525
Wire Wire Line
	5950 1025 5850 1025
Wire Wire Line
	5850 1025 5850 1525
Wire Wire Line
	5850 1525 6125 1525
Wire Wire Line
	5650 1875 5650 775 
Wire Wire Line
	5650 775  6550 775 
Wire Wire Line
	6550 775  6550 1025
Wire Wire Line
	6675 1875 7000 1875
Wire Wire Line
	7850 2350 7850 2500
Wire Wire Line
	8600 1900 8900 1900
Wire Wire Line
	7850 1575 8175 1575
Wire Wire Line
	6675 3075 6675 3225
Wire Wire Line
	6675 4450 6675 4600
Wire Wire Line
	1500 6025 1500 6250
Wire Wire Line
	1500 6025 1950 6025
Wire Wire Line
	1950 5650 1950 5725
Wire Wire Line
	1950 5650 2175 5650
Wire Wire Line
	1475 4550 1475 4775
Wire Wire Line
	1475 4550 1925 4550
Wire Wire Line
	1925 4175 1925 4250
Wire Wire Line
	1925 4175 2150 4175
Wire Wire Line
	1475 3050 1475 3275
Wire Wire Line
	1475 3050 1925 3050
Wire Wire Line
	1925 2675 1925 2750
Wire Wire Line
	1925 2675 2150 2675
Wire Wire Line
	1450 1575 1450 1800
Wire Wire Line
	1450 1575 1900 1575
Wire Wire Line
	1900 1200 1900 1275
Wire Wire Line
	1900 1200 2125 1200
Wire Wire Line
	9300 5600 9300 5700
Wire Wire Line
	6675 1525 7000 1525
Text Notes 7625 5200 0    60   ~ 0
video out
$EndSCHEMATC
