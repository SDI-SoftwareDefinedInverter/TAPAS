# TAPAS
Community drives inverter project

## Differences between the TAPAS developer-version and TAPAS version 1.0
+ Pin 4 of the JTAG-Interface-Connector SV2 is not connected to GND in the developer version, this has been fixed to version 1.0. You have to solder Pin 4 of SV2 to GND by hand, to be able to flash the DSP.
+ version 1.0 has more PINs of the Raspberry-Pi socket (SV4) connected to GND, in the developer-version, only the Pins 34 and 39 were connected to GND. Therefore, you cannot use a Nano Pi on this socket, as the GND connection to TAPAS is missing then.
+ The SPI-Chip Select on GPIO53 of the DSP that is connected to SV4 via the address DIP-switch(2) is connected to Pin 26 of SV4 in the development-version and is now moved to Pin 16 in TAPAS V1.0
+ The resistor R\_MISO\_1 is populated in the development-version of TAPAS, but not in version 1.0 any more, here you can solder one by hand, if needed.
+ The resistors R\_TXA1, R\_RXA1, R\_TXB1 and R\_RXB1 are all populated in the development-version, but not in version 1.0 any more, solder in by hand, if you need one of them
+ The gate-driving resistors R19, R23, R20, R24, R12, R14, R16, R15, R17, R18, R22, R21 are implemented as 0 Ohm in the development version and have now been changed to 2,2Ohm in TAPAS vesion 1.0

## TAPAS Quick-Start Guide
Use your TAPAS board with Raspberry PI and TI InstaSPIN

SIEMENS AG - July 2017 

Document version 0.1

__CAUTION__

The TAPAS community inverter board is not a toy! It is intended for
laboratory use only. Never use it in a productive environment!	
(see section 6)

The TAPAS board can get very hot never touch the board during	
operation. Always use an appropriate case.

If the TAPAS board is used in conjunction with mechanical,	
electromagnetic, acoustic, optical or other components, e.g. a motor	
drive, significant forces can occur. Always ensure safety of the	
entire set-up! Prevent direct physical contact, always place set-up	
in an appropriate case, employ safe software techniques (e.g. torque	
limiting) and limit the supply current.

The device is very sensitive to electrostatic discharge, handle with	
care! Never touch the board if the supply voltage is turned on!

 
## Foreword and acknowledgements

This board (TAPAS) is intended to train the next generation of power 
electronics researchers and (application) engineers. It is designed as an 
educational platform that addresses enthusiasts as well as scholars in
university and industry. 

TAPAS features a 48V, 3-phase GaN power stage with on-board filters. This
design-choice allows for a very high switching frequency/bandwidth (500kHz 
and beyond) whilst producing a smooth output wave-form. In contrast, 
commonly available IGBT or MOSFET converter boards typically have a 
limited bandwidth and/or produce a square output wave-form.

This unique feature of high bandwidth and smooth output makes TAPAS to 
some degree universal, giving rise to educational applications in AC and DC 
drives, DC/DC power conversion, audio, robotics, magnetic field control, DC-
battery charging, etc. Note that universality is achieved with a single, fixed 
hardware platform where the overall functionality is defined via software 
(changes) only – the reason why we coined the term “Software Defined 
Inverter” (SDI). 

TAPAS is Raspberry PI compatible and multiple boards can be used in 
collaboration, giving rise to many-phase applications such as quadrocopters 
or multi-axis servo control. Together with open-source code examples and 
extensive documentation we made TAPAS as accessible to the community as 
possible.

To help us make TAPAS also affordable, we would like to thank our friends 
and partners at Texas Instruments, Efficient Power Conversion (EPC), Würth 
Elektronik and Allegro Micro who sponsored most of the active and passive 
components on the board (see bill of materials). I hope you will have as much 
fun with TAPAS as we had making it.


						Dominic Buchstaller
					(Concept and  lead-design - TAPAS)


(is adding the logos here ok ? )
