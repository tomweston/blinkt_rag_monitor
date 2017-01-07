#!/usr/bin/env python
"""
Code adapted from https://github.com/randomInteger

Sets the BLINKT LED closest to the usb ports on a Raspberry Pi to RED if it can't reach google, GREEN if it can 
and AMBER if it only has LAN connectivity.

Install into "/home/pi/Pimoroni/blinkt/examples" after installing blinkt from
the link above.

Launch on boot by adding the following to "crontab -e":
@reboot python /home/pi/Pimoroni/blinkt/examples/ragnet_monitor.py &

Kill via shutdown script with:
pgrep -f /home/pi/Pimoroni/blinkt/examples/ragnet_monitor.py | xargs kill -SIGINT

Tested on Rpi3 with Pimoroni blinkt with Raspbian GNU/Linux 8 (jessie).

Date:   01/17
Author:  Tom Weston
"""
import colorsys
import signal
import socket
import time
import sys
from blinkt import set_brightness, set_pixel, show, clear

def signal_handler(signal, frame):
    """
    This signal handler allows us to background
    the process and send it a simple SIGINT to tell it to
    exit cleanly.
    """
    sys.exit(0)

#Start the signal handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)

set_brightness(0.1)
hostname = 'google.com'

while True:
    #Test for the ability to open a socket and resolve DNS.
    try:
        socket.gethostbyname(hostname)
        dns = True
    except socket.gaierror as e:
        dns = False


    while True:
        if dns:
            #We have internet, sets LED to green
                clear()
                set_pixel(7, 0, 255, 0)
        else:
            #DNS and/or internet services are down, sets LED to RED
                clear()
                set_pixel(7, 255, 0, 0)
        show()
        time.sleep(0.05)
