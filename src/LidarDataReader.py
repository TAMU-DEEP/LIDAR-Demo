import serial
import matplotlib.pyplot as plt
import numpy as np
import math
from math import pi
import time

class LidarDataReader():
    def __init__(self,ser):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.ser = ser

        #Array of points that will be plotted out
        self.points_x = [0]*360
        self.points_y = [0]*360

        self.c_vals = [-math.sin(i * pi/ 180.0) for i in range(360)]
        self.s_vals = [math.cos(i * pi/ 180.0) for i in range(360)]

        self.axis = plt.axis([-2500, 2500, -2500, 2500])

    def compute_angle_distance(self, angle, data):
        """
        Takes the angle (an int, from 0 to 359) and the last of four bytes of data in the order they arrived.
        """
        x = data[0] #distance
        x1= data[1] #distance mask
        x2= data[2] #distance quality
        x3= data[3] #distance quality mask
        c = self.c_vals[angle - 143]
        s = self.s_vals[angle - 143]
        dist_mm = x | (( x1 & 0x3f) << 8) # distance is coded on 13 bits ? 14 bits ?
        quality = x2 | (x3 << 8) # quality is on 16 bits
        dist_x = dist_mm*c
        dist_y = dist_mm*s
        return dist_x, dist_y

    def compute_angle_distance_list(self, angle_index, data_list):
        angle_x_y = []
        for i, data in enumerate(data_list):
            angle = angle_index * 4 + i
            dist_x, dist_y = self.compute_angle_distance(angle, data)
            angle_x_y.append([angle, dist_x, dist_y])
        return angle_x_y

    def read_from_arduino(self):
        b = ord(self.ser.read(1))
        #check for start bit
        if b != 0xFA: return -1
        b = ord(self.ser.read(1))
        #check validity of angle bit
        if not (b >= 0xA0 and b <= 0xF9): return -2
        index = b - 0xA0
        speed = [b for b in self.ser.read(2)]
        b_data = [[ b for b in self.ser.read(4)] for i in range(4)]
        return index, b_data

    def one_iteration(self):
        #read data from arduino
        result = self.read_from_arduino()
        #ignore bad reads
        if result == -1 or result == -2: return -1
        index, data = result
        angle_x_y = self.compute_angle_distance_list(index, data)
        angle,x,y = list(zip(*angle_x_y))
        #update
        for a,x,y in angle_x_y:
            self.points_x[a] = x
            self.points_y[a] = y
        #successfull update
        return angle[0]

    def plot(self, pause=.01):
        ldr.scatter = plt.scatter(ldr.points_x, ldr.points_y, color='blue')
        plt.pause(pause)
        ldr.scatter.remove()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="run basic lidar module")
    parser.add_argument("-m", "--max", type=int, default=-1)
    parser.add_argument("-r", "--record", action="store_true")
    args = parser.parse_args()

    serial_port='/dev/tty.HC-06-DevB'
    baudrate = 115200
    ser = serial.Serial(serial_port, baudrate, timeout=5)
    ldr = LidarDataReader(ser=ser)
    
    record = args.record
    if record: frames = []
    max_val = args.max
    i = 0
    while True:
        #control max number of frames
        if i > max_val and max_val > 0: break
        angle = ldr.one_iteration()
        #update plot on 0
        if angle == 0:
            ldr.plot()
            if record: frames.append([ldr.points_x,ldr.points_y])
            i += 1

    if record:      
        import pickle as pkl 
        pkl.dump(frames,open("recorded_lidar.pkl",'wb'))

