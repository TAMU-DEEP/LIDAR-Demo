# LIDAR-Demo
Instructions for setting up the LIDAR:

Wiring:

Bluetoth chip connections
	1. VCC-> 3.3 V
	2. GND-> GND
	3. TXD-> RX0
	4. RXD-> (Resistor 1) to GND; (Resistor 2) to TX0

LIDAR connections
	Red-> 5V
	Green-> GND
	Blue-> RX3
	Black-> PWM 4



HARDWARE:

1. Make sure that each of the four bare wires of the cord in the box with the arduino chip
are connected to the correct pins on the board. There should be a piece of tape with a
legend attached to the cord.

2. Connect the plug on the LIDAR system to the one which was in the Arduino chip box.

3. Plug the USB cable into the Arduino port and an available USB plug on your computer.



ARDUINO SOFTWARE: (Skip this section if the board is already programmed - odds are it is)

1. Open up the Arduino interface (must be downloaded from the Arduino website).

2. Open the Arduino file with the correct code in it.  At the time of making this, the
filename is: Arduino_Mega_XV_11_motor_control_v0_2_simple_close_loop_modified.ino

3. Select the arduino board from the Tools>Board menu.  The correct Serial Port should 
automatically be selected.

4. Click "Upload"



PYTHON SOFTWARE:

1. Make sure that you have downloaded Python, VPython, and PySerial to the correct
directories before continuing.

2. Open VIDLE for VPython
