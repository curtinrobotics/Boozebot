import serial
import time
import multiprocessing

from .. import Data


class PumpControllerProcess(multiprocessing.Process):
    """
    Worker process for communication with the pump controller
    """

    def __init__(self, drink_queue, output_queue=None):
        multiprocessing.Process.__init__(self)

        self.drink_queue = drink_queue
        self.output_queue = output_queue

    def close(self):
        self.sp.close()

    def readSerial(self):
        return self.sp.readline().decode('ascii').replace("\n", "").replace("\r", "")

    def send_drink(self, instructions):
        pumpString = ""

        for pump in instructions:
            pumpString += str(pump).zfill(2)  # Prepend leading 0 if necessary

        self.sp.write(pumpString.encode())

    def run(self):
        self.sp = serial.Serial(Data.PumpControllerPort, 115200)

        while True:
            # Check for incoming drink requests
            if not self.drink_queue.isEmpty():
                instructions = self.drink_queue.get()
                self.send_drink(self, instructions)

            data = self.readSerial()
            print("Serial:", data)
            self.output_queue.put(data)
