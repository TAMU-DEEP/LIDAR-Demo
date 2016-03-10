import serial
import matplotlib.pyplot as plt
import numpy as np
import math
import time


#for windows machines only
import serial.tools.list_ports as ports
coms = ports.comports()
p = coms.next()
if "Arduino" in p[1]:
    com_port = p[0]
else:
    com_port = "COM3" # example: 5 == "COM6" == "/dev/tty5"

print com_port

baudrate = 115200
ser = serial.Serial(com_port, baudrate)

pi = math.pi

#Array of points that will be plotted out
points_x = [0]*360
points_y = [0]*360

#Initialize plot
#plt.ion()
#plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([-2500, 2500])
ax.set_ylim([-2500, 2500])
li, = ax.plot(points_x, points_y, '.')
fig.canvas.draw()
plt.show(block=False)

def graph():
    #ax.clear()
    #ax.set_xlim([-100, 100])
    #ax.set_ylim([-100, 100])
    #ax.scatter(points_x, points_y)
    #plot.draw()
    #plot.pause(.0001)
    li.set_xdata(points_x)
    li.set_ydata(points_y)
    fig.canvas.draw()
    time.sleep(0.01)
    #print "Graph update"
    

c_vals = [math.cos(i * pi/ 180.0) for i in range(360)]
s_vals = [-1 * math.sin(i * pi/ 180.0) for i in range(360)]

def update_view( angle, data ):
    """Updates the view of a sample.

Takes the angle (an int, from 0 to 359) and the list of four bytes of data in the order they arrived.
"""
    global c_vals, s_vals, points_x, points_y, pi
    #unpack data using the denomination used during the discussions
    x = data[0] #distance
    x1= data[1] #distance mask
    x2= data[2] #distance quality
    x3= data[3] #distance quality mask

    #c = s_vals[angle]
    #s = c_vals[angle]

    #angle_rad = angle * pi / 180.0
    #c = math.cos(angle_rad)
    #s = -math.sin(angle_rad)

    c = c_vals[angle]
    s = s_vals[angle]
    dist_mm = x | (( x1 & 0x3f) << 8) # distance is coded on 13 bits ? 14 bits ?
    quality = x2 | (x3 << 8) # quality is on 16 bits
    
    dist_x = dist_mm*c
    dist_y = dist_mm*s

    
    #the flag for "bad data" was always set
    #points_x[angle] = dist_x
    #points_y[angle] = dist_y
    
    if x1 & 0x80: # is the flag for "bad data" set?
        0
        #print "Bad data"
        # yes it's bad data, set points to origin
        #points_x[angle] = 0
        #points_y[angle] = 0
    else:
        #print "angle: %i\tdist_mm: %i\ndist_x: %i\tdist_y: %i\n" %(angle, dist_mm, dist_x, dist_y)
        #show where the points are
        points_x[angle] = dist_x
        points_y[angle] = dist_y

    
init_level = 0
index = 0
def get_data():
    global init_level, index
    n = 0
    update_every = 100
    while True:
        #time.sleep(.000001)
        if init_level == 0 :
            b = ord(ser.read(1))
            # start byte
            if b == 0xFA :
                init_level = 1
            else:
                init_level = 0
        elif init_level == 1:
            # position index
            b = ord(ser.read(1))
            if b >= 0xA0 and b <= 0xF9 :
                index = b - 0xA0
                init_level = 2
            elif b != 0xFA:
                init_level = 0
        elif init_level == 2 :
            # speed
            b_speed = [ ord(b) for b in ser.read(2)]

            # data
            b_data0 = [ ord(b) for b in ser.read(4)]
            b_data1 = [ ord(b) for b in ser.read(4)]
            b_data2 = [ ord(b) for b in ser.read(4)]
            b_data3 = [ ord(b) for b in ser.read(4)]

            update_view(index * 4 + 0, b_data0)
            update_view(index * 4 + 1, b_data1)
            update_view(index * 4 + 2, b_data2)
            update_view(index * 4 + 3, b_data3)
            n = n+1
            if n%update_every == 0: graph() #graph it
            init_level = 0  #reset to accept new data
  

        

get_data()
