import serial #imports pyserial library
import time

#sends a new drink request
def sendDrink(instructions, exitKey='exit'):
    exit = False
    try:
        arduino = serial.Serial('COM3', 9600) #initialises serial port
        time.sleep(2) #waits for arduino boot, can possibly be shorter
        pumpString = ""

        for pump in instructions:
            if pump < 10:
                pumpString += '0' + str(pump) #makes all digits 2 digits
            else:
                pumpString += str(pump) #combines pumps to send
        arduino.write(str(pumpString).encode())

        while exit != True:
            command = arduino.readline()
            if command == exitKey:
                exit = True
            time.sleep(0.1)
        return True
    except FileNotFoundError:
        print("Serial port not found, may need to manually change com port")
        return False
    except serial.SerialException:
        print("Serial port not found")
        return False
