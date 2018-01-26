# -*- coding: utf-8 -*-
"""Wait for a request to read and send orientation
"""

from microbit import display, sleep
from microbit import button_a, button_b
from microbit import pin0
import radio

pin0.write_digital(0)

def get_number():
    gesture = False
    while not gesture:
        radio.send('get_gesture')
        sleep(500)  # Wait for msg
        msg = radio.receive()
        try:
            x,y,z = map(int, msg.split(','))
            ax,ay,az = map(abs,(x,y,z))  # Absolute values
            if ax>=ay:
                if ax>=az:
                    gesture = 'x' if x>=0 else '-x'
                else:
                    gesture = 'z' if z>=0 else '-z'
            else:
                if ay>=az:
                    gesture = 'y' if y>=0 else '-y'
                else:
                    gesture = 'z' if z>=0 else '-z'
        except:
            sleep(400)
    return {  # Translation table
        'x':  5,
        '-x': 2,
        'y':  3,
        '-y': 4,
        'z':  6,
        '-z': 1,
    }.get(gesture,0)


display.scroll("magician")
radio.on()
haptic_map = {  # .=1, -=3
    1: '.',
    2: '..',
    3: '-',
    4: '-.',
    5: '-..',
    6: '--'
}
while True:
    if button_a.was_pressed():  # Haptic
        for symbol in haptic_map[get_number()]:
            pin0.write_digital(1)
            if symbol=='.':
                sleep(100)
            else:
                sleep(300)
            pin0.write_digital(0)
            sleep(200)
    elif button_b.was_pressed():  # Screen
        display.show(str(get_number()))
        sleep(1500)
        display.clear()
    sleep(600)
