import serial #imports pyserial library
import time

#sends a new drink request
def sendDrink(instructions):
    try:
        send = serial.Serial('COM3', 9600) #initialises serial port
        time.sleep(2) #waits for arduino boot, can possibly be shorter
        pumpString = ""
        for pump in instructions:
            if pump < 10:
                pumpString += '0' + str(pump) #makes all digits 2 digits
            else:
                pumpString += str(pump) #combines pumps to send
        send.write(str(pumpString).encode())
    except FileNotFoundError:
        print("Serial port not found, may need to manually change com port")
    except serial.SerialException:
        print("Serial port not found")
