#raspirobotboard.py Library

import RPi.GPIO as GPIO
import serial
import time

DEVICE = '/dev/ttyAMA0'
BAUD = 9600

LEFT_ENABLE_PIN = 4
LEFT_FORWARD_PIN = 17
LEFT_REVERSE_PIN = 27

RIGHT_ENABLE_PIN = 10
RIGHT_FORWARD_PIN = 11
RIGHT_REVERSE_PIN = 9

class RaspiMotor:

    '''
    This class is for L298N motor driver board
    '''

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(LEFT_ENABLE_PIN, GPIO.OUT)
        GPIO.setup(LEFT_FORWARD_PIN, GPIO.OUT)
        GPIO.setup(LEFT_REVERSE_PIN, GPIO.OUT)
        GPIO.setup(RIGHT_ENABLE_PIN, GPIO.OUT)
        GPIO.setup(RIGHT_FORWARD_PIN, GPIO.OUT)
        GPIO.setup(RIGHT_REVERSE_PIN, GPIO.OUT)

        GPIO.output(LEFT_ENABLE_PIN, 1)
        GPIO.output(RIGHT_ENABLE_PIN, 1)

        self.ser = None

    def enable_motor(self, left_enable, enable):
        GPIO.output(LEFT_ENABLE_PIN, left_enable)
        GPIO.output(RIGHT_ENABLE_PIN, right_enable)

    def set_motors(self, left_forward, left_reverse, right_forward, right_reverse):
        GPIO.output(LEFT_FORWARD_PIN, left_forward)
        GPIO.output(LEFT_REVERSE_PIN, left_reverse)
        GPIO.output(RIGHT_FORWARD_PIN, right_forward)
        GPIO.output(RIGHT_REVERSE_PIN, right_reverse)

    def forward(self, seconds=0):
        self.set_motors(1, 0, 1, 0)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def stop(self):
        self.set_motors(0, 0, 0, 0)
 
    def reverse(self, seconds=0):
        self.set_motors(0, 1, 0, 1)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()
    
    def left(self, seconds=0):
        self.set_motors(0, 1, 1, 0)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def right(self, seconds=0):
        self.set_motors(1, 0, 0, 1)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def test(self):
        raw_input("forward")
        self.forward(2)

        raw_input("left")
        self.left(2)

        raw_input("right")
        self.right(2)

        raw_input("reverse")
        self.reverse(2)

        raw_input("stop")
        self.stop()


        raw_input("End of test")

if __name__ == '__main__':
    motor = RaspiMotor()
    while True:
        cmd = raw_input('please input motor command:')
        if cmd == 'q':
            break
        if cmd == 'w':
            motor.forward(2)
        elif cmd == 'a':
            motor.left(2)
        elif cmd == 'd':
            motor.right(2)
        elif cmd == 's':
            motor.reverse(2)
        else:
            print('unknow command')
