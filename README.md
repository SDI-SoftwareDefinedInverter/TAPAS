## SDI TAPAS - Community Inverter - Quick-Start Guide

![PCB](images/FIKAT_all_small.JPG "PCB")

Use your TAPAS board with Raspberry PI or Texas Instruments InstaSPIN

__!CAUTION!__

__The TAPAS community inverter board is not a toy!__ It is __intended for
laboratory use only. Never use it in a productive environment!__
(see section 6)

The TAPAS board can get __very hot, never touch the board during	
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
electronics researchers and (application) engineers.
It is designed as an educational platform that addresses enthusiasts as well as experts at
universities and in the industry. 

TAPAS features a 48V, 3-phase GaN power stage with on-board filters. This
design-choice allows for a high switching frequency/bandwidth (300kHz 
and beyond) whilst producing a smooth output wave-form. In contrast, 
commonly available IGBT or MOSFET converter boards typically have a 
rather limited bandwidth and/or produce a square output wave-form.

This unique feature of high bandwidth and smooth output makes TAPAS to 
some degree universal, giving rise to educational applications in AC and DC 
drives, DC/DC power conversion, audio, robotics, magnetic field control, 
battery charging, etc. Note that universality is achieved with a single, fixed 
hardware platform where the overall functionality is defined via software 
(changes) only – the reason why we coined the term “Software Defined 
Inverter” (SDI). 

TAPAS is Raspberry PI compatible and multiple boards can be used in 
collaboration, giving rise to many-phase applications such as quadrocopters 
or multi-axis servo control. Together with open-source code examples and 
extensive documentation we made TAPAS as accessible to the community as 
possible.

To help us make TAPAS affordable, we would like to thank our friends 
and partners at Texas Instruments, Efficient Power Conversion (EPC), Würth 
Elektronik and Allegro Micro who sponsored most of the active and passive 
components on the board (see bill of materials). I hope you will have as much 
fun with TAPAS as we had making it.

Dominic Buchstaller (concept & lead-design - TAPAS)

__Created by :__

![SIEMENS LOGO](images/siemens_logo_vsmall.png "SIEMENS LOGO")

_SIEMENS SDI (Software Defined Inverter)_ \* in-house start-up for I/Os

__Components sponsored by:__


![SPONSORS LOGO](images/logobar_small.jpg "SPONSORS LOGO")


_Texas Instruments_ <http://www.ti.com>

_Efficient power conversion (EPC)_ <http://epc-co.com>

_WÜRTH ELEKTRONIK_ <http://www.we-online.com>

_Allegro Microsystems_ <http://www.allegromicro.com>

## 1. INTRODUCTION	

This quick-start-guide will lead you through the necessary steps to get TAPAS
up and running with most commercially available DC-brushless motors.
If you are new to Texas Instrument DSPs or power conversion, we advise you	
to start with this guide. It will take you through the necessary steps to set-up 
your (coding) environment and bring the board to life. You are then free to
explore the endless possibilities that the platform provides.

### TAPAS key characteristics
+ DC-Input 12V - 48V
+ Maximum DC / AC (per phase) current - 30A
+ Up to 300W continuous power - passively cooled (@>120kHz switching frequency)
+ Switching frequency up to 600 kHz at reduced load
+ On-board output-filter smooth output voltage
+ Texas Instruments C2000 Piccolo (TMS320F28069M) DSP - InstaSPIN-enabled
+ CAN, GPIO, UART, SPI, 2 x QEP (encoder) interface onboard
+ Raspberry-Pi compatible

### TAPAS pinout
![TAPAS PINOUT](images/TAPAS_V1.0%20-%20Pinout.png "Figure1 : TAPAS pinout")

### Box contents
+ TAPAS board
+ This quick-start guide
+ An SDI sticker
+ 7 (optional) board-connectors (JP7, JP10, JP11, JP13, JP14, SV3, SV4) for hand-soldering

### Required materials 
To get started with TAPAS you will need the following (additional) items.

