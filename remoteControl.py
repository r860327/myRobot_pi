#!/usr/bin/env python
from socket import *
from time import ctime
from motor import *
import sys
import RPi.GPIO as GPIO
from cradlecamera import CameraServo

rr = RaspiMotor()
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

while True:
	print 'waiting for connection...'
	tcpClientSock,clientAddr = tcpSerSock.accept()
	print '...connected from :', clientAddr
	while True:
		data = tcpClientSock.recv(BUFSIZE)
		if not data:
			break
		print '[%s] %s' % (ctime(), data)

		if data == 'ud':
			rr.forward(0.075)
		elif data == 'ld':
			rr.left(0.075)
		elif data == 'dd':
			rr.reverse(0.075)
		elif data == 'rd':
			rr.right(0.075)
		elif data == 'udc':
			camera_servo.update_pos(CAM_ANGLE_DECREASE, CAM_VERTICAL_DIR, 5)
		elif data == 'ddc':
			camera_servo.update_pos(CAM_ANGLE_INCREASE, CAM_VERTICAL_DIR, 5)
		elif data == 'ldc':
			camera_servo.update_pos(CAM_ANGLE_INCREASE, CAM_HORIZONTAL_DIR, 5)
		elif data == 'rdc':
			camera_servo.update_pos(CAM_ANGLE_DECREASE, CAM_HORIZONTAL_DIR, 5)
		else:
			print 'unknow command'
	tcpClientSock.close()
tcpSerSock.close()
