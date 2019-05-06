import serial #imports pyserial library

#sends a new drink request
def sendDrink(instructions, port):
    send = serial.Serial(port, 9600)
    send.write('N'.encode())
    for pump in instructions:
        send.write(str(pump).encode())
