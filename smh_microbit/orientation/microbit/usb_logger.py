# -*- coding: utf-8 -*-
"""Read sensors and write the msg in the serial port.
"""

from microbit import uart
from data import get_data, data2msg

uart.init(115200)
while True:
    uart.write(data2msg(get_data()))
