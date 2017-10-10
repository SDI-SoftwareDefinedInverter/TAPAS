#!/usr/bin/python3
###################################################################################################
## SDI TAPAS python demo application - main module
##
## Revisions:
## 1.0 - Initial version
## 
## Copyright (c) 2017 Siemens AG
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions 
# are met:
#
# 1. Redistributions of source code must retain the above copyright 
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in the 
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of 
#    its contributors may be used to endorse or promote products derived 
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###################################################################################################

# import for platform check
import platform

# modules for spi communication
import spidev
import TAPASComm

# other modules for data handling
import struct
import json

# modules for implementing user interface
import curses
import time

# global constants
RATED_CURRENT_RUN = 2.5
SERVO_MOTOR = "1"
MODEL_MOTOR = "2"

###
# this function is necessary for running the script on IOT2000 platform
# exporting gpio file
def export_gpio ():
    export = "/sys/class/gpio/export"
    file = open(export, 'w')
    file.write("10")
if (platform.machine() == "i586"):
    export_gpio()
### 

# defining the names for the states of Controller-state-machine, estimator and custom user errors
_CTRL_states_ = ["CTRL_State_Error","CTRL_State_Idle","CTRL_State_OffLine","CTRL_State_OnLine","CTRL_numStates","CTRL_State_unknown"]
   
_EST_states_ = ["EST_State_Error","EST_State_Idle","EST_State_RoverL","EST_State_Rs","EST_State_RampUp","EST_State_IdRated",
                "EST_State_RatedFlux_OL","EST_State_RatedFlux","EST_StateRampDown","EST_StateLockRotor","EST_State_Ls","EST_State_Rr",
                "EST_State_MotorIdentified","EST_State_OnLine","EST_numStates","EST_State_unknown"]  

_PROTECT_states_ = ["Normal_OP", "PROTECT_OVERTEMP", "PROTECT_OVERCURRENT", "PROTECT_UNKNOWN"]

# start application
# set title of terminal window
title = "SDI TAPAS BOARD QUICK START" 
print("\x1b]2;%s\x07" % title)

# initialize SPI-HW
spi = spidev.SpiDev()

if (platform.machine() == "i586"):
    # open spi connection on IOT2040
    spi.open(1,0)
else :
    # e.g. for raspberry pi zero (w) 
    spi.open(0,1)

spi.bits_per_word = 8 
spi.mode = 3

#initialize "curses"-module for console management
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

###
# this one is not executable on the iot2040
if not (platform.machine() == "i586"):
    # e.g. raspberry pi lib supports this 
    curses.curs_set(False)
###

stdscr.keypad(1)
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_WHITE)

stdscr.bkgd(curses.color_pair(1))
stdscr.refresh()
 
win = curses.newwin(40, 85, 1, 2)
win.bkgd(curses.color_pair(2))
win.box()

# init variables
callNo = 0
RoverLestFrequencyHz = 0.0
fluxEstFrequency = 0.0
motorParametersSet = 0
motorIsIdentified = 0
# init table for CRC
TAPASComm.GenerateCrcTable()	

# synchronize the communication with the slave
syncStatus = 0
SPIstatusTest = 0
countTransactionsSuccess = 0
win.addstr(1,2, "Connecting to slave...")
win.refresh()
try : 
    while syncStatus != 1:
        ret = TAPASComm.transferMasterSlave(spi,0,
                                    1,0.0,
                                    10.0,10.0,
                                    0.0,0.0)
   
        if(ret["spi connection status"] == 1):
            countTransactionsSuccess += 1
            if((ret["spi status slave"] == 0xABCD) and (countTransactionsSuccess > 15)):
                syncStatus = 1
            else:    
                syncStatus = 0
        else:   
            syncStatus = 0

except KeyboardInterrupt :

    win.addstr(10,5, "User abort of connection procedure...", curses.A_BOLD)
    win.refresh()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

    spi.close()
    time.sleep(1.5)

    quit()

