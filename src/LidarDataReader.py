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
        self.points_x = np.full(360,0)
        self.points_y = np.full(360,0)
        self.distance = np.full(360,0)

        self.angle = np.linspace(0,359,360)
        self.c_vals = -np.sin(self.angle * pi/180.)
        self.s_vals = np.cos(self.angle * pi/180.)

        self.axis = plt.axis([-2500, 2500, -2500, 2500])

    def compute_distance(self,data):
        x = data[0] #distance
        x1= data[1] #distance mask
        x2= data[2] #distance quality
        x3= data[3] #distance quality mask
        if x1 & 0x80:
             return 0
        dist_mm = x | (( x1 & 0x3f) << 8) # distance is coded on 13 bits ? 14 bits ?
        return dist_mm

    def update_angle_distance_list(self, angle_index, data_list):
        for i, data in enumerate(data_list):
            angle = angle_index * 4 + i
            self.distance[angle] = self.compute_distance(data)

    def read_from_arduino(self):
        b = ord(self.ser.read(1))
        #check for start bit
        if b != 0xFA: return -1
        b = ord(self.ser.read(1))
        #check validity of angle bit
        if not (b >= 0xA0 and b <= 0xF9): return -2
        index = b - 0xA0
        speed = [b for b in self.ser.read(2)]
        b_data = [[b for b in self.ser.read(4)] for i in range(4)]
        return index, b_data

    def one_iteration(self):
        #read data from arduino
        result = self.read_from_arduino()
        #ignore bad reads
        if result == -1 or result == -2: return -1
        index, data = result
        self.update_angle_distance_list(index, data)
        return index

    def get_x_y(self, min_distance=1):
        x,y = self.distance*self.c_vals, self.distance*self.s_vals
        d_x_y_a = list(zip(self.distance,x,y,self.angle))
        filtered_d_x_y_a = filter(lambda x: x[0] > min_distance, d_x_y_a)
        d, x, y, a = zip(*filtered_d_x_y_a)
        return d, x, y, a 

    def gradient(self):
        return np.gradient(self.distance)

    def jump_cluster(self, d, max_distance=200):
        cluster_index = 1
        cluster_list = np.full(len(d),0)
        for i in range(len(d)):
            cluster_list[i] = cluster_index
            if i+1 != len(d):
                if abs(d[i+1] - d[i]) > max_distance: cluster_index += 1
            else:
                if abs(d[i] - d[0]) < max_distance:
                    print(cluster_list)
                    cluster_list[cluster_list == cluster_index] = 1
                    print(cluster_list)
        return cluster_list

    def plot(self, pause=.01,cluster=True):
        try:
            d, x, y, a = self.get_x_y()
            if cluster:
                cluster = self.jump_cluster(d)
                self.scatter = plt.scatter(x,y, c=cluster, cmap='prism') 
            else:
                self.scatter = plt.scatter(x, y, color='blue')
        except:
            print("dropped data")
        plt.pause(pause)
        self.scatter.remove()

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
            ldr.plot(cluster=False)
            if record: frames.append([ldr.points_x.copy(),ldr.points_y.copy()])
            i += 1

    if record:      
        import pickle as pkl 
        pkl.dump(frames,open("data/recorded_lidar.pkl",'wb'))

