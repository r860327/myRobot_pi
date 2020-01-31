#!/usr/bin/python

from Raspi_PWM_Servo_Driver import PWM
import time


HORIZONTAL_CHANNEL = 0
VERTICAL_CHANNEL = 1

servoMin = 150  # Min pulse length out of 4096
servoMax = 565  # Max pulse length out of 4096

servoVerticalMin = 150
servoVerticalMax = 450

START_HORIZONTAL_POS = 355#should be the centre postion of horizontal
START_VERTICAL_POS = 250    #should be the suitable postion of vertical

class CameraServo:
    def __init__(self, default_h_pos = START_HORIZONTAL_POS, default_v_pos = START_VERTICAL_POS):
        self.pwm = PWM(0x6F, debug=True)
        self.pwm.setPWMFreq(50)
        self.current_horizontal_pos = default_h_pos
        self.current_vertical_pos = default_v_pos
        self.pwm.setPWM(HORIZONTAL_CHANNEL, 0, int(self.current_horizontal_pos))
        self.pwm.setPWM(VERTICAL_CHANNEL, 0, int(self.current_vertical_pos))


    def convert_angle_to_pwm(self, angle):
        return int((servoMax - servoMin) * angle / 180)

    def set_postion(self, horizontal_pos, vertical_pos):
        '''
        The postion is angle
        0 ---->  servoMin
        180 ----> servoMax
        ''' 
        horizontal_pwm = self.convert_angle_to_pwm(horizontal_pos) + 150
        vertical_pwm = self.convert_angle_to_pwm(vertical_pos) + 150
        if horizontal_pwm < servoMin or horizontal_pwm > servoMax:
            print("invaild horizontal_pwm!")
            return
        if vertical_pwm < servoVerticalMin or vertical_pwm > servoVerticalMax:
            print("invaild vertical_pwm")
            return

        print("set horizontal to: %s " % horizontal_pwm)
        print("set vertical to: %s " % vertical_pwm)

        self.pwm.setPWM(HORIZONTAL_CHANNEL, 0, int(horizontal_pwm))
        self.pwm.setPWM(VERTICAL_CHANNEL, 0, int(vertical_pos))

    def update_pos(self, direction, x_or_y, delta_angle):
        '''
        This function is used to update postion by a solid step
        direction: 1, increase; 0, decrease
        x_or_y: 0, horizontal; 1, vertical
        delta_angle: position change in angle
        '''
        delta_pwm = self.convert_angle_to_pwm(delta_angle)
        if x_or_y == 0:
            if direction == 0:
                if self.current_horizontal_pos > servoMin:
                    self.current_horizontal_pos = max(self.current_horizontal_pos - delta_pwm, servoMin)
            elif direction == 1:
                if self.current_horizontal_pos < servoMax:
                    self.current_horizontal_pos = min(self.current_horizontal_pos + delta_pwm, servoMax)
            else:
                print("unknow direction!")
        elif x_or_y == 1:
            if direction == 0:
                if self.current_vertical_pos > servoVerticalMin:
                    self.current_vertical_pos = max(self.current_vertical_pos - delta_pwm, servoMin)
            elif direction == 1:
                if self.current_vertical_pos < servoVerticalMax:
                    self.current_vertical_pos = min(self.current_vertical_pos + delta_pwm, servoMax)
            else:
                print("unknow direction!")
        else:
            print("unknow x_or_y!")
        print("set self.current_horizontal_pos: " + str(self.current_horizontal_pos))
        print("set self.current_vertical_pos: " + str(self.current_vertical_pos))
        self.pwm.setPWM(HORIZONTAL_CHANNEL, 0, int(self.current_horizontal_pos))
        self.pwm.setPWM(VERTICAL_CHANNEL, 0, int(self.current_vertical_pos))
        

if __name__ == '__main__':
    camera_servo = CameraServo()
    while True:
        #v_pos = raw_input("please v_pos:")
        #h_pos = raw_input("please h_pos:")
        #if v_pos == 'q' or h_pos == 'q':
        #    break
        #camera_servo.set_postion(int(h_pos), int(v_pos))
        direction = input("please input direction:")
        x_or_y = input("please input x_or_y:")
        delta_angle = input("please input delta_angle:")
        camera_servo.update_pos(int(direction), int(x_or_y), int(delta_angle))
