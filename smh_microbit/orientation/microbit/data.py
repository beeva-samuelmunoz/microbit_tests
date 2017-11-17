# -*- coding: utf-8 -*-
"""Utilities to deal with board data.
"""

import sys
from collections import namedtuple



FIELDS = [
    'Acc_X',
    'Acc_Y',
    'Acc_Z',
    # 'Acc_gesture',
    'Mag_X',
    'Mag_Y',
    'Mag_Z',
    'Mag_heading'
]

#4 digits per measure and separating commas
DATA_LENGTH = 4*len(FIELDS) + len(FIELDS)-1 + 10

Data = namedtuple('Data', FIELDS)


#
### TODO: Compression b64 int encoding
#


#
### Serialization
#

def data2msg(data):
    """Serialize data
    """
    return ','.join([str(x) for x in data])+'\n'

def msg2data(msg):
    """Unserialize data
    """
    return Data(*[int(x) for x in msg.split(',')])


#
### Access sensors
#

if sys.platform == 'microbit':  # This won't run on the webserver
    from microbit import accelerometer
    from microbit import compass

    def get_data():
        x, y, z = accelerometer.get_values()
        return Data(
            Acc_X=x,
            Acc_Y=y,
            Acc_Z=z,
            # Acc_gesture=accelerometer.current_gesture(),
            Mag_X=compass.get_x(),
            Mag_Y=compass.get_x(),
            Mag_Z=compass.get_x(),
            Mag_heading=compass.heading()
        )
