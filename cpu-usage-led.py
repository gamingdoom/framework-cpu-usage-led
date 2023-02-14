#!/usr/bin/env python

# Change the LED based on CPU usage
# Inspired by https://community.frame.work/t/reprogramming-the-leds-for-the-holidays/12906

import psutil
import time
import subprocess
import math
import signal

shouldExit = False

# Possible values: power, left, right. Power is the fingerprint sensor's LED.
ledsToChange = ["power"]

# Privilege escalation command to use. fw-ectool needs to be run as root.
#privilegeEscalation = "sudo"
privilegeEscalation = None

def changeColor(color, led):
    colorName = "white"

    # Convert 0-4 to color names
    match color:
        # 0%
        case 0:
            colorName = "green"

        # 0% < load < 25%
        case 1:
            colorName = "green"

        # 25% < load < 50%
        case 2:
            colorName = "yellow"
        
        # 50% < load < 75%
        case 3:
            colorName = "amber"

        # 75% < load < 100%
        case 4:
            colorName = "red"

    changeLed(colorName, led)

def changeLed(colorName, led):
    if privilegeEscalation:
        subprocess.run([privilegeEscalation, "fw-ectool", "led", led, colorName])
    else:
        subprocess.run(["fw-ectool", "led", led, colorName])

# Check if lid is open or closed
def isLidOpen():
    f = open("/proc/acpi/button/lid/LID0/state")
    if f.read()[12:16] == "open":
        return True
    else:
        return False

def resetLeds():
    for led in ledsToChange:
        changeLed("auto", led)


# We need to reset led state after exiting so we register a signal handler.
def signal_handler(sig, frame):
    print("exiting...")
    
    resetLeds()
    exit(0)

def main():
    # Main Loop
    while not shouldExit:
        if isLidOpen():
            for led in ledsToChange:
                changeColor(math.ceil(psutil.cpu_percent() / 25), led)
        else:
            resetLeds()

        # Sleep for 1 second. 
        time.sleep(0.5)

    return

if __name__ == "__main__":
    # We need to reset the Leds back to auto if we close
    signalsToHandle = [signal.SIGINT, signal.SIGTERM]
    for sig in signalsToHandle:
        signal.signal(sig, signal_handler)
    
    main()

    resetLeds()
