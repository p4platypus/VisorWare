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
from cobot_cloud import g_cobot_info, cred

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

def machineInfoDisplay(machineBig, machineMiddle, machineSmall):
    install = [machineBig[1], machineMiddle[1], machineSmall[1]]
    minute = [machineBig[0], machineMiddle[0], machineSmall[0]]
    size = ["big", "middle", "small"]
    info = ""
    if machineBig[1] and machineMiddle[1] and machineSmall[1]:
        if machineBig[0] != 0 and machineMiddle[0] != 0 and machineSmall[0] != 0:
            info = info + "Wait for " + size[minute.index(min(minute))] + ", " + str(min(minute)) + " mins"
        else:
            info = info + "Replace "
            for i in range(3):
                if minute[i] == 0:
                    info = info + size[i] + ", "
    else:
        info = info + "Install "
        for i in range(3):
            if install[i] == False:
                info = info + size[i] + ", "
    return info

def machineInfo(debugStatus):
    print("Starting live machine information stream...")
    TempDisp = 1
    HumidDisp = 0
    while GPIO.input(homeb) == True:
        font = ImageFont.load_default()
        machineABig = g_cobot_info.read_machine_status("A", "big")
        machineAMiddle = g_cobot_info.read_machine_status("A", "middle")
        machineASmall = g_cobot_info.read_machine_status("A", "small")
        machineBBig = g_cobot_info.read_machine_status("B", "big")
        machineBMiddle = g_cobot_info.read_machine_status("B", "middle")
        machineBSmall = g_cobot_info.read_machine_status("B", "small")
        machineCBig = g_cobot_info.read_machine_status("C", "big")
        machineCMiddle = g_cobot_info.read_machine_status("C", "middle")
        machineCSmall = g_cobot_info.read_machine_status("C", "small")
        machineA_status = "A: " + machineInfoDisplay(machineABig, machineAMiddle, machineASmall)
        machineB_status = "B: " + machineInfoDisplay(machineBBig, machineBMiddle, machineBSmall)
        machineC_status = "C: " + machineInfoDisplay(machineCBig, machineCMiddle, machineCSmall)

        VisionEngine.disptext(machineA_status, machineB_status, machineC_status, " ", 0, 0, 0, 0, 0, 12, 24, 36, debugStatus, '0')
