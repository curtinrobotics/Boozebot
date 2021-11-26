import serial
import time
import multiprocessing

class CashAcceptorProcess(multiprocessing.Process):
    """
    Worker process for communication with the cash acceptor
    """
    def __init__(self):
        multiprocessing.Process.__init__(self)

        # TODO: Port over cash acceptor codeta)