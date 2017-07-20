# TAPAS
Community drives inverter project

Foreword and acknowledgements
-----------------------------

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