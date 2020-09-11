import threading
import time
import Arduino
from Queue import Queue

class ArduinoThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.daemon = True
        self.drinkCount = 0

    def run(self):
        print(threading.currentThread().getName() + "starting")
        while True:
            drink = self.queue.get()
            self.ServeDrink(drink)

    def ServeDrink(self, drink):
        success = False
        while success != True:
            success = Arduino.sendDrink(drink)
        print("Order " + str(drinkCount) + " is finished.")
        self.drinkCount += 1
