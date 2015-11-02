from math import fabs, sin, cos, pi
import smbus
import time


class Pathfinder(object):

    def __init__(self):
        self.i2c_bus = smbus.SMBus(0)
        self.arduino = 0x08

    def move(self, x, y, w):
        _motor_0 = -x * sin(pi/3) + (y * cos(pi/3)) + w
        _motor_1 = -y + w
        _motor_2 = x * sin(pi/3) + (y * cos(pi/3)) + w

        _max = max([fabs(_motor_0), fabs(_motor_1), fabs(_motor_2)])
        if _max > 1:
            _motor_0 /= _max
            _motor_1 /= _max
            _motor_2 /= _max
        msg = "(%.2f,%.2f,%.2f,0)" % (_motor_0, _motor_1, _motor_2)
        for part in msg:
            self.i2c_bus.write_byte(self.arduino, ord(part))
        time.sleep(0.1)
