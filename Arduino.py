import serial #imports pyserial library
import time

#sends a new drink request
def sendDrink(instructions, exitKey=b'exit\r\n', blockSize=10):
    exit = False
    try:
        arduino = serial.Serial('COM3', 9600) #initialises serial port
        time.sleep(2) #waits for arduino boot, can possibly be shorter
        arduino.flushInput()

        pumpString = ""

        for pump in instructions:
            if pump < blockSize:
                pumpString += '0' + str(pump) #makes all digits 2 digits
            else:
                pumpString += str(pump) #combines pumps to send
        arduino.write(str(pumpString).encode())

        arduino.flushInput()
        while exit != True:
            try:
                command = arduino.readline()
                print(command)
            except:
                print("Keyboard Interrupt")
            if command == exitKey:
                exit = True
        return True
    except FileNotFoundError:
        print("Serial port not found, may need to manually change com port")
        return False
    except serial.SerialException:
        print("Serial port not found")
        return False
