# SDI TAPAS
Community drives inverter project

---

## Differences between the TAPAS developer-version and TAPAS version 1.0
+ Pin 4 of the JTAG-Interface-Connector SV2 is not connected to GND in the developer version, this has been fixed to version 1.0. You have to solder Pin 4 of SV2 to GND by hand, to be able to flash the DSP.
+ version 1.0 has more PINs of the Raspberry-Pi socket (SV4) connected to GND, in the developer-version, only the Pins 34 and 39 were connected to GND. Therefore, you cannot use a Nano Pi on this socket, as the GND connection to TAPAS is missing then.
+ The SPI-Chip Select on GPIO53 of the DSP that is connected to SV4 via the address DIP-switch(2) is connected to Pin 26 of SV4 in the development-version and is now moved to Pin 16 in TAPAS V1.0
+ The resistor R\_MISO\_1 is populated in the development-version of TAPAS, but not in version 1.0 any more, here you can solder one by hand, if needed.
+ The resistors R\_TXA1, R\_RXA1, R\_TXB1 and R\_RXB1 are all populated in the development-version, but not in version 1.0 any more, solder in by hand, if you need one of them
+ The gate-driving resistors R19, R23, R20, R24, R12, R14, R16, R15, R17, R18, R22, R21 are implemented as 0 Ohm in the development version and have now been changed to 2,2Ohm in TAPAS vesion 1.0

---

### TAPAS Quick-Start Guide
Use your TAPAS board with Raspberry PI and TI InstaSPIN

SIEMENS AG - July 2017 

Document version 0.1

__CAUTION__

__The TAPAS community inverter board is not a toy!__ It is __intended for
laboratory use only. Never use it in a productive environment!__
(see section 6)

The TAPAS board can get __very - hot never touch the board during	
operation. Always use an appropriate case.__

__If the TAPAS board is used in conjunction with mechanical,
electromagnetic, acoustic, optical or other components,__ e.g. a motor
drive, __significant forces can occur. Always ensure safety of the
entire set-up! Prevent direct physical contact, always place set-up
in an appropriate case, employ safe software techniques__ (e.g. torque
limiting) and __limit the supply current.__

The device is very __sensitive to electrostatic discharge - handle with	
care! Never touch the board if the supply voltage is turned on!__

 
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

1. INTRODUCTION	

This quick-start-guide will lead you through the necessary steps to get TAPAS
up and running with most commercially available DC-brushless motors.
If you are new to Texas Instrument DSPs or power conversion, we advise you	
to start with this guide. It will take you through the necessary steps to set-up 
your (coding) environment and bring the board to life. You are then free to
explore the endless possibilities that the platform provides.

### TAPAS key characteristics
+ DC-Input 12V ¿ 48V
+ Maximum DC / AC (per phase) current - 30A
+ Up to 300W continuous power - passively cooled (@>120kHz switching frequency)
+ Switching frequency up to 600 kHz at reduced load
+ On-board output-filter for sinusoidal AC output
+ Texas Instruments C2000 Piccolo (TMS320F28069M) DSP - InstaSPIN-enabled
+ CAN, GPIO, UART, SPI, 2 x QEP (encoder) interface onboard
+ Raspberry-Pi compatible

### Box contents
+ TAPAS board
+ This quick-start guide
+ An SDI sticker
+ 7 (optional) board-connectors (JP7, JP10, JP11, JP13, JP14, SV3, SV4) for hand-soldering

### Required materials 
To get started with TAPAS you will need the following (additional) items.

+ We highly recommend placing TAPAS in __a case__. This will keep your TAPAS board safe.
The 3D model for our very own case can be found and downloaded here:
<https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/TAPAShousing.zip>	
The archive contains multiple files for e.g. the bottom part and the lid of the case.
If you don¿t own a 3D printer, many local 3D printing services are available on-line.
Print in ABS.				
+ __DC power supply__ with minimum 12V and >3A continuous current output.
Alternatively, you may use any battery with the correct voltage and an appropriate
fuse in the supply line	
+ A __DC brushless motor__	
+ If you want to use TAPAS with __Raspberry PI__ we recommend an Raspberry PI Zero (W)
+ If you want to start programming with TAPAS you will need a __JTAG programmer__.
We recommend using the OLIMEX TMS320-JTAG-USB XDS100-V2
+ If you want to use the TAPAS platform with a Raspberry Pi, you may also want to
fasten the two PCBs together. Then you will need
	+ 4 screws M2,5 x 6mm (plastic)	
	+ 4 screw nuts M2,5 (plastic)
	+ 4 spacers M2,5 x 10mm with one male and one female thread (plastic)
	+ 12 washers M2,5 (plastic)

