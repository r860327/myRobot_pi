#!/usr/bin/env python
from socket import *
from time import ctime
from motor import *
import sys
import RPi.GPIO as GPIO
from cradlecamera import CameraServo
from pwm_control_motor import PWMControlMotor
import utils

# rr = RaspiMotor()
rr = PWMControlMotor()
camera_servo = CameraServo(355, 290)

HOST = ''
PORT = 20000
BUFSIZE = 1024    #1KB
ADDR = (HOST, PORT)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

CAM_HORIZONTAL_DIR = 0
CAM_VERTICAL_DIR = 1
CAM_ANGLE_DECREASE = 0
CAM_ANGLE_INCREASE = 1

if utils.isPython3():
	go_forward_key = b'ud'
	turn_left_key = b'ld'
	turn_right_key = b'rd'
	stop_key = b'dd'

	camera_up_key = b'udc'
	camera_left_key = b'ldc'
	camera_right_key = b'rdc'
	camera_down_key = b'ddc'
else:
	go_forward_key = 'ud'
	turn_left_key = 'ld'
	turn_right_key = 'rd'
	stop_key = 'dd'

	camera_up_key = 'udc'
	camera_left_key = 'ldc'
	camera_right_key = 'rdc'
	camera_down_key = 'ddc'


while True:
	print('waiting for connection...')
	tcpClientSock,clientAddr = tcpSerSock.accept()
	print('...connected from :', clientAddr)
	while True:
		data = tcpClientSock.recv(BUFSIZE)
		if not data:
			break
		print('[%s] %s' % (ctime(), data))

		if utils.isPython3():
			data_array = data.split(b'\n')
		else:
			data_array = data.split('\n')

		if go_forward_key in data_array:
			rr.go_forward(0.075)
		elif turn_left_key in data_array:
			rr.turn_left(0.075)
		elif stop_key in data_array:
			rr.stop()
		elif turn_right_key in data_array:
			rr.turn_right(0.075)
		elif camera_up_key in data_array:
			camera_servo.update_pos(CAM_ANGLE_DECREASE, CAM_VERTICAL_DIR, 5)
		elif camera_down_key in data_array:
			camera_servo.update_pos(CAM_ANGLE_INCREASE, CAM_VERTICAL_DIR, 5)
		elif camera_left_key in data_array:
			camera_servo.update_pos(CAM_ANGLE_INCREASE, CAM_HORIZONTAL_DIR, 5)
		elif camera_right_key in data_array:
			camera_servo.update_pos(CAM_ANGLE_DECREASE, CAM_HORIZONTAL_DIR, 5)
		else:
			print('unknow command')
	tcpClientSock.close()
