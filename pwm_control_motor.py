#!/usr/bin/python

from Raspi_PWM_Servo_Driver import PWM
import RPi.GPIO as GPIO
import time
import utils


LEFT_WHEEL_CHANNEL = 8
RIGHT_WHEEL_CHANNEL = 7

L298N_I1_PIN = 4
L298N_I2_PIN = 17

L298N_I3_PIN = 23
L298N_I4_PIN = 24


class PWMControlMotor:
    """
    This class is used to control car with pwm signal.
    The range of pulse width is from 0 to 4095.
    But it seems the min pulse width must be set to 800 to enable car to move.
    """
    def __init__(self, default_h_pos=0, default_v_pos=0):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(L298N_I1_PIN, GPIO.OUT)
        GPIO.setup(L298N_I2_PIN, GPIO.OUT)
        GPIO.setup(L298N_I3_PIN, GPIO.OUT)
        GPIO.setup(L298N_I4_PIN, GPIO.OUT)

        GPIO.output(L298N_I1_PIN, 0)
        GPIO.output(L298N_I2_PIN, 0)
        GPIO.output(L298N_I3_PIN, 0)
        GPIO.output(L298N_I4_PIN, 0)

        self.pwm = PWM(0x6F, debug=True)
        self.pwm.setPWMFreq(50)
        self.current_horizontal_pos = default_h_pos
        self.current_vertical_pos = default_v_pos
        self.pwm.setPWM(LEFT_WHEEL_CHANNEL, 0, int(self.current_horizontal_pos))
        self.pwm.setPWM(RIGHT_WHEEL_CHANNEL, 0, int(self.current_vertical_pos))

    def _set_direction(self, wheel, direction=0):
        """
        :param wheel: 0 for left wheel, 1 for right wheel
        :param direction: 0 for go ahead, 1 for back
        :return:
        """
        if wheel == 0:
            if direction == 0:
                GPIO.output(L298N_I1_PIN, 1)
                GPIO.output(L298N_I2_PIN, 0)
                print('set I1 to 1 and I2 to 0')
            elif direction == 1:
                GPIO.output(L298N_I1_PIN, 0)
                GPIO.output(L298N_I2_PIN, 1)
                print('set I1 to 0 and I2 to 1')
            else:
                print("unknown direction: {}".format(direction))
        elif wheel == 1:
            if direction == 0:
                GPIO.output(L298N_I3_PIN, 0)
                GPIO.output(L298N_I4_PIN, 1)
                print('set I3 to 0 and I4 to 1')
            elif direction == 1:
                GPIO.output(L298N_I3_PIN, 1)
                GPIO.output(L298N_I4_PIN, 0)
                print('set I3 to 1 and I4 to 0')
            else:
                print('unknown direction: {}'.format(direction))
        else:
            print('unknown wheel {}'.format(wheel))

    def set_pulse_width(self, wheel_channel, pulse_width):
        self.pwm.setPWM(wheel_channel, 0, pulse_width)

    def go_forward(self, seconds=0):
        self._set_direction(0, 0)
        self._set_direction(1, 0)

        self.set_pulse_width(LEFT_WHEEL_CHANNEL, 4000)
        self.set_pulse_width(RIGHT_WHEEL_CHANNEL, 4000)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def turn_left(self, seconds=0):
        self._set_direction(0, 1)
        self._set_direction(1, 0)

        self.set_pulse_width(LEFT_WHEEL_CHANNEL, 4000)
        self.set_pulse_width(RIGHT_WHEEL_CHANNEL, 4000)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def turn_right(self, seconds=0):
        self._set_direction(0, 0)
        self._set_direction(1, 1)
        self.set_pulse_width(RIGHT_WHEEL_CHANNEL, 4000)
        self.set_pulse_width(LEFT_WHEEL_CHANNEL, 4000)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def stop(self):
        self._set_direction(0, 1)
        self._set_direction(1, 1)
        self.set_pulse_width(RIGHT_WHEEL_CHANNEL, 0)
        self.set_pulse_width(LEFT_WHEEL_CHANNEL, 0)

    def back_up(self, seconds=0):
        self._set_direction(0, 1)
        self._set_direction(1, 1)
        self.set_pulse_width(RIGHT_WHEEL_CHANNEL, 4000)
        self.set_pulse_width(LEFT_WHEEL_CHANNEL, 4000)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def clean_gpio(self):
        GPIO.cleanup()

if __name__ == '__main__':
    pwm_control_motor = PWMControlMotor()
    while True:
        if utils.isPython3():
            direction = input("please input 'l' or 'r' or 'g' or 's' or 'b':")
        else:
            direction = raw_input("please input 'l' or 'r' or 'g' or 's' or 'b':")

        if direction == 'l':
            pwm_control_motor.turn_left(2)
        elif direction == 'r':
            pwm_control_motor.turn_right(2)
        elif direction == 'g':
            pwm_control_motor.go_forward(2)
        elif direction == 's':
            pwm_control_motor.stop()
        elif direction == 'b':
            pwm_control_motor.back_up(2)
        elif direction == 'quit':
            break
        else:
            print("don't support this command!")

    pwm_control_motor.clean_gpio()