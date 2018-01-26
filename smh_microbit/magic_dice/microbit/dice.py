# -*- coding: utf-8 -*-
"""Wait for a request to read and send orientation.

NOTES:
  1- I wasn't able to make it work with gestures.
  2- Working with accelerometer, x-y-z reads
"""

from microbit import display, sleep, accelerometer
import radio

display.scroll("dice")
display.off()
radio.on()
while True:
    if radio.receive() == 'get_gesture':
        radio.send(','.join(map(str, accelerometer.get_values())))  # 'x,y,z' string
    sleep(500)