+ We highly recommend placing TAPAS in __a case__. This will keep your TAPAS board safe.
The 3D model for our very own case can be found and downloaded here:
<https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/TAPAShousing.zip>. 
If you don't own a 3D printer, many local 3D printing services are available on-line.
Print with temperature-stable materials like ABS (not PLA).				
+ __DC power supply__ with a minimum of 12V and >3A continuous current output.
Alternatively, you may use any battery with the correct voltage and an appropriate
fuse in the supply line	
+ A __DC brushless motor__	
+ If you want to start programming with TAPAS you will need a __JTAG programmer__.
We recommend using the OLIMEX TMS320-JTAG-USB XDS100-V2
+ If you want to use TAPAS with __Raspberry PI__ we recommend a Raspberry PI Zero (W)
+ If you want to use TAPAS with __Raspberry PI__ we also recommend the following parts for mechanical stability: 
	+ 4 screws M2,5 x 6mm (plastic)	
	+ 4 screw nuts M2,5 (plastic)
	+ 4 spacers M2,5 x 10mm with one male and one female thread (plastic)
	+ 12 washers M2,5 (plastic)

	
### Note: Difference between FIKAT (TAPAS pre-release version) and TAPAS (release version)
There are some PCB differences between the pre-release version (code-name FIKAT - PCB with Siemens & SDI logo) and release version 1.0 (code-name TAPAS - PCB with Siemens and manufacturer logos)

+ The connector of the OLIMEX programmer does not fit directly to the JTAG-interface connector SV2 on the FIKAT-board, you have
to solder an adapter here for being able to program the DSP on the board. The pinning of SV2 on FIKAT does match with the one of 
the programmers' connector. This has been fixed for TAPAS V1.0  
+ TAPAS has more PINs of the Raspberry-Pi socket (SV4) connected to GND. On FIKAT only pins 34 and 39 are connected to GND. Hence 
you cannot use a Nano Pi with FIKAT as the GND connection is missing.
+ The SPI-Chip select signal (GPIO53) is connected to pin26 of SV4 via the address DIP-switch (2) on FIKAT. This has moved to pin 
16 of SV4 on TAPAS.
+ The resistor R\_MISO\_1 is populated on FIKAT but not on TAPAS. 
+ The resistors R\_TXA1, R\_RXA1, R\_TXB1 and R\_RXB1 are populated on FIKAT but not on TAPAS.
+ The 0Ohm gate resistors R19, R23, R20, R24, R12, R14, R16, R15, R17, R18, R22, R21 on FIKAT have been changed to 2,2Ohm on 
TAPAS
+ The DC-bus capacitor C10 for the 5V-voltage regulator U99 has been upgraded from a standard SMD-electrolytic type on FIKAT to a 
39µF polymer type on TAPAS. It can now handle a higher DC ripple current on the dc-bus
+ We added a TVS-clamping-diode for DC over voltage protection on TAPAS. (Not available on FIKAT). This is to absorb some of the 
breaking energy if the user forgot to use a breaking chopper
+ The isolation ICs IC5, IC6 and IC7 on FIKAT have been swapped for a different type on TAPAS  - this should have no influence on 
the behaviour


## 2. GETTING STARTED WITH TAPAS AND RASPBERRY PI

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

## 3. GETTING STARTED WITH TAPAS AND CODE COMPOSER STUDIO

__!CAUTION!__	

__The stock TAPAS firmware implements software features that ensure safe operation.
Changing the stock TAPAS firmware may damage or destroy your TAPAS board, lead to
harm and/or danger. Make sure that you fully understand the supplied sample code and
the underlying principles before flashing your own firmware.__

For programming the TAPAS-Board, we recommend Code Composer Studio from Texas Instruments.
It is free of charge and can be downloaded from here:

<http://processors.wiki.ti.com/index.php/Download_CCS>

Choose the correct setup-package for your OS and install it following the instructions in
the installation-wizard.

The drivers for the OLIMEX JTAG-Debug probe are included in the standard installation
package. If you choose a JTAG Programmer from another vendor make sure that you installed
the correct drivers and that it is compatible with code composer studio.


To be able to use the InstaSpin capabilities of the DSP, you require motorware version
1\_01\_00\_16. Install git for your operating system and clone the repository in the same
way, you did it for the Raspberry Pi:

```
git clone https://github.com/SDI-SoftwareDefinedInverter/TAPAS.git
```



