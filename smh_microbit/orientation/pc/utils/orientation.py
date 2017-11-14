# -*- coding: utf-8 -*-
"""
"""

import math

class Orientation:
    """Class to get the orientation of the device.
    """

    def __init__(self, roll=0, pitch=0, yaw=0):
        """Initial calibration
        """
        self.c_roll, self.c_pitch, self.c_yaw = roll, pitch, yaw


    def data2roll_pitch_yaw(self, data):
        """Apply the inital calibration.
        """
        roll, pitch, yaw = self._data2roll_pitch_yaw(data)
        new_roll = (-roll+self.c_roll)%360
        if 90<new_roll<270 and 90<yaw<270:
            pitch = -pitch
        return (
            new_roll,
            (pitch-self.c_pitch)%360,
            (yaw-self.c_yaw)%360
        )

    @staticmethod
    def _data2roll_pitch_yaw(data):
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
        return (roll, pitch, yaw)
