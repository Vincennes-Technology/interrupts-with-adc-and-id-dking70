
#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv
# http://RasPi.tv/ ###Had to split the URL onto two lines###
# how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3

# Modified by DKing:
# additional code added from ipDisplay.py by cut and paste
# modified ADC0832 to use BMC numbering rather than BOARD numbering
# Added functions for reading and converting ADC into strings for LCD display
# Editied to be PEP-8 complient

import time
import RPi.GPIO as GPIO
import ADC0832 as ADC
import subprocess
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()
GPIO.setmode(GPIO.BCM)
ADCSelect = False
oldprintLCDString = None

# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
# So we'll be setting up falling edge detection for both
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ADC setup code
ADC.setup(cs=24, clk=25, dio=8)
#this is where you change the pins for the ADC

#get IP and Host name
while True:
    IPaddr = subprocess.check_output(['hostname', '-I'])
    if len(IPaddr) > 8:
        break
    else:
        time.sleep(2)
Name = subprocess.check_output(['hostname']).strip()
displayText = IPaddr + Name

# now we'll define two threaded callback functions
# these will run in another thread when our events are detected


def my_callbackADC(channel):
    global ADCSelect
    ADCSelect = True


def my_callbackIP(channel):
    global ADCSelect
    ADCSelect = False


# when a falling edge is detected on port 17, regardless of whatever
# else is happening in the program, the function my_callback will be run
GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callbackADC, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callbackIP, bouncetime=300)


def ADCread():
    #This is where the code is from the Internet goes
    # Must return the print string for the LCD panel
    result = ADC.getResult(0)
    voltage = result * 3.3 / 255
    return "Current Voltage = \n %1.3f" % voltage


def IPandHost():
    #This is where the ipDisplay.py code goes to set up the display
    # Must return the print string for the LCD panel
    return displayText

try:
    while True:
        if ADCSelect:
            printLCDString = ADCread()
        else:
            printLCDString = IPandHost()
        if (oldprintLCDString == printLCDString):
            pass
        else:
            lcd.clear()
            lcd.message(printLCDString)
            oldprintLCDString = printLCDString
    time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit