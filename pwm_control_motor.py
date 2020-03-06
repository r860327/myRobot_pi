#!/usr/bin/python

from Raspi_PWM_Servo_Driver import PWM
import time
import utils


LEFT_WHEEL_CHANNEL = 8
RIGHT_WHEEL_CHANNEL = 7


class PWMControlMotor:
    """
    This class is used to control car with pwm signal.
    The range of pulse width is from 0 to 4095.
    But it seems the min pulse width must be set to 800 to enable car to move.
    """
    def __init__(self, default_h_pos=0, default_v_pos=0):
        self.pwm = PWM(0x6F, debug=True)
        self.pwm.setPWMFreq(50)
        self.current_horizontal_pos = default_h_pos
        self.current_vertical_pos = default_v_pos
        self.pwm.setPWM(LEFT_WHEEL_CHANNEL, 0, int(self.current_horizontal_pos))
        self.pwm.setPWM(RIGHT_WHEEL_CHANNEL, 0, int(self.current_vertical_pos))

    def set_pulse_width(self, wheel_channel, pulse_width):
        self.pwm.setPWM(wheel_channel, 0, pulse_width)

    def go_forward(self, seconds=0):
        self.set_pulse_width(LEFT_WHEEL_CHANNEL, 4000)
        self.set_pulse_width(RIGHT_WHEEL_CHANNEL, 4000)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def turn_left(self, seconds=0):
        self.set_pulse_width(LEFT_WHEEL_CHANNEL, 0)
        self.set_pulse_width(RIGHT_WHEEL_CHANNEL, 3000)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def turn_right(self, seconds=0):
        self.set_pulse_width(RIGHT_WHEEL_CHANNEL, 0)
        self.set_pulse_width(LEFT_WHEEL_CHANNEL, 3000)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def stop(self, seconds=0):
        self.set_pulse_width(RIGHT_WHEEL_CHANNEL, 0)
        self.set_pulse_width(LEFT_WHEEL_CHANNEL, 0)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()


if __name__ == '__main__':
    pwm_control_motor = PWMControlMotor()
    while True:
        if utils.isPython3():
            direction = input("please input 'l' or 'r' or 'g' or 's':")
        else:
            direction = raw_input("please input 'l' or 'r' or 'g' or 's':")

        if direction == 'l':
            pwm_control_motor.turn_left(2)
        elif direction == 'r':
            pwm_control_motor.turn_right(2)
        elif direction == 'g':
            pwm_control_motor.go_forward(2)
        elif direction == 's':
            pwm_control_motor.stop(2)
        else:
            print("don't support this command!")
