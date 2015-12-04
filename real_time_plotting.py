#
#	Kyle Shores
#	created: 11/19/2015
#	updated: 12/3/2015
#	
#	This script is a simple set up for plotting data with matplotlib in realtime to show a small proof-of-concept 
#	to be used for the LIDAR demo.
#	At the time of this writing, the program that shows the position of the lidar car to the user has a slow response time
#	when updating the points.
#	We would like to make this minimize this response time.
#	Here, I show how you can plot realtime data on both a 2d and 3d axis, and do so quickly.	
#
#	To use this, make sure python 2.7 is installed along with matplotlib. time and random are shipped with python.
#
#
#	Note: The 2d axes cannot be moved around to my knowledge, but we could plot everything with the 3d axes and by able to rotate the plot.
#	
#	Note: The 3d axes can be rotated. Click on the plot of the 3d axes and drag it around to view it from different angles
#	
#
#	The only bad thing about this script is that you have to manually stop the program by pressing CTRL+Z, or CTRL+C, depending on the system you use.
#	But to avoid this, the program will manually close itself after 10 seconds.
#	To leave it open for longer, edit the variable on line 58.


import matplotlib.pyplot as plot
import random
import time
from mpl_toolkits.mplot3d import Axes3D


def main():

	#make the figure
	fig = plot.figure()
	'''
	An axes is an object in python that manages where data will be plotted inside of a figure.
	The window is the figure. Inside of a window there can be plots.
	Each of these plots are assigned a set of axes that the data is attached to.
	Because I am making two plots inside of one figure, I need to have specify the axes that the data will be plotted on for each subplot.
	'''



	#make the axes to be used for the 3d graph
	ax1 = fig.add_subplot(211, projection = '3d')
	
	#make the axes to be used for the 2d graph
	ax2 = fig.add_subplot(212)

	#enable the ineractive plotting to allow for continual updates, show it once to enable the drawing
	plot.ion()
	plot.show()

	#a variable to keep track of how long the plot has been open to terminate thi program after 10 seconds
	start = time.time()
	#variable to choose how long this runs
	close_after = 10	#in seconds
	while True:
		#check if the program has been running longer than 10 seconds, if so, close the plot and terminate the program
		if (time.time() - start) > close_after:
			plot.close('all')
			break


		#generate random x,y and z points
		x = range(0,21)
		y = [random.randint(i,i+20) for i in x]
		z = range(1,len(y) + 1)

		#clear any old data
		ax1.clear()
		ax2.clear()

		#plot the new data
		ax1.scatter(x,y,z)
		ax2.scatter(x,y)

		#fiz the axes limits
		ax1.set_xlim([0,21])
		ax1.set_ylim([0,41])
		ax1.set_zlim([0,20])

		ax2.set_xlim([0,21])
		ax2.set_ylim([0,41])
		#redraw the plot
		plot.draw()

		#allows the viewer to see the points after they are drawn
		plot.pause(.00001)
main()
