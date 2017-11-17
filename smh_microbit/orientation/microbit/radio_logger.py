# -*- coding: utf-8 -*-
"""Read sensor data and broadcast it over radio.
"""

import radio

from data import DATA_LENGTH, get_data, data2msg


radio.config(length=DATA_LENGTH)
radio.on()

while True:
    radio.send(data2msg(get_data()))