We included a copy of TI motorware in the cloned repository (_`motorware.zip`_). Alternatively you can download motorware from Motorware or here <https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/motorware.zip>.

As the TAPAS board definition is not part of the stock motorware package we have to make some modifications to it. All the necessary changes are contained in the patch-file _`SDITAPASmotorwarePatch.patch`_. Now copy _`SDITAPASmotorwarePatch.patch`_ to the motorware installation folder (usually _`C:\ti\`_) and start git in bash mode (also in the motorware installation folder). Then execute the following commands:

```
dos2unix SDITAPASmotorwarePatch.patch
patch -p0 -i SDITAPASmotorwarePatch.patch
```

This completes the installation of motorware und you can start playing with the motorware-labs
and the quick-start demo firmware. To add the quick-start project, start Code Composer 
Studio and choose a workspace location. Close the welcome-window and then select 
"Project-\>Import CCS Projects..." In the upcoming window choose the option "Select search-directory"
and click the "Browse" - button. Navigate to the directory of your motorware installation,
go to the folder
_`<drive>:\ti\motorware\motorware_1_01_00_16\sw\solutions\instaspin  
_foc\boards\TAPAS_V1_0\f28x\f2806xF\projects\ccs5\`_
and click the "OK" button.

In the "Discovered projects" - list below you will see all the projects in the selected directory.
Here you can choose, for example, the _"TAPAS\_quick\_start"_ project which represents the stock demo firmware to be used with the python - script for Raspberry PI.

For all the other projects in the folders
_`<drive>:\ti\motorware\motorware_1_01_00_16\sw\solutions\instaspin_foc\boards\TAPAS_V1_0\f28x\f2806xF\projects\ccs5\ `_
and
_`<drive>:\ti\motorware\motorware_1_01_00_16\sw\solutions\instaspin_motion\boards\TAPAS_V1_0\f28x\f2806xF\projects\ccs5\ `_

please consider the _"InstaSPIN Projects and Labs User's Guide"_ which comes with the motorware-installation 
and is located in _`<drive>:\ti\motorware\motorware_1_01_00_16\docs\labs\instaspin_labs.pdf`_ of the motorware installation.
There you can find further information on how to compile the firmware, start a debugging session, flash the DSP and get an
impression, what all the program components actually do. Please keep in mind that all labs are designed to drive two motors independently - this is not possible with TAPAS as there is only one 3-phase power stage.

To be able to run our TAPAS demo-webapp you also require the InstaSPIN-UNIVERSALGUI from Texas Instruments which you can get here:

<http://www.ti.com/tool/INSTASPINUNIVERSALGUI>

You have now completed the installation of the TAPAS development environment. We have also created a TAPAS-webapp to test all external I/O hardware. You can download it from:	

```
https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/TAPASwebapp.zip
```
Unzip the file place it in:

```
<drive>:\ti\guicomposer\webapps\
```



## 4. FREQUENTLY ASKED QUESTIONS / TROUBLE SHOOTING

Q: Where can I get a TAPAS board 

A: For now drop a board request in the issues tracker. We will update update this section if more boards become available.


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

## 5. REFERENCES

The following documents can be helpful in developing with TAPAS:

+ TAPAS Pinout: 
<https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/TAPAS-Pinout.pdf>	
+ TAPAS Schematics: 
<https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/TAPAS-Schematic.pdf>
+ This 13document(quick start guide):
<https://github.com/SDI-SoftwareDefinedInverter/TAPAS/blob/master/TAPASquickStartGuide.pdf>
+ InstaSPIN-FOC and InstaSPIN-MOTION user guide : 
<http://www.ti.com/lit/ug/spruhj1g/spruhj1g.pdf>
+ Instaspin projects and labs user's guide, see motorware _`<drive>:\ti\motorware\
motorware_1_01_00_16\docs\labs\instaspin_labs.pdf`_
+ TMS320F28069MPZT overview and datasheet: 
<http://www.ti.com/lit/ug/spruh18g/spruh18g.pdf>

## 6. STANDARD TERMS FOR EVALUATION MODULES

1.Delivery: Siemens delivers Siemens evaluation boards, kits, or modules, including any accompanying demonstration software,
components, and/or documentation which may be provided together or separately (collectively, an “EVM” or “EVMs”) to the User
(“User”) in accordance with the terms set forth herein. User's acceptance of the EVM is expressly subject to the following terms.

1.1 EVMs are intended solely for product or software developers for use in a research and development setting to facilitate feasibility
evaluation, experimentation, or scientific analysis of Siemens semiconductors products. EVMs have no direct function and are not
finished products. EVMs shall not be directly or indirectly assembled as a part or subassembly in any finished product. For
clarification, any software or software tools provided with the EVM (“Software”) shall not be subject to the terms and conditions
set forth herein but rather shall be subject to the applicable terms that accompany such Software

1.2 EVMs are not intended for consumer or household use. EVMs may not be sold, sublicensed, leased, rented, loaned, assigned,
or otherwise distributed for commercial purposes by Users, in whole or in part, or used in any finished product or production
system.

2 Limited Warranty and Related Remedies/Disclaimers:

2.1 These terms do not apply to Software. The warranty, if any, for Software is covered in the applicable Software License
Agreement.Siemens

2.2 Siemens warrants that the Siemens EVM will conform to Siemens' published specifications for ninety (90) days after the date
Siemens delivers such EVM
to User. Notwithstanding the foregoing, Siemens shall not be liable for a nonconforming EVM if (a) the nonconformity was caused by
neglect, misuse or mistreatment by an entity other than Siemens, including improper installation or testing, or for any EVMs that
have been altered or modified in any way by an entity other than Siemens, (b) the nonconformity resulted from User's design,
specifications or instructions for such EVMs or improper system design, or (c) User has not paid on time. Testing and other quality control techniques are used to the extent Siemens deems necessary. Siemens does not test all parameters of each EVM.
User's claims against Siemens under this Section 2 are void if User fails to notify Siemens of any apparent defects in the EVMs
within ten (10) business days after delivery, or of any hidden defects with ten (10) business days after the defect has been detected.

2.3 Siemens's sole liability shall be at its option to repair or replace EVMs that fail to conform to the warranty set forth above, or
credit User's account for such EVM. Siemens's liability under this warranty shall be limited to EVMs that are returned during the
warranty period to the address designated by Siemens and that are determined by Siemens not to conform to such warranty. If
Siemens elects to repair or replace such EVM, Siemens shall have a reasonable time to repair such EVM or provide replacements.
Repaired EVMs shall be warranted for the remainder of the original warranty period. Replaced EVMs shall be warranted for a new
full ninety (90) day warranty period.

3 Regulatory Notices:

3.1 United States

3.1.1 Notice applicable to EVMs not FCC-Approved:

__FCC NOTICE:__ This kit is designed to allow product developers to evaluate electronic components, circuitry, or software
associated with the kit to determine whether to incorporate such items in a finished product and software developers to write
software applications for use with the end product. This kit is not a finished product and when assembled may not be resold or
otherwise marketed unless all required FCC equipment authorizations are first obtained. Operation is subject to the condition
that this product not cause harmful interference to licensed radio stations and that this product accept harmful interference.
Unless the assembled kit is designed to operate under part 15, part 18 or part 95 of this chapter, the operator of the kit must
operate under the authority of an FCC license holder or must secure an experimental authorization under part 5 of this chapter.

3.1.2 For EVMs annotated as FCC – FEDERAL COMMUNICATIONS COMMISSION Part 15 Compliant:

__CAUTION__ 

This device complies with part 15 of the FCC Rules. Operation is subject to the following two conditions: (1) This device may not
cause harmful interference, and (2) this device must accept any interference received, including interference that may cause
undesired operation.
Changes or modifications not expressly approved by the party responsible for compliance could void the user's authority to
operate the equipment.

__FCC Interference Statement for Class A EVM devices__

NOTE: This equipment has been tested and found to comply with the limits for a Class A digital device, pursuant to part 15 of
the FCC Rules. These limits are designed to provide reasonable protection against harmful interference when the equipment is
operated in a commercial environment. This equipment generates, uses, and can radiate radio frequency energy and, if not
installed and used in accordance with the instruction manual, may cause harmful interference to radio communications.
Operation of this equipment in a residential area is likely to cause harmful interference in which case the user will be required to
correct the interference at his own expense.

__FCC Interference Statement for Class B EVM devices__

NOTE: This equipment has been tested and found to comply with the limits for a Class B digital device, pursuant to part 15 of
the FCC Rules. These limits are designed to provide reasonable protection against harmful interference in a residential
installation. This equipment generates, uses and can radiate radio frequency energy and, if not installed and used in accordance
with the instructions, may cause harmful interference to radio communications. However, there is no guarantee that interference
will not occur in a particular installation. If this equipment does cause harmful interference to radio or television reception, which
can be determined by turning the equipment off and on, the user is encouraged to try to correct the interference by one or more
of the following measures:
+ Reorient or relocate the receiving antenna.
+ Increase the separation between the equipment and receiver.
+ Connect the equipment into an outlet on a circuit different from that to which the receiver is connected.
+ Consult the dealer or an experienced radio/TV technician for help.

3.2 Canada

3.2.1 For EVMs issued with an Industry Canada Certificate of Conformance to RSS-210 or RSS-247

__Concerning EVMs Including Radio Transmitters:__

This device complies with Industry Canada license-exempt RSSs. Operation is subject to the following two conditions:
(1) this device may not cause interference, and (2) this device must accept any interference, including interference that may
cause undesired operation of the device.

__Concernant les EVMs avec appareils radio:__

Le présent appareil est conforme aux CNR d'Industrie Canada applicables aux appareils radio exempts de licence. L'exploitation
est autorisée aux deux conditions suivantes: (1) l'appareil ne doit pas produire de brouillage, et (2) l'utilisateur de l'appareil doit
accepter tout brouillage radioélectrique subi, même si le brouillage est susceptible d'en compromettre le fonctionnement.

__Concerning EVMs Including Detachable Antennas:__

Under Industry Canada regulations, this radio transmitter may only operate using an antenna of a type and maximum (or lesser)
gain approved for the transmitter by Industry Canada. To reduce potential radio interference to other users, the antenna type
and its gain should be so chosen that the equivalent isotropically radiated power (e.i.r.p.) is not more than that necessary for
successful communication. This radio transmitter has been approved by Industry Canada to operate with the antenna types
listed in the user guide with the maximum permissible gain and required antenna impedance for each antenna type indicated.
Antenna types not included in this list, having a gain greater than the maximum gain indicated for that type, are strictly prohibited
for use with this device.

__Concernant les EVMs avec antennes détachables__

Conformément à la réglementation d'Industrie Canada, le présent émetteur radio peut fonctionner avec une antenne d'un type et
d'un gain maximal (ou inférieur) approuvé pour l'émetteur par Industrie Canada. Dans le but de réduire les risques de brouillage
radioélectrique à l'intention des autres utilisateurs, il faut choisir le type d'antenne et son gain de sorte que la puissance isotrope
rayonnée équivalente (p.i.r.e.) ne dépasse pas l'intensité nécessaire à l'établissement d'une communication satisfaisante. Le
présent émetteur radio a été approuvé par Industrie Canada pour fonctionner avec les types d'antenne énumérés dans le
manuel d’usage et ayant un gain admissible maximal et l'impédance requise pour chaque type d'antenne. Les types d'antenne
non inclus dans cette liste, ou dont le gain est supérieur au gain maximal indiqué, sont strictement interdits pour l'exploitation de
l'émetteur

3.3 Japan – does not apply

3.4 European Union

3.4.1 For EVMs subject to EU Directive 2014/30/EU (Electromagnetic Compatibility Directive):
This is a class A product intended for use in environments other than domestic environments that are connected to a
low-voltage power-supply network that supplies buildings used for domestic purposes. In a domestic environment this
product may cause radio interference in which case the user may be required to take adequate measures.

4 EVM Use Restrictions and Warnings:

4.1 EVMS ARE NOT FOR USE IN FUNCTIONAL SAFETY AND/OR SAFETY CRITICAL EVALUATIONS, INCLUDING BUT NOT
LIMITED TO EVALUATIONS OF LIFE SUPPORT APPLICATIONS.

4.2 User must read and apply the user guide and other available documentation provided by Siemens regarding the EVM prior to
handling or using the EVM, including without limitation any warning or restriction notices. The notices contain important safety
information related to, for example, temperatures and voltages.

4.3 Safety-Related Warnings and Restrictions:

4.3.1 User shall operate the EVM within Siemens’s recommended specifications and environmental considerations stated in the
user guide, other available documentation provided by Siemens, and any other applicable requirements and employ reasonable and
customary safeguards. Exceeding the specified performance ratings and specifications (including but not limited to input
and output voltage, current, power, and environmental ranges) for the EVM may cause personal injury or death, or
property damage. If there are questions concerning performance ratings and specifications, User should contact a Siemens
field representative prior to connecting interface electronics including input power and intended loads. Any loads applied
outside of the specified output range may also result in unintended and/or inaccurate operation and/or possible
permanent damage to the EVM and/or interface electronics. Please consult the EVM user guide prior to connecting any
load to the EVM output. If there is uncertainty as to the load specification, please contact a Siemens field representative.
During normal operation, even with the inputs and outputs kept within the specified allowable ranges, some circuit
components may have elevated case temperatures. These components include but are not limited to linear regulators,
switching transistors, pass transistors, current sense resistors, and heat sinks, which can be identified using the
information in the associated documentation. When working with the EVM, please be aware that the EVM may become
very warm.

4.3.2 EVMs are intended solely for use by technically qualified, professional electronics experts who are familiar with the
dangers and application risks associated with handling electrical mechanical components, systems, and subsystems.
User assumes all responsibility and liability for proper and safe handling and use of the EVM by User or its employees,
affiliates, contractors or designees. User assumes all responsibility and liability to ensure that any interfaces (electronic
and/or mechanical) between the EVM and any human body are designed with suitable isolation and means to safely
limit accessible leakage currents to minimize the risk of electrical shock hazard. User assumes all responsibility and
liability for any improper or unsafe handling or use of the EVM by User or its employees, affiliates, contractors or
designees.

4.4 User assumes all responsibility and liability to determine whether the EVM is subject to any applicable international, federal,
state, or local laws and regulations related to User’s handling and use of the EVM and, if applicable, User assumes all
responsibility and liability for compliance in all respects with such laws and regulations. User assumes all responsibility and
liability for proper disposal and recycling of the EVM consistent with all applicable international, federal, state, and local
requirements.

5.Accuracy of Information: To the extent Siemens provides information on the availability and function of EVMs, Siemens attempts
to be as accurate as possible. However, Siemens does not warrant the accuracy of EVM descriptions, EVM availability or other 
information on its websites as accurate, complete, reliable, current, or error-free.

6.Disclaimers:

6.1 EXCEPT AS SET FORTH ABOVE, EVMS AND ANY MATERIALS PROVIDED WITH THE EVM (INCLUDING, BUT NOT
LIMITED TO, REFERENCE DESIGNS AND THE DESIGN OF THE EVM ITSELF) ARE PROVIDED "AS IS" AND "WITH ALL
FAULTS." Siemens DISCLAIMS ALL OTHER WARRANTIES, EXPRESS OR IMPLIED, REGARDING SUCH ITEMS, INCLUDING
BUT NOT LIMITED TO ANY EPIDEMIC FAILURE WARRANTY OR IMPLIED WARRANTIES OF MERCHANTABILITY OR
FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT OF ANY THIRD PARTY PATENTS, COPYRIGHTS,
TRADE SECRETS OR OTHER INTELLECTUAL PROPERTY RIGHTS.

6.2 EXCEPT FOR THE LIMITED RIGHT TO USE THE EVM SET FORTH HEREIN, NOTHING IN THESE TERMS SHALL BE
CONSTRUED AS GRANTING OR CONFERRING ANY RIGHTS BY LICENSE, PATENT, OR ANY OTHER INDUSTRIAL OR
INTELLECTUAL PROPERTY RIGHT OF Siemens, ITS SUPPLIERS/LICENSORS OR ANY OTHER THIRD PARTY, TO USE THE
EVM IN ANY FINISHED END-USER OR READY-TO-USE FINAL PRODUCT, OR FOR ANY INVENTION, DISCOVERY OR
IMPROVEMENT, REGARDLESS OF WHEN MADE, CONCEIVED OR ACQUIRED.

7.USER'S INDEMNITY OBLIGATIONS AND REPRESENTATIONS. USER WILL DEFEND, INDEMNIFY AND HOLD Siemens, ITS
LICENSORS AND THEIR REPRESENTATIVES HARMLESS FROM AND AGAINST ANY AND ALL CLAIMS, DAMAGES,
LOSSES, EXPENSES, COSTS AND LIABILITIES (COLLECTIVELY, "CLAIMS") ARISING OUT OF OR IN CONNECTION WITH
ANY HANDLING OR USE OF THE EVM THAT IS NOT IN ACCORDANCE WITH THESE TERMS. THIS OBLIGATION SHALL
APPLY WHETHER CLAIMS ARISE UNDER STATUTE, REGULATION, OR THE LAW OF TORT, CONTRACT OR ANY OTHER
LEGAL THEORY, AND EVEN IF THE EVM FAILS TO PERFORM AS DESCRIBED OR EXPECTED.

8.Limitations on Damages and Liability:

8.1 General Limitations. IN NO EVENT SHALL Siemens BE LIABLE FOR ANY SPECIAL, COLLATERAL, INDIRECT, PUNITIVE,
INCIDENTAL, CONSEQUENTIAL, OR EXEMPLARY DAMAGES IN CONNECTION WITH OR ARISING OUT OF THESE
TERMS OR THE USE OF THE EVMS, REGARDLESS OF WHETHER Siemens HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES. EXCLUDED DAMAGES INCLUDE, BUT ARE NOT LIMITED TO, COST OF REMOVAL OR
REINSTALLATION, ANCILLARY COSTS TO THE PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES, RETESTING,
OUTSIDE COMPUTER TIME, LABOR COSTS, LOSS OF GOODWILL, LOSS OF PROFITS, LOSS OF SAVINGS, LOSS OF
USE, LOSS OF DATA, OR BUSINESS INTERRUPTION. NO CLAIM, SUIT OR ACTION SHALL BE BROUGHT AGAINST Siemens
MORE THAN TWELVE (12) MONTHS AFTER THE EVENT THAT GAVE RISE TO THE CAUSE OF ACTION HAS
OCCURRED.

8.2 Specific Limitations. IN NO EVENT SHALL Siemens' AGGREGATE LIABILITY FROM ANY USE OF AN EVM PROVIDED
HEREUNDER, INCLUDING FROM ANY WARRANTY, INDEMITY OR OTHER OBLIGATION ARISING OUT OF OR IN
CONNECTION WITH THESE TERMS, , EXCEED THE TOTAL AMOUNT PAID TO Siemens BY USER FOR THE PARTICULAR
EVM(S) AT ISSUE DURING THE PRIOR TWELVE (12) MONTHS WITH RESPECT TO WHICH LOSSES OR DAMAGES ARE
CLAIMED. THE EXISTENCE OF MORE THAN ONE CLAIM SHALL NOT ENLARGE OR EXTEND THIS LIMIT.

9.Return Policy. Except as otherwise provided, Siemens does not offer any refunds, returns, or exchanges. Furthermore, no return
of EVM(s) will be accepted if the package has been opened and no return of the EVM(s) will be accepted if they are damaged or
otherwise not in a resalable condition. If User feels it has been incorrectly charged for the EVM(s) it ordered or that delivery violates
the applicable order, User should contact Siemens. All refunds will be made in full within thirty (30) working days from the return of
the components(s), excluding any postage or packaging costs.

10.Governing Law: These terms and conditions shall be governed by and interpreted in accordance with the laws of the State of
Texas, without reference to conflict-of-laws principles. User agrees that non-exclusive jurisdiction for any dispute arising out of or
relating to these terms and conditions lies within courts located in the State of Texas and consents to venue in Dallas County,
Texas.
Notwithstanding the foregoing, any judgment may be enforced in any United States or foreign court, and Siemens may seek
injunctive relief in any United States or foreign court.

Mailing Address: Siemens Aktiengesellschaft, Werner-von-Siemens-Straße 1, 80333 Munich 
