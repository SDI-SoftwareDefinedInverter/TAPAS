"""
TapasFlashTool -- This script can be used to flash a TapasBoard using the UART interface.

Author: Stefan Steinmueller

BSD 3-Clause License

Copyright (c) 2017, SDI-SoftwareDefinedInverter
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import time
import argparse
import sys
import logging
import os
import time
import pdb
# not standard
import progressbar
import serial as serial
start_time = time.time()
parser = argparse.ArgumentParser()
parser.add_argument("-b", default=9600, help="Set the communication baudrate for the SCI Bootloader!")
parser.add_argument("-p", required=True, help="set the serial device address (/dev/ttySx)")
parser.add_argument("-k", required=True, help="path to the flash kernel file")
parser.add_argument("-a", required=True, help="path to the application file")
parser.add_argument("-d", required=True, help="The name of the device to load to", choices=["f2802x", "f2803x", "f2805x", "f2806x", "f2837xD", "f2837xS", "f2807x"])
parser.add_argument("-b2", help="second baudrate for flashing the program. The Flash API Can handl ehigher baudrates than the SCI Bootloader! -- Defaults to -b which defaults to 9600 --")
parser.add_argument("-debug", action="store_true", help="enable debug logging")

args = parser.parse_args()

MAX_AUTOBAUD = 10

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
logging.debug("args: {}".format(args))

if not os.path.isfile(args.a):
    logging.error("The given application file path does not point to a file!")
    exit(1)
elif not os.path.isfile(args.k):
    logging.error("The given kernel file path does not point to a file!")
    exit(1)

with serial.Serial(port=args.p) as ser:
    ser.baudrate = int(args.b)
    ser.port = args.p
    ser.timeout = 1  # read timeout 5 seconds...
#    ser.write_timeout = 0.1  # write timeout 5 seconds...
    if ser.is_open:
        logging.debug("Serial Port opened succesfull")
    else:
        logging.error("Could not open serial device Port: {}".format(args.p))
        exit(1)

    gu32_SectorMask = 0xFF
    # Do Autobaud
    logging.debug("Starting Autobaud!")
    ser.write("A".encode())
    okay = False
    count = 0
    while not okay and count < MAX_AUTOBAUD:
        recData = ser.read()      
        if recData == "A".encode():
            okay = True
            count = 0
        else:
            wr = ser.write("A".encode())
            count +=1
    if count is MAX_AUTOBAUD:
        logging.error("Max Autobaud Tries exceeded!")
        exit(1)
    logging.debug("Kernel Autobaud Successfull")
    logging.info("Downloading Kernel file to Controller...")
    with open(args.k, "rt") as kf:
        data = kf.read().replace("\n","").split(" ")
        bar = progressbar.ProgressBar(maxval=len(data), widgets=[progressbar.Bar("=", "[", "]"), " ", progressbar.Percentage()])
        bar.start()
        for i, b in enumerate(data):
            ser.write(bytes([int(b, 16)]))
            recData = ser.read(1)
            if not recData == bytes([int(b, 16)]):
                logging.error("recieved byte did not match sent!\n{} != {}\tPOS:{}\naborting...".format(recData, bytes([int(b, 16)]), i))
                exit(1)
            bar.update(i+1)
    bar.finish()
    sys.stdout.write("\n")
    sys.stdout.flush()

    logging.info("Flash kernel succesfully transferred to device.")

    for i in range(1,5)[::-1]: # Wait a few Seconds for the Flash kerne to boot. (the "5" is taken from the ti sample code)
        sys.stdout.write("\r")
        sys.stdout.write("Waiting for flash kernel to boot: {:2}".format(i))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\n")
    sys.stdout.flush()
    # Do Autobaud
    if args.b2:
        try:
            baud2 = int(args.b2)
        except:
            logging.error("value passed for b2 must be an integer!")
            exit(1)
        ser.baudrate = baud2 
    logging.debug("Starting Autobaud!")
    ser.write("A".encode())
    okay = False
    i = 0
    count = 0
    while not okay and count < MAX_AUTOBAUD:
        recData = ser.read()
        if str(recData.decode()) == "A":
            okay = True
            count = 0
        else:
            ser.write("A".encode())
            count += 1
    if count is MAX_AUTOBAUD:
        logging.error("Max Autobaud Tries exceeded!")
        exit(1)
    logging.debug("Application Autobaud Successfull")

    checksum = 0
    txCount = 0
    with open(args.a, "rt") as af:
        data = [a for a in af.read().split(" ")]
        logging.debug("Start sending first 22 bytes from file to DSP")
        bar = progressbar.ProgressBar(maxval=len(data), widgets=[progressbar.Bar("=", "[", "]"),  " ", progressbar.Percentage()])
        bar.start()
        i = 0
        for by in data[:22]: # Info on that can be found in the flash_kernel source itself. I did not find any on that in the documentation, at least not what they are transferring here.
            checksum = checksum + int(by, 16)
            ser.write(bytes([int(by, 16)]))
            bar.update(i+1)
            i += 1
        # waiting for flash kernel to erase the Flash. If done it will return the checksum of the sent data. (16 bit Integer)
        okay = False
        while not okay:
            retCheck = ser.read(2)
            if not retCheck:
                continue
            elif int(retCheck[::-1].hex(), 16) == checksum & 0xFFFF:
                okay = True
                checksum = 0
            else:
                logging.error("Returned Checksum did not match! //0// {:X} != {}".format(checksum, retCheck[::-1].hex()))
                exit(1)
         
        txCount = 0
        totalCount = 0
        wordData = 0x0000
        byteData = 0x0000
        # Send what comes after those reserved bytes
        for by in data[22:]:
            ser.write(bytes([int(by, 16)]))
            checksum = checksum + int(by, 16)
            bar.update(i+1)
            i += 1
            if txCount == 0: # read the length of the Data LSB
                wordData = int(by, 16)
            elif txCount == 1: # read the length of the Data MSB
                byteData = int(by, 16)
                wordData |= (byteData << 8)
            txCount += 1
            totalCount += 1
            if wordData == 0 and txCount > 1: # seems like there should be no 0 within the data? 
                wordData = 0
                byteData = 0
                break
            elif txCount == (2 * (wordData + 3)): # twice the wordData because of sending just 1 byte and not 16 bits - no idea where the "+3" comes from (taken from sample code, can be confirmed in the flash_kernel source) 
                okay = False
                while not okay:
                    retCheck = ser.read(2)
                    if not retCheck:
                        continue
                    elif int(retCheck[::-1].hex(), 16) == checksum & 0xFFFF:
                        okay = True
                        checksum = 0
                    else:
                        logging.error("Returned Checksum did not match! //1// {:X} != {}".format(checksum, retCheck[::-1].hex()))
                        exit(1)
                    wordData = 0
                    byteData = 0
                    txCount = 0
            elif (txCount - 6) % 0x800 == 0 and txCount > 6: # if the already sent data exceeds the device buffer (check flash_kernel source for mor info on how its done) checksum is returned and the program is flashed. Continue after that. 
                okay = False
                while not okay:
                    ser.timeout = 5
                    retCheck = ser.read(2)
                    ser.timeout = 1
                    if not retCheck:
                        continue
                    elif int(retCheck[::-1].hex(), 16) == checksum & 0x00FFFF:
                        okay = True
                        checksum = 0
                    else:
                        logging.error("Returned Checksum did not match! //2// {:X} != {}".format(int(hex(checksum), 16), retCheck[::-1].hex()))
                        exit(1)
        bar.finish()
        logging.info("Application loaded Successful!")
        logging.debug("--- %{} seconds ---".format(time.time() - start_time)) 
        exit(0)