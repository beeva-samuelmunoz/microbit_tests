# -*- coding: utf-8 -*-
"""Read the radio messages and write them in the serial port.
"""

from microbit import uart
import radio

from data import DATA_LENGTH


radio.config(length=DATA_LENGTH)
radio.on()
uart.init(115200)

while True:
    data = radio.receive()
    if data:
        uart.write(data)
