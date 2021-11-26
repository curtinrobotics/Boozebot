import serial
import time
import multiprocessing

from .. import Data

class CardReaderProcess(multiprocessing.Process):
    """
    Worker process for communication with the student ID card reader
    """

    def __init__(self, output_queue):
        multiprocessing.Process.__init__(self)

        self.output_queue = output_queue

    def close(self):
        self.sp.close()

    def read_id(self):
        id = self.sp.readline().decode('ascii')

        # Filter out all non-numeric characters from the ID
        return ''.join(ch for ch in id if ch.isdigit())

    def run(self):
        self.sp = serial.Serial(Data.ScannerPort, 115200)

        while True:
            id = self.read_id()
            print("Scanned ID:", id)
            self.output_queue.put(id)