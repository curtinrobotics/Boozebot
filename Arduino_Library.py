import time
from Arduino import Arduino  # type: ignore

async def sendDrink(instructions, exitKey='exit', blockSize=10):
    try:
        board = Arduino("9600", port="COM3")
        pumpString = ""
        for pump in instructions:
            if pump < blockSize:
                pumpString += '0' + str(pump) 
            else:
                pumpString += str(pump) 
        
        board.SoftwareSerial.write(pumpString)
        
        exit = False
        while not exit:
            try:
                command = board.SoftwareSerial.read()
                print(command)
                if command == exitKey:
                    exit = True
            except Exception as e:
                print(f"Error: {e}")
        
        board.close()
        return True
        
    except FileNotFoundError:
        print("Serial port not found, may need to manually change com port")
        return False
    except Exception as e:
        print(f"Connection error: {e}")
        return False
    