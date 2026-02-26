import serial #imports pyserial library
import time
import Data

#sends a new drink request
def sendDrink(instructions, exitKey=b'exit\r\n', blockSize=10):
    exit = False
    try:
        arduino = serial.Serial(Data.PumpControllerPort, 9600) #initialises serial port
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
                print("An error occurred reading the card")
            if command == exitKey:
                exit = True
        return True
    except FileNotFoundError:
        print("Serial port not found, may need to manually change com port")
        return False
    except serial.SerialException:
        print("Serial port not found")
        return False

def getID():
    print("getId() Called")
    exit = False
    try:
        arduino = serial.Serial(Data.ScannerPort, 115200) #initialises serial port
        time.sleep(2) #waits for arduino boot, can possibly be shorter
        ID = arduino.readline().decode('ascii')

        # Filter out all non-numeric characters from the ID
        id_filtered = ''.join(ch for ch in ID if ch.isdigit())

        print("getId() finished")
        return id_filtered
    except FileNotFoundError:
        print("Serial port not found, may need to manually change com port")
        print("getId() finished (error)")
        return ""
    except serial.SerialException:
        print("Serial port not found")
        print("getId() finished (error)")
        return ""
