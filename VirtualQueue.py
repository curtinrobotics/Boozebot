import threading
import time
from queue import Queue

import Arduino_Library

class ArduinoThread(threading.Thread):
    drinkCount = 0

    def __init__(self, queue):
        # Initialize the thread TODO: make it a pool rather then self setting
        threading.Thread.__init__(self)
        self.queue = queue
        self.daemon = True
        self.drinkCount = 0

    def run(self):
        print(threading.currentThread().getName() + " starting")
        while True:
            drink = self.queue.get()
            self.ServeDrink(drink)

    def ServeDrink(self, drink):
        success = False
        while success != True:
            success = Arduino_Library.sendDrink(drink)
        print("Order " + str(ArduinoThread.drinkCount) + " is finished.")
        ArduinoThread.drinkCount += 1
        self.drinkCount += 1