# when sync is done 
# -> start the interactive part
try:	
    while True:
        # clear screen and print buffer
        win.erase()
        win.box()
        win.addstr(1, 2, "SDI TAPAS BOARD QUICK START - MAIN MENU", curses.A_BOLD)
        win.addstr(2, 2, "##########################################################################")
        win.addstr(3, 2, "please choose one of the following options:")
        win.addstr(4, 2, "1 : set basic motor parameters")
        win.addstr(5, 2, "2 : identify motor")
        win.addstr(6, 2, "3 : run motor")
        win.addstr(7, 2, "4 : disable inverter")
        win.addstr(8, 2, "5 : disable inverter and quit")
        win.addstr(9, 2, "##########################################################################")
    
        # print to the terminal-screen
        win.refresh()

        # evaluate user input for mode selection
        selectedMode = chr(stdscr.getch(11,4))

        if selectedMode == "1" :
            curses.echo()

        # get rough motor parameters
            win.erase()
            win.refresh()
            win.box()
            win.addstr(1, 2, "SDI TAPAS BOARD QUICK START - SET BASIC MOTOR PARAMETERS",curses.A_BOLD) 
            win.addstr(2, 2, "###################################################")
            #win.addstr(3, 2,"Please enter a few motor parameters neccessary to start the identification", curses.A_BOLD)
        
        # get the number of pole pairs for the connected motor
            win.addstr(5,2,"a)Number of motor pole pairs", curses.A_DIM)
            win.addstr(6,4,"2", curses.color_pair(4))
            win.refresh()
            
            polePairsInputSucc = 0
            while(polePairsInputSucc == 0): 
                try :
                    # read in number of pole pairs and convert to int format
                    polePairs = stdscr.getstr(7,6)    
                    polePairs = int(polePairs)
                    polePairsInputSucc = 1
                except ValueError:
                    win.addstr(6,2,  "                                                   ")
                    win.addstr(7,5 , "! ERROR: Invalid input, please retry !", curses.color_pair(3))
                    win.refresh()
                    time.sleep(1.5)
                    polePairsInputSucc = 0

            win.addstr(7,2,"--> Motor has " + str(polePairs) + " pole pairs       ")
            win.refresh()
                
        # get rated current for the connected motor
            win.addstr(9,2,"b) Enter maximum rated motor current [A] ", curses.A_DIM)
            win.addstr(10,4, "4", curses.color_pair(4))
            win.refresh()
            
            currentInputSucc = 0 
            while(currentInputSucc == 0):
                try :   
                    ratedCurrent = stdscr.getstr(11, 6)
                    ratedCurrent = float(ratedCurrent)
                    currentInputSucc = 1
                except ValueError: 
                    win.addstr(10,2,  "                                                    ")
                    win.addstr(11,5 , "! ERROR: Your input was invalid, please retry !", curses.color_pair(3))
                    win.refresh()
                    time.sleep(1.5)
                    currentInputSucc = 0

            win.addstr(11,2,"--> Rated motor current "  + str(ratedCurrent) + " [A]")
            win.refresh()


            win.addstr(13,2,"c) Motor type:", curses.A_DIM)
            win.addstr(14,4, " 1 - servo motor (does it look gray and serious)", curses.A_DIM)
            win.addstr(15,4, " 2 - hobbyist motor (for models and rc toys)", curses.A_DIM)
            win.addstr(16,4, "1", curses.color_pair(4))
            win.refresh()
        
        # get motor type
            motorTypeInputSucc = 0
            while(motorTypeInputSucc == 0): 
                try : 
                    motorType = chr(stdscr.getch(17, 6))

                    if motorType == SERVO_MOTOR:
                        win.addstr(17, 2, "--> Selected a servo motor                                              ")
                        win.refresh()
                        RoverLestFrequencyHz = 150.0
                        fluxEstFrequency = 50.0
                        motorParametersSet = 1
                        motorTypeInputSucc = 1
                    elif motorType == MODEL_MOTOR:
                        win.addstr(17, 2, "--> Selected a hobbyist motor                                              ")
                        win.refresh()
                        RoverLestFrequencyHz = 300.0
                        fluxEstFrequency = 30.0
                        motorParametersSet = 1
                        motorTypeInputSucc = 1
                    else:
                        win.addstr(16,2,  "                                                                 ")
                        win.addstr(17, 6, "! --> invalid selection, choose either 1 or 2 !", curses.A_BOLD)
                        win.refresh()
                        motorParametersSet = 0
                        motorTypeInputSucc = 0
                except ValueError: 
                        win.addstr(16,2, "                                                    ")
                        win.addstr(17,5 , "! ERROR: Invalid input, please retry !", curses.color_pair(3))
                        win.refresh()
                        time.sleep(1.5)
                        motorTypeInputSucc = 0

                curses.noecho()
                time.sleep(1.5)

        elif selectedMode == "2" : 
            # start id
            if(not motorParametersSet == 1) :
                win.erase()
                win.refresh()
                win.box()
                win.addstr(10, 10, "ERROR: ", curses.color_pair(3))
                win.addstr(11,5,"! you have to set the motor parameters first !", curses.color_pair(3))
                win.refresh()
                time.sleep(1.5)
            else :
                Senden_flags = 1
                
                for i in range(0,4):
                        ret = TAPASComm.transferMasterSlave(spi,int(Senden_flags),
                        int(polePairs),float(ratedCurrent),
                        float(RoverLestFrequencyHz),float(fluxEstFrequency),
                        1.0,1.0)
                
                Senden_flags = 3 # set run and identify bits

                runConfiguration = 0
            
                try : 
                    while ((ret["flags"] & (1 << 5)) == 0):
                        ret = TAPASComm.transferMasterSlave(spi,int(Senden_flags),
                                                    int(polePairs),float(ratedCurrent),
                                                    float(RoverLestFrequencyHz),float(fluxEstFrequency),
                                                    1.0,1.0)

                        # monitor the CTRL_state index
                        if(ret["controller state [CTRL_state]"] > 4):
                            ret["controller state [CTRL_state]"] = 5

                        # monitor the EST_state index
                        if(ret["estimator state [EST_state]"] > 14):	
                            ret["estimator state [EST_state]"] = 15
                
                        # check the TAPAS-slave for a protection error
                        if(ret["Protection mode"] != 0):
                            Senden_flags = 0
                            motorIsIdentified = 0
                            if(ret["Protection mode"] > 2) :
                                ret["Protection mode"] = 3
                            win.erase()
                            win.refresh()
                            win.box()
                            win.addstr(10,10, "ERROR!", curses.color_pair(3))
                            win.addstr(11, 5, "SDI TAPAS-Board reported an " + str(_PROTECT_states_[int(ret["Protection mode"])]) + "!", curses.color_pair(3))
                            win.addstr(12, 5, "Restart identification to continue")
                            win.refresh()

                            for i in range(0,3):
                                ret = TAPASComm.transferMasterSlave(spi,int(Senden_flags),
                                int(polePairs),float(ratedCurrent),
                                float(RoverLestFrequencyHz),float(fluxEstFrequency),
                                0.0 , 0.0)
                            time.sleep(1.5) 
                            break
                                                     
                        win.erase()
                        win.box()
                        win.addstr(1, 2, " SDI TAPAS BOARD QUICK START - MOTOR IDENTIFICATION ", curses.A_BOLD)
                        win.addstr(2, 2, "###################################################")
                        win.addstr(3, 2, "--------------current SDI TAPAS-board data-------------")
                        win.addstr(4, 2, "* Protection mode..............: " + _PROTECT_states_[ret["Protection mode"]])
                        win.addstr(5, 2, "* dc-bus voltage...............: " + str(round((ret["dc-bus voltage"]*1000.0),2)))
                        win.addstr(5, 43, "   [V] ")
                        win.addstr(6, 2, "* dc-bus current...............: " + str(round((ret["dc-bus current"]),2)))
                        win.addstr(6, 43, "   [A] ")
                        win.addstr(7, 2, "* dc-bus power.................: " + str(round(((ret["dc-bus voltage"]*1000.0)*ret["dc-bus current"]),2)))
                        win.addstr(7, 43, "   [W] ")
                        win.addstr(8, 2, "* board-temperature............: " + str(round((ret["board-temperature"]),2)))
                        win.addstr(8, 43, "   [C] ")
                        win.addstr(9, 2, "* motor speed..................: " + str(round((ret["motor speed"]*1000.0),2)))
                        win.addstr(9, 43, "  [rpm] ")
                        win.addstr(10,2, "* controller state [CTRL_state]: " + _CTRL_states_[int(ret["controller state [CTRL_state]"])])
                        win.addstr(11,2, "* estimator state [EST_state]..: " + _EST_states_[int(ret["estimator state [EST_state]"])])
                        win.addstr(12,2, "------------identified motor parameters------------")                 
                        win.addstr(13,2, "* motorRs......................: " + str(round(ret["motorRs"],7)))
                        win.addstr(13,43, "  [Ohm] ")
                        win.addstr(14,2, "* motorRr......................: " + str(round(ret["motorRr"],7)))
                        win.addstr(14,43, "  [Ohm] ")
                        win.addstr(15,2, "* motorLsd.....................: " + str(round(ret["motorLsd"],7)))
                        win.addstr(15,43, " [Henry] ")
                        win.addstr(16,2, "* motorLsq.....................: " + str(round(ret["motorLsq"],7)))
                        win.addstr(16,43, " [Henry] ")
                        win.addstr(17,2, "* ratedFlux....................: " + str(round(ret["ratedFlux"],7)))
                        win.addstr(17,43, "  [V/Hz] ")
                        win.addstr(18,2, "---------------------------------------------------")
                        if(ret["spi connection status"] == 1) :
                            win.addstr(19,6, "  checksum correct - data valid  ")
                        else :
                            win.addstr(19,6, "!!checksum incorrect - data invalid!!", curses.color_pair(3))
                        win.addstr(20,2, "###################################################")   
                        win.addstr(22,2, "Identifying connected motor - please wait ...", curses.A_BOLD)
                        win.addstr(24,4, "ABORT WITH CTRL-C", curses.color_pair(3))
                        win.refresh()
                        time.sleep(0.2)

                    ratedCurrent = RATED_CURRENT_RUN    
                    Senden_flags = 1 # system remains enabled
                    for i in range(0,3):
                        ret = TAPASComm.transferMasterSlave(spi,int(Senden_flags),
                        int(polePairs),float(ratedCurrent),
                        float(RoverLestFrequencyHz),float(fluxEstFrequency),
                        0.0 , 0.0)

                    win.addstr(22, 2, "                                                 ")
                    win.addstr(22, 2, "Motor identification successful", curses.color_pair(1))
                    win.addstr(23, 4, "Please press <s> to save the identified motor                     ")
                    win.addstr(24, 4, "parameters to file or any other key to quit without saving                ")
                    win.refresh()
                
                    # save or not save ? 
                    sel = chr(stdscr.getch(28,4))
                    motorIsIdentified = 1
                    if(sel == 's'):
                        json.dump(ret, open("yourMotorParams.json","w") )
                except KeyboardInterrupt:
                    Senden_flags = 0
                    motorParametersSet = 0
                    motorIsIdentified = 0
                    ratedCurrent = 0.0
                    for i in range(0,3):
                        ret = TAPASComm.transferMasterSlave(spi,int(Senden_flags),
                        int(polePairs),float(ratedCurrent),
                        float(RoverLestFrequencyHz),float(fluxEstFrequency),
                        0.0 , 0.0)
                    win.erase()
                    win.box()
                    win.refresh()
                    win.addstr(10,10, "HINT:", curses.A_BOLD)
                    win.addstr(11, 5, "User canceled motor identification, disabling inverter", curses.color_pair(3))
                    win.addstr(12, 5, "Enter motor parameters again - see (1)", curses.color_pair(3))
                    win.refresh()
                    time.sleep(1.5)                
        elif selectedMode == "3" :
            if(motorIsIdentified != 1):
                win.erase()
                win.refresh()
                win.box()
                win.addstr(10,10, "ERROR: ", curses.color_pair(3))
                win.addstr(11,5, "Identify motor first - see (2)! ", curses.color_pair(3))
                win.refresh()
                time.sleep(1.5)
            else:

                Senden_flags = 3
                curses.echo()
        # get setpoint for the maximum acceleration
                win.erase()
                win.box()
                win.addstr(1,2,"SDI TAPAS BOARD QUICK START - RUN MOTOR", curses.A_BOLD)
                win.addstr(2, 2, "###################################################")
                win.addstr(3,2,"a) Set maximum acceleration in [rpm/s]")
                win.addstr(4,4,"100.0", curses.color_pair(4)) 
                win.refresh()
        
                getMaxAccSucc = 0
                while(getMaxAccSucc == 0): 
                    try:
                        win.addstr(16,5,"                                                    ")
                        win.refresh()
                        setMaxAcc = stdscr.getstr(5, 6)
                        setMaxAcc = float(setMaxAcc)
                        if(setMaxAcc > 1500.0):
                                setMaxAcc = 1500
                                win.addstr(5,6, "HINT: Acceleration limited to 1500 rpm/s for security reasons", curses.A_BOLD)
                                win.refresh()
                        setMaxAcc /= 1000.0
                        getMaxAccSucc = 1
                    except ValueError:
                        win.addstr(4, 1, "                                                    ")
                        win.addstr(16,5 , "ERROR: invalid input, please retry", curses.color_pair(3))
                        win.refresh()
                        time.sleep(1.5)
                        getMaxAccSucc = 0
                
         # get setpoint for the motor speed
                win.addstr(7,2,"b) Set speed [rpm] ")
                win.addstr(8,4,"200", curses.color_pair(4))
                win.refresh()
                
                getSpeedSucc = 0
                while(getSpeedSucc == 0): 
                    try: 
                        win.addstr(16,5,"                                                    ")
                        win.refresh()
                        setSpeed = stdscr.getstr(9, 6)
                        setSpeed = float(setSpeed)
                        setSpeed /= 1000.0
                        getSpeedSucc = 1
                    except ValueError:
                        win.addstr(8, 1, "                                                    ") 
                        win.addstr(16, 5, "ERROR: Invalid input, please retry", curses.color_pair(3))
                        win.refresh()
                        time.sleep(1.5) 
                        getSpeedSucc = 0


                win.addstr(10 ,6," -> Your acceleration : " + str(setMaxAcc*1000.0) + " [rpm/s]")
                win.addstr(11 ,6," -> Your motor speed  : " + str(setSpeed*1000.0) + " [rpm]")
                win.addstr(12 ,6," -> To stop observing values, hit Ctrl-C")
                win.refresh()
                time.sleep(1.0)
                curses.noecho()

                readData = 1
                ratedCurrent = RATED_CURRENT_RUN
                try : 
                    while readData:

                        ret = TAPASComm.transferMasterSlave(spi,int(Senden_flags),
                        int(polePairs),float(ratedCurrent),
                        float(RoverLestFrequencyHz),float(fluxEstFrequency),
                        float(setSpeed),float(setMaxAcc))
                     
                        # monitor the CTRL_state index
                        if(ret["controller state [CTRL_state]"] > 4):
                            ret["controller state [CTRL_state]"] = 5
                      
                        # monitor the EST_state index
                        if(ret["estimator state [EST_state]"] > 14):
                            ret["estimator state [EST_state]"] = 15
                      
                        # check the TAPAS-slave for a protection error
                        if(ret["Protection mode"] != 0):
                            if(ret["Protection mode"] > 2) :
                                ret["Protection mode"] = 3
                            Senden_flags = 0
                            motorIsIdentified = 0
                            win.erase()
                            win.refresh()
                            win.box()
                            win.addstr(10, 10, "ERROR!", curses.color_pair(3))
                            win.addstr(11, 5, "Your SDI TAPAS-Board reported an " + str(_PROTECT_states_[int(ret["Protection mode"])]) + "!", curses.color_pair(3))
                            win.refresh()

                            for i in range(0,3):
                                ret = TAPASComm.transferMasterSlave(spi,int(Senden_flags),
                                int(polePairs),float(ratedCurrent),
                                float(RoverLestFrequencyHz),float(fluxEstFrequency),
                                0.0 , 0.0)
                      
                            readData = 0 
                            time.sleep(1.5)
                            break
                            
                        win.erase()
                        win.box()
                        win.addstr(1, 2, "SDI TAPAS BOARD QICK START - OBSERVER VIEW", curses.A_BOLD)
                        win.addstr(2, 2, "###################################################")
                        win.addstr(3, 2, "--------------current SDI TAPAS-board data-------------")
                        win.addstr(4, 2, "* Protection mode..............: " + _PROTECT_states_[ret["Protection mode"]])
                        win.addstr(5, 2, "* dc-bus voltage...............: " + str(round((ret["dc-bus voltage"]*1000.0),2)))
                        win.addstr(5, 43, "   [V] ")
                        win.addstr(6, 2, "* dc-bus current...............: " + str(round((ret["dc-bus current"]),2)))
                        win.addstr(6, 43, "   [A] ")
                        win.addstr(7, 2, "* dc-bus power.................: " + str(round(((ret["dc-bus voltage"]*1000.0)*ret["dc-bus current"]),2)))
                        win.addstr(7, 43, "   [W] ")
                        win.addstr(8, 2, "* board-temperature............: " + str(round((ret["board-temperature"]),2)))
                        win.addstr(8, 43, "   [C] ")
                        win.addstr(9, 2, "* motor speed..................: " + str(round((ret["motor speed"]*1000.0),2)))
                        win.addstr(9, 43, "  [rpm] ")
                        win.addstr(10,2, "* controller state [CTRL_state]: " + _CTRL_states_[int(ret["controller state [CTRL_state]"])])
                        win.addstr(11,2, "* estimator state [EST_state]..: " + _EST_states_[int(ret["estimator state [EST_state]"])])
                        win.addstr(12,2, "---------------------------------------------------")
                        if(ret["spi connection status"] == 1) :
                            win.addstr(13,6, "  checksum correct - data valid  ")
                        else :
                            win.addstr(13,6, "!!checksum incorrect - data invalid!!", curses.color_pair(3))
                        win.addstr(14,2, "###################################################")
                        win.addstr(16,2, "Running motor in closed loop mode now ...", curses.A_BOLD)
                        win.addstr(18,4, "press CTRL-C to quit this view", curses.color_pair(1))
                        win.refresh()
                        time.sleep(0.2)
                except KeyboardInterrupt: 
                        readData = 0                   
        
        elif selectedMode == "4" : 
            win.erase()
            win.box()
            win.refresh()
            win.addstr(5,5, "Inverter now gets shut down", curses.A_BOLD)
            win.refresh()
            motorParametersSet = 0
            motorIsIdentified = 0 
            for i in range(0,3):
                ret = TAPASComm.transferMasterSlave(spi,0,
                                            1,0.0,
                                            float(RoverLestFrequencyHz),float(fluxEstFrequency),
                                            0.0,0.0)
            time.sleep(1.5)
        elif selectedMode == "5" :
            win.erase()
            win.box()
            win.refresh()
            win.addstr(5,5, "Disabling inverter ...", curses.A_BOLD)
            win.addstr(6,5, "Shutting down ...", curses.A_BOLD)
            win.refresh()
            motorParametersSet = 0
            motorIsIdentified = 0     
            for i in range(0,3):
                ret = TAPASComm.transferMasterSlave(spi,0,
                1,0.0,
                float(RoverLestFrequencyHz),float(fluxEstFrequency),
                0.0,0.0)
            curses.nocbreak()
            stdscr.keypad(0)
            curses.echo()
            curses.endwin()
             
            spi.close()

            quit()
            time.sleep(1.5)
        else :
            win.erase()
            win.refresh()
            win.box()
            win.addstr(11, 5,"Invalid selection", curses.color_pair(3))
            win.refresh()
            time.sleep(1.5)
	
except KeyboardInterrupt:# Ctrl+C pressed, so...
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

    spi.close()
#end try
