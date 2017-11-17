# -*- coding: utf-8 -*-
"""
"""

import asyncio
import json
import websockets

from utils.orientation import Orientation
from utils.USB_data import USBData


async def ws_func(websocket, path):
    while True:
        data = connection.get_data()
        if data:
            roll_pitch_yaw = orientation.data2roll_pitch_yaw(data)
            # print("{}\t{}\t{}".format( *map(round,roll_pitch_yaw)))
            await websocket.send(json.dumps(roll_pitch_yaw))
            await asyncio.sleep(0.01)


if __name__ == '__main__':
    # Serial connection
    connection = USBData(port="/dev/ttyACM0", baudrate=115200)
    connection.start()
    print("==>  CALIBRATION  <==")
    print("Put yout device:")
    print("\t- On an flat surface")
    print("\t- With the micro:bit logo facing upwards")
    print("\t- With the USB connector pointing to the screen")
    input("... and press ENTER")
    c_roll, c_pitch, c_yaw = Orientation._data2roll_pitch_yaw(connection.get_data())
    orientation = Orientation(c_roll, c_pitch, c_yaw)
    # orientation = Orientation(0,0,0)
    print("\n\n==>  WEB SERVER  <==")
    print("\t- Open the file web/demo_mb.html")
    print("\t- Firefox: OK")
    print("\t- Chromium: chromium-browser --allow-file-access-from-files")
    # Websocket server
    start_server = websockets.serve(ws_func, '127.0.0.1', 5678)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

    connection.close()
