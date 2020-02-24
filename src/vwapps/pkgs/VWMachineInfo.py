import time
import RPi.GPIO as GPIO
import os
import subprocess
import requests
import math
from termCol import *
import VWUtils
import VisionEngine

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from test import CobotInfo

cobot = CobotInfo()

#######################################
# Display Initialization. DO NOT ALTER!
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
width = disp.width
height = disp.height
padding = -2
top = padding
bottom = height=padding
x = 0
font = ImageFont.load_default()
#
#######################################

##################################################
# Button input board initialization. DO NOT ALTER!
GPIO.setmode(GPIO.BCM)
leftb = 17
homeb = 27
rightb = 22
screenb = 4
GPIO.setup(leftb, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(homeb, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rightb, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(screenb, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
##################################################

def machineStatusDecode(machineStatus):
    if machineStatus == 1:
        return("busy")
    elif machineStatus == 2:
        return("free")
    else:
        return("unknown")

def machineInfoDisplay(machineBig, machineMiddle, machineSmall):
    if machineCoilSize == 1:
        return("big")
    elif machineCoilSize == 2:
        return("med")
    elif machineCoilSize == 3:
        return("small")
    else:
        return("none")

def machineInfo(debugStatus):
    print("Starting live machine information stream...")
    TempDisp = 1
    HumidDisp = 0
    while GPIO.input(homeb) == True:
        font = ImageFont.load_default()
        #machine1 = 
        #machine2 = 
        #machine3 = 
        machine1_status = "Machine 1: " 
        machine2_status = "Machine 2: " 
        machine3_status = "Machine 3: " 

        VisionEngine.disptext(machine1_status, machine2_status, machine3_status, " ", 0, 0, 0, 0, 0, 12, 24, 36, debugStatus, '0')
