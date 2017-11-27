# -*- coding: utf-8 -*-
"""Read sensor data and broadcast it over radio.
"""

from microbit import display, sleep
import radio

from data import DATA_LENGTH, get_data, data2msg, PERIOD_MS


display.scroll("logger")

radio.config(length=DATA_LENGTH)
radio.on()

while True:
    radio.send(data2msg(get_data()))
    sleep(PERIOD_MS)
