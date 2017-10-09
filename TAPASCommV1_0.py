###################################################################################################
## SDI TAPAS python demo application - communication module
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

# module for platform check
import platform
                     
# module for data handling
import struct

# global variable necessary for crc-calculation
crc_table = [0] * 256

# used for crc
POLY = 0x1021
START = 0xFFFF
###
if (platform.machine() == "i586"):
    # this is necessary to run the script on IOT2000
    # (manual control of the CS-pin)
    #set filename for set_chipselect
    CS = "/sys/class/gpio/gpio10/value"
else: 
    # just do nothing
    print("")

#function for setting chipselect, necessary only on IOT2000
def set_chipselect (status):
    file = open(CS, 'w')

    if(status == 0):
        file.write("0")
    elif(status == 1):
        file.write("1")
    else:
        file.write("0")

    file.close()
###

def GenerateCrcTable():
	for i in range(0, 256, 1):
		crc = i << 8
		for j in range(0, 8, 1):
			if crc & 0x8000:
				crc <<= 1
				crc = crc ^ POLY 
			else:
				crc <<= 1
		crc_table[i] = crc & 0xFFFF # just regard the lower 16Bit of the value

def CalcCrc(data, len_words):
	crc = START
	for i in range(0, len_words, 1):
		octet = data[i] & 0xFF

		idx = ((crc >> 8) & 0xFF) ^ octet
		crc = (crc << 8) ^ crc_table[idx]
		
		octet = (data[i] >> 8) & 0xFF
		idx = ((crc >> 8) & 0xFF) ^ octet
		crc = (crc << 8) ^ crc_table[idx]
	crc = crc & 0xFFFF # just regard the lower 16Bit of the value
	return crc

def transferMasterSlave(spi,flags, numPolePairs, ratedCurrent,
                        RoverLestFrequency, fluxEstFrequency,
                        setpointSpeed, setpointAccel):
 
    # packing data together
    sender_temp = struct.pack('HHffffffffffffffffHHHH', flags, numPolePairs, ratedCurrent, RoverLestFrequency, fluxEstFrequency, setpointSpeed, setpointAccel,
                0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0, 0, 0, 0, 0)
    sender = []
    sender16 = []

    # first create a list containing all the single Bytes 
    for byte in sender_temp:
        sender.append(byte)

    # then create a second list which holds 16Bit values and the bytes swapped
    for i in range(0, len(sender), 2):
        temp = (sender[i+1]<<8) | (sender[i] )
        sender16.append(temp)

    # calculate the checksum for the "package" to be sent   
    send_CRC = CalcCrc(sender16, ((len(sender)//2)-1))
    packed_CRC = struct.pack('H', send_CRC)

    # now, add the Checksum to the package to be sent 
    sender[len(sender)-2] = packed_CRC[0]
    sender[len(sender)-1] = packed_CRC[1]

    resp = []
    receiver = []

    for i in range(0, len(sender), 2):
        ### 
        # IOT2000 : necessary to set and reset the CS-Pin by hand
        if (platform.machine() == "i586"):
            set_chipselect(0)
        else :
            # else it's done implicitly
            print("")
        ###

        res2 = spi.xfer( [sender[i+1], sender[i]], 20000)
        
        ###
        # IOT2000 : manually drive CS back
        if (platform.machine() == "i586"):
            set_chipselect(1) 
        else : 
            # else it's done implicitly
            print("")
        ###

        resp.append(res2[1])
        resp.append(res2[0])

    resp_bytes = struct.pack('B'*len(resp), *resp)
    resp_calcCrc = struct.unpack('H'*((len(resp_bytes)//2)), resp_bytes)
    resp_readable = struct.unpack('HHffffHHfffffffffffHHHH', resp_bytes)

    for byte in resp_calcCrc:
        receiver.append(byte)

    recv_CRC = CalcCrc(receiver, (len(receiver)-1))

    if(recv_CRC == int(resp_readable[22])):
        SPIstatus = 1
    else:
        SPIstatus = 0

    resp_readable = resp_readable + (SPIstatus,)
    slave_rx_dict={};
    slave_rx_dict["flags"] = resp_readable[0]
    slave_rx_dict["Protection mode"] = resp_readable[1]
    slave_rx_dict["dc-bus voltage"] = resp_readable[2]
    slave_rx_dict["dc-bus current"] = resp_readable[3]
    slave_rx_dict["board-temperature"] = resp_readable[4]
    slave_rx_dict["motor speed"] = resp_readable[5]
    slave_rx_dict["controller state [CTRL_state]"] = resp_readable[6]
    slave_rx_dict["estimator state [EST_state]"] = resp_readable[7]
    slave_rx_dict["motorRs"] = resp_readable[8]
    slave_rx_dict["motorRr"] = resp_readable[9]
    slave_rx_dict["motorLsd"] = resp_readable[10]
    slave_rx_dict["motorLsq"] = resp_readable[11]
    slave_rx_dict["ratedFlux"] = resp_readable[12]
    slave_rx_dict["analog in 0 voltage"] = resp_readable[13]
    slave_rx_dict["analog in 1 voltage"] = resp_readable[14]
    slave_rx_dict["analog in 2 voltage"] = resp_readable[15]
    slave_rx_dict["analog in 3 voltage"] = resp_readable[16]
    slave_rx_dict["analog in 4 voltage"] = resp_readable[17]
    slave_rx_dict["analog in 5 voltage"] = resp_readable[18]
    slave_rx_dict["status digital inputs"] = resp_readable[19]
    slave_rx_dict["spi status slave"] = resp_readable[20]
    slave_rx_dict["reserved2"] = resp_readable[21]
    slave_rx_dict["CRC"] = resp_readable[22]
    slave_rx_dict["spi connection status"] = SPIstatus
    return slave_rx_dict
