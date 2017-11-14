# -*- coding: utf-8 -*-
"""
"""

import sys

import vispy
vispy.use(app='pyglet', gl=None)

from vispy import app, gloo
from vispy.visuals import CubeVisual, transforms
from vispy.color import Color

from utils.orientation import Orientation
from utils.USB_data import USBData



class Canvas(app.Canvas):
    def __init__(self, connection, orientation):
        self.con = connection
        self.orientation = orientation
        app.Canvas.__init__(self, 'Cube', keys='interactive', size=(400, 400))
        self.cube = CubeVisual((7.0, 4.0, 0.3), color=Color(color='grey', alpha=0.1, clip=False), edge_color="black")

        # Create a TransformSystem that will tell the visual how to draw
        self.cube_transform = transforms.MatrixTransform()
        self.cube.transform = self.cube_transform
        self._timer = app.Timer('0.05', connect=self.on_timer, start=True)
        self.show()

    def on_close(self, event):
        self.con.close()

    def on_resize(self, event):
        # Set canvas viewport and reconfigure visual transforms to match.
        vp = (0, 0, self.physical_size[0], self.physical_size[1])
        self.context.set_viewport(*vp)
        self.cube.transforms.configure(canvas=self, viewport=vp)

    def on_draw(self, event):
        gloo.set_viewport(0, 0, *self.physical_size)
        gloo.clear('white', depth=True)
        self.cube.draw()

    def on_timer(self, event):
        data = connection.get_data()
        if data:
            roll, pitch, yaw = orientation.data2roll_pitch_yaw(data)
            # print("{}\t{}\t{}".format( *map(round,(roll,pitch,yaw))))
            self.cube_transform.reset()
            self.cube_transform.rotate(pitch, (1, 0, 0))  # Pitch
            self.cube_transform.rotate(roll,  (0, 1, 0))  # Roll
            self.cube_transform.rotate(yaw,   (0, 0, 1))  # Yaw
            self.cube_transform.scale((20, 20, 0.001))
            self.cube_transform.translate((200, 200))
            self.update()


if __name__ == '__main__':
    connection = USBData(port="/dev/ttyACM0", baudrate=115200)
    connection.start()
    print("Calibration\nSet your device on the origin and press ENTER.\n")
    input("Waiting...")
    c_roll, c_pitch, c_yaw = Orientation._data2roll_pitch_yaw(connection.get_data())
    orientation = Orientation(c_roll, c_pitch, c_yaw)
    win = Canvas(connection, orientation)
    win.show()
    if sys.flags.interactive != 1:
        win.app.run()
