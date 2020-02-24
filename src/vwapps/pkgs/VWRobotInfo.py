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

def robotStatusDecode(robotStatus):
    if robotStatus == 0:
        return("free")
    elif robotStatus == 1:
        return("busy")
    elif robotStatus == 2:
        return("stopped")
    else:
        return("unknown")

def robotInfo(debugStatus):
    print("Starting live robot information stream...")
    TempDisp = 1
    HumidDisp = 0
    while GPIO.input(homeb) == True:
        font = ImageFont.load_default()
        #robotA = 
        #robotB = 
        #robotC = 
        robot1_status = "Robot A: " + robotStatusDecode(robot1) + ", " + robotCoilSizeDecode(robot1)
        robot2_status = "Robot B: " + robotStatusDecode(robot2) + ", " + robotCoilSizeDecode(robot2)
        robot3_status = "Robot C: " + robotStatusDecode(robot3) + ", " + robotCoilSizeDecode(robot3)

        VisionEngine.disptext(robot1_status, robot2_status, robot3_status, " ", 0, 0, 0, 0, 0, 12, 24, 36, debugStatus, '0')
