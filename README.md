# LIDAR Car:

lidar_car_ino tested as of Feb 7 2021 to work both with stearing car and lidar seperately.

LIDAR:
1. Blue-> SR3 RXD (15)
2. Red->Red->5V
3. Black->Black->analogWrite(3)
4. Green->Bronw->Ground

Bluetooth:
1. Red->5V
1. Brown->Ground
1. Orange->RXD (Serial 0)
1. Yelllow->TXD (Serial 0)

Elago motor controller:
1. Sheild connector.

# LIDAR vis:

Basic vis working with src/LidarDataReader.

# Car controll:
Need to write class to steer car. Instructions to be sent as "&[speedleft]:[speedright]&". between -255 and +255.

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
