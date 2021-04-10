import serial
import matplotlib.pyplot as plt
import numpy as np
import math
from math import pi
import time

car_template ='&{}:{}&'

def write_ser(speed_left,speed_right):
    ser.write(car_template.format(speed_left,speed_right).encode())

def stop():
    write_ser(0,0)



step_time = 1000 # miliseconds

class car_controller():
    def __init__(self,ser,step_time=1000):
        self.ser = ser
        self.step_time = step_time
    def forward(self,distance=18):
        '''
        for 1 second run
        towards lidar is backwards
        18cm ~ 100
        34cm ~150
        44cm ~ 200
        '''
        print(distance)
        speed = 3.8 * abs(distance) + 30
        sign = distance/abs(distance)
        speed = max(speed,100)
        speed = min(speed,255)
        speed = -speed*sign
        write_ser(speed,speed)
        time.sleep(step_time/1000.)

    def turn(self,angle=math.pi/4):
        '''
        for 1 second run
        left is negative
        200 ~ 90 + 45 degrees
        150 ~ 45 degrees
        175 ~ 90 degrees
        '''
        speed = 100/math.pi * abs(angle) + 125
        print(speed)
        sign = angle/abs(angle)
        speed = max(speed,150)
        speed = min(speed,255)   
        speed = speed*sign
        write_ser(-speed,speed)
        time.sleep(step_time/1000.)

    def text_inst(self,direction,distance):
        distance = abs(distance)
        if 'f' in direction:
            self.forward(distance)
        if 'b' in direction:
            self.forward(-1*distance)
        if 'r' in direction:
            self.turn(distance)
        if 'l' in direction:
            self.turn(-1*distance)
    def interpret_text(self,text_inst):

            text = text_inst[0]
            distance = float(text_inst[1:])
            print(text, distance)
            self.text_inst(text,distance)

                       
    def follow_series(self,series):
        for inst in series:
            self.interpret_text(inst)
            

test_series= ['l1.5','r1.5','f30','b30']

if __name__ == "__main__":
    import argparse

    serial_port='/dev/tty.HC-06-DevB'
    baudrate = 115200
    ser = serial.Serial(serial_port, baudrate, timeout=5)
    print(ser)
    car_ctrl = car_controller(ser,step_time=step_time)
    car_ctrl.follow_series(test_series)
    #write_ser(200,200)
