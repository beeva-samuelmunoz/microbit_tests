# -*- coding: utf-8 -*-
"""
"""

import math

def data2roll_pitch_yaw(data):
    """
    Return:
    retval: roll, pitch, yaw

    https://theccontinuum.com/2012/09/24/arduino-imu-pitch-roll-from-accelerometer/
    """
    #Normalize input [-1, 1]
    x,y,z = [ i/1024.0 for i in (data.Acc_X, data.Acc_Y, data.Acc_Z) ]
    roll = math.atan2(-x, z) * 57.3
    pitch = math.atan2( (y) , math.sqrt(x**2 + z**2)) * 57.3
    yaw = data.Mag_heading
    if roll<-90 or 90<roll:
        pitch = -pitch
    return (-roll, pitch, yaw)
