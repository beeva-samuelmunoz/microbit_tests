# -*- coding: utf-8 -*-
"""Get logger data from the usb-serial port
"""

import serial
from threading import Thread

import numpy as np

from . import data


class USBData(Thread):

    def __init__(self, n=20, *args, **kwargs):
        """Intialize device
        """
        self._con = serial.Serial(*args, **kwargs)
        self.running = True  # Stop condition
        self.w_n = n # length of the window
        self.w_data = []  # n last read elements. Running window
        super().__init__()


    def run(self):
        """Thread loop. Read continuously from serial port.
        """
        while len(self.w_data)<self.w_n:  # Fill window
            try:
                self.w_data.append(data.msg2data(self._con.readline().decode()))
            except:
                pass
        while self.running:
            try:
                self.w_data.append(data.msg2data(self._con.readline().decode()))
                self.w_data.pop(0)
            except:
                pass
        self._con.close()


    def get_data(self):
        """Return the last data value
        """
        retval = None
        if self.w_data != []:
            window_data = np.array(self.w_data)
            means = window_data.mean(axis=0)
            # Correct heading, intermediate values range [360,0]
            headings = window_data[:,6]
            headings_rot = (headings+90)%360
            if headings.std()>headings_rot.std():
                means[6] = (headings_rot-90).mean()
            retval = data.Data(*means)
        return retval


    def close(self):
        """Stop webcam and thread
        """
        self.running = False
        self.join()
