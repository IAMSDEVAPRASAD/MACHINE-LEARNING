#! /usr/bin/env python3

import drivers
import time
import serial
import pickle

display = drivers.Lcd()
ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)  #PC

### loading the model
model_loaded_linear_regression = pickle.load(open("/home/pi_4/Desktop/ML_assignment_3/Assignment 3/models/tf_luna_linear","rb"))


try:
    while True:

        ser.write(0x42)
        ser.write(0x57) 
        ser.write(0x02) 
        ser.write(0x00) 
        ser.write(0x00) 
        ser.write(0x00) 
        ser.write(0x01) 
        ser.write(0x06)

        recv = ser.read(9)
        ser.reset_input_buffer()
        display.lcd_clear() 

        if 89 == recv[0] and 89 == recv[1] :

            distance = recv[2]
            distance = model_loaded_linear_regression.predict([[distance]])
            distance = distance[0][0]
            display.lcd_display_string("Distance : "+str(distance), 1)
            print(distance)  

        else:
            display.lcd_display_string("No input", 1)

        time.sleep(0.5)


except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
