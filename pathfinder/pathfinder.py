from math import fabs, sin, cos, pi
import sys

sys.path.append('/root/pybotics')

from board.arietta.pin.digital import Digital
from board.arietta.pin.pwm import PWM


class Pathfinder(object):

    def __init__(self):
        self.motor_0_direction = Digital(33, 'out')
        self.motor_1_direction = Digital(35, 'out')
        self.motor_2_direction = Digital(37, 'out')
        self.motor_0_speed = PWM(0)
        self.motor_1_speed = PWM(1)
        self.motor_2_speed = PWM(2)

    def move(self, x, y, w):
        _motor_0 = -x * sin(pi/3) + (y * cos(pi/3)) + w
        _motor_1 = -y + w
        _motor_2 = x * sin(pi/3) + (y * cos(pi/3)) + w

        _max = max([fabs(_motor_0), fabs(_motor_1), fabs(_motor_2)])
        if _max > 1:
            _motor_0 /= _max
            _motor_1 /= _max
            _motor_2 /= _max
        _d, _spd = self._parse_speed(_motor_0)
        self.motor_0_direction.write(_d)
        self.motor_0_speed.duty_cycle = int(self.motor_0_speed.period * _spd)

        _d, _spd = self._parse_speed(_motor_1)
        print _d, _spd
        self.motor_1_direction.write(_d)
        self.motor_1_speed.duty_cycle = int(self.motor_1_speed.period * _spd)

        _d, _spd = self._parse_speed(_motor_2)
        print _d, _spd
        self.motor_2_direction.write(_d)
        self.motor_2_speed.duty_cycle = int(self.motor_2_speed.period * _spd)

    def _parse_speed(self, speed):
        if speed == 0:
            return 0, 0
        elif speed > 0:
            return 0, speed
        elif speed < 0:
            return 1, 1 + speed
