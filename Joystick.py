#!/usr/bin/python
#--------------------------------------
# This script reads data from a
# MCP3008 ADC device using the SPI bus.
#
# Analogue joystick version!
#
# Author : Matt Hawkins
# Date   : 17/04/2014
#
# https://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

# modified By DKing
# Analog Joystick on raspberry pi using ADC0832

import ADC0832
import time
import socket

ADC0832.setup(cs=25, clk=11, dio=8)

SERVERIP = '10.0.0.43'
n = 0

# Define sensor channels
# (channels 3 to 7 unused)
vrx_channel = 0
vry_channel = 1

# Define delay between readings (s)
delay = 0.5

while True:
  # Read the joystick position data
    vrx_pos = ADC0832.getResult(vrx_channel)
    vry_pos = ADC0832.getResult(vry_channel)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVERIP, 8881))
    print "%d : Connected to server" % n,
    data = "'Joystick Postion',n,'X : {}  Y : {}  ".format(vrx_pos, vry_pos)
    sock.sendall(data)
    print ((" Sent:", data))
    sock.close()
    n += 1
    time.sleep(30)
  # Print out results
    print ("--------------------------------------------")