2. GETTING STARTED WITH TAPAS AND RASPBERRY PI

+ Create an SD-Card image for your Raspberry Pi Zero (W)
(<https://www.raspberrypi.org/documentation/installation/installing-images/>)
+ Insert SD card in Raspberry PI Zero (W) and check that the Raspberry PI boots to a command prompt
+ Make sure that you have a working Python 3.0 and git installation

```
python --version
git --version
```
+ Get the TAPAS software and documentation package from 
<https://github.com/SDI-SoftwareDefinedInverter/TAPAS>
and place it into your home folder

```
cd
git clone https://github.com/SDI-SoftwareDefinedInverter/TAPAS.git
```
+ If successful, halt your Raspberry PI

```
sudo halt
```
+ Set the SPI-Address select DIP switch to (OFF)-(ON)-(OFF)-(OFF) for the switch 
positions from (1) - (4) (see pinout)
+ Disconnect the Raspberry PI from any power source and plug it into the TAPAS
Raspberry PI board connector (see pinout).
+ Connect your TAPAS board to a DC power supply and to a DC brushless motor (see pinout).
+ Set the supply voltage to 12V with 3A current limit and turn it on.
+ Log into your Raspberry PI and type

```
cd ~/TAPAS
python3 TAPASstart.py
```
+ Then follow the prompts on the monitor.

3. GETTING STARTED WITH TAPAS AND CODE COMPOSER STUDIO

__CAUTION__	

__The stock TAPAS firmware implements software features that ensure safe operation.
Changing the stock TAPAS firmware may damage or destroy your TAPAS board, lead to
harm and/or danger. Make sure that you fully understand the supplied sample code and
the underlying principles before flashing your own firmware.__

For programming the TAPAS-Board, we recommend Code Composer Studio from Texas Instruments.
It is free of charge and can be downloaded from here:

<http://processors.wiki.ti.com/index.php/Download_CCS>

Choose the correct setup-package for your OS and install it following the instructions in
theinstallation-wizard.

The drivers for the OLIMEX JTAG-Debug probe are included in the standard installation
package. If you choose a JTAG Programmer from another vendor make sure that you installed
the correct drivers and that it is compatible with code composer studio.


To be able to use the InstaSpin capabilities of the DSP, you require motorware version
1\_01\_00\_16. Install git for your operating system and clone the repository in the same
way, you did it for the Raspberry Pi calling

```
git clone https://github.com/SDI-SoftwareDefinedInverter/TAPAS.git
```

Motorware is only available as a windows installer executable also included in the 
previously cloned repository in the file _`motorware.zip`_.

Alternatively you can download the archive with the windows installer via a browser here:
<https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/motorware.zip>

As the TAPAS board definition is not contained in motorware per default and TAPAS has some
additional features, compared to most of the development-kits from TI, some modifications
to your motorware installation have to be done before being able to do firmware-development
for this platform. These modifications basically include inserting some additional drivers 
and replacing existing modules, that are for example needed for the external IO of the board.	

All the necessary changes to motorware can be done automatically by using our patch-file
_`SDITAPASmotorwarePatch.patch`_ included in the previously cloned repository.

If you use git in bash-mode, you have a possibility to run the patch command for changing
your motorware-installation under windows.
Copy the file _`SDITAPASmotorwarePatch.patch`_ to the motorware installation folder
(usually _`C:\ti\`_), start git in bash mode in this folder and execute the following commands:

```
dos2unix SDITAPASmotorwarePatch.patch
patch -p0 -i SDITAPASmotorwarePatch.patch
```

If this command has finished execution successfully, you can start with the motorware-labs
and the quick-start demo firmware. To edit the quick-start project, start Code Composer 
Studio and choose a workspace location. Close the welcome-window and then select 
"Project-\>Import CCS Projects..." In the upcoming window choose the option "Select search-directory"
and click the "Browse" - button. Navigate to the directory of your motorware installation,
go to the folder
_`<drive>:\ti\motorware\motorware\_1\_01\_00\_16\sw\solutions\instaspin\_foc\boards\TAPAS\_V1\_0\f28x\f2806xF\projects\ccs5\ `_
and click the "OK" button.

In the "Discovered projects" - list below you will see all the projects lying in the selected directory.
Here, you can choose for example the project _"TAPAS\_quick\_start"_, which represents the demo firmware used with the python - 
script for the Raspberry PI.

For all the other projects in the folders
_`<drive>:\ti\motorware\motorware\_1\_01\_00\_16\sw\solutions\instaspin\_foc\boards\TAPAS\_V1\_0\f28x\f2806xF\projects\ccs5\ `_
and
_`<drive>:\ti\motorware\motorware\_1\_01\_00\_16\sw\solutions\instaspin\_motion\boards\TAPAS\_V1\_0\f28x\f2806xF\projects\ccs5\ `_

please have a look at the _"InstaSPIN Projects and Labs User's Guide"_ which comes together with the motorware-installation 
and is located at
_`<drive>:\ti\motorware\motorware\_1\_01\_00\_16\docs\labs\instaspin\_labs.pdf`_ with a standard-motorware installation.
There you can further find some information how to compile the firmware, start a debugging session, flash the DSP and get an
impression, what all the program components actually do. Please keep in mind, that all the labs for driving two motors independent
with one DSP are not possible with TAPAS, as there is only one 3-phase power stage.

To be able to run our TAPAS demo-webapp you also require the InstaSPIN-UNIVERSALGUI from Texas Instruments which you can get here:

<http://www.ti.com/tool/INSTASPINUNIVERSALGUI>

You have now completed the installation of the TAPAS development environment. We have created a TAPAS-webapp including not only	
external IO for you to check if everything is working ok. Download it here:	

```
https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/TAPASwebapp.zip
```
unzip it and place it in the folder:

```
<drive>:\ti\guicomposer\webapps\
```

__And now? How do we get it running?__

If you plan to do unlock even more features of TAPAS, we recommend installing the Texas Instruments controlSUITE which is available here:

<http://www.ti.com/tool/controlsuite>

It delivers a lot of ready-to-use peripheral-drivers and examples for the C2000DSP series.

Here comes the pinout for the TAPAS-board:
![TAPAS-pinout](https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/images/TAPAS_V1.0%20-%20Pinout.png "Figure1 : TAPAS pinout")


4. FREQUENTLY ASKED QUESTIONS / TROUBLE SHOOTING

Q: Where can I get a TAPAS board 

A: You can get one here: <http://xxx>	


Q: Can I use other JTAG-Programmers than the OLIMEX?

A: Yes you can. As long as it's 3,3V compatible and supported by Code Composer Studio it should work.


Q: Can I run the board at full power for longer periods of time?

A: Yes you can. In that case it is important to manage the board temperature. We recommend adding some temperature monitoring code (see examples)
and dynamically limit the output current. Keep the board temperature below 90°C at all times to keep your TAPAS board healthy.


Q: If I abruptly reduce the speed of my motor why is the JTAG-connection interrupted or other funny things happen?

A: It is very likely that you are using a DC power supply and not a battery to power TAPAS. The breaking energy is fed back into the DC supply and
causes an abrupt rise in DC voltage. Note that although TAPAS is designed to absorb some breaking energy, excessive DC voltage peaks may damage the
board. To prevent this effect, limit the rate of change in motor velocity, use a battery instead of a DC power supply or invest in a current sink
(breaking chopper).

5. REFERENCES

The following documents can be helpful in developing with TAPAS:

+ TAPAS Pinout: 
<https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/TAPAS-Pinout.pdf>	
+ TAPAS Schematics: 
<https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/TAPAS-Schematic.pdf>
+ This 13document(quick start guide):
<https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/TAPASquickStartGuide.pdf>
+ InstaSPIN-FOC and InstaSPIN-MOTION user guide : 
<http://www.ti.com/lit/ug/spruhj1g/spruhj1g.pdf>
+ Instaspin projects and labs user's guide 
-\> see motorware (<drive>:\ti\motorware\motorware\_1\_01\_00\_16\docs\labs\instaspin\_labs.pdf)
+ TMS320F28069MPZT overview and datasheet: 
<http://www.ti.com/lit/ug/spruh18g/spruh18g.pdf>
