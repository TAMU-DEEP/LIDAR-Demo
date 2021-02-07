import serial
import time
import termios
import tty, sys
from pynput import keyboard


# # Serial port parameters
#serial_speed = 9600
serial_speed = 115200
serial_port = '/dev/tty.HC-06-DevB'

uPressed = False
dPressed = False
lPressed = False
rPressed = False

def on_press(key):
    #if key == keyboard.Key.up:
    if key == keyboard.Key.esc:
        return False
    '''     
    if keyboard.Key.up:
        print( "forward")
        ser.write(b'w')
    
    if keyboard.Key.down:
        print( "bkf")
        ser.write(b'd')
    if keyboard.Key.left:
        print( "down")
        ser.write(b'a')
    if keyboard.Key.right:
        print( "down")
        ser.write(b'q')
    '''

    if hasattr(key, "char"):
        
        if key.char == '8':
            print( "forward")
            ser.write(b'w')
            #print( ser.readline())
        if key.char == '6':
            print( "bkf")
            ser.write(b'd')
        if key.char == '4':
            print( "down")
            ser.write(b'a')
        if key.char == '2':
            print( "down")
            ser.write(b's')
        if key.char == 'q':
            print( "down")
            ser.write(b'q')
        if key.char == '5':
            print( "light")
            ser.write(b'3')
        
        
        #ser.write(bkey.char)   

def on_release(key):
    #if key == keyboard.Key.up:
    if hasattr(key, "char"):

        ser.write(b'e')
        '''if key.char == 'f':

            print( "up")
        ''' 
        #ser.write(b's')
        





if __name__ == '__main__':
    print( "conecting to serial port ...")
    ser = serial.Serial(serial_port, serial_speed, timeout=5)

    print( "sending message to turn on PIN 13 ...")
    time.sleep(1)
    #ser.write(b'q')
    ser.write(b'e')
    print( "sending message to turn on PIN 13 ...")
    ser.write(b'q')

    #data = ser.readline()
    #if (data != ""):
    #    print( "arduino says: %s" % data)

    #fd = sys.stdin.fileno()
    #old = termios.tcgetattr(fd)
    #old[3] = old[3] | termios.ECHO
    #tty.setraw(sys.stdin.fileno())
    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

        '''
        data = ser.readline()
        if (data != ""):
            print( "arduino says: %s" % data)
        '''
#termios.tcsetattr(fd, termios.TCSADRAIN, old)
#    #time.sleep(10)
#
#    fd = sys.stdin.fileno()
#    old = termios.tcgetattr(fd)
#    old[3] = old[3] | termios.ECHO
#    tty.setraw(sys.stdin.fileno())
#    # Collect events until released
#    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#        listener.join()
#
#    #while 1:
#    #    ch = sys.stdin.read(1)
#    #    #if ch == 'f':
    #
    #    while sys.stdin.read(1) =='f': 
    #        ser.write(b'f')
    #    ser.write(b's')

    #    if ch == 's':
    #        ser.write(b's')

    #    if ch == '':
    #        ser.write(b's')
    #    if ch == 'b':
    #        break

    #    print( "test")
    #    #time.sleep(.11)
    #    #ser.write(b's')



    #termios.tcsetattr(fd, termios.TCSADRAIN, old)
    #termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


'''

    print( "recieving message from arduino ...")
    data = ser.readline()

    if (data != ""):
        print( "arduino says: %s" % data)
    else:
        print( "arduino doesnt respond")

    ser.write(b'f')
    time.sleep(10)

    print( "recieving message from arduino ...")
    data = ser.readline()

    if (data != ""):
        print( "arduino says: %s" % data)
    else:
        print( "arduino doesnt respond")
        
    ser.write(b's')
    print( "recieving message from arduino ...")
    data = ser.readline()

    if (data != ""):
        print( "arduino says: %s" % data)
    else:
        print( "arduino doesnt respond")

    time.sleep(4)
    print( "finish program and close connection!")
'''
