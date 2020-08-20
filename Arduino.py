import serial #imports pyserial library

#sends a new drink request
def sendDrink(instructions):
    try:
        send = serial.Serial() #initialises serial port
        send.baudrate = 9600
        send.port = 'COM3' #sets aurduino com port
        send.write('N'.encode())
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
