# Pulse.py
# author: Alex Erf, Airspace, alex.erf@airspace.co, 8/3/2018
# https://stackoverflow.com/a/12435256

from threading import Event, Thread
from typing import Callable

from Server.baseGSCRAMsocket import GSCRAMtofromCRAM
from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from Utilities.TimeUtils import millisSinceMidnight

class Pulse: #Pulse defines a socket connection that sends data at a specified rate.
    def __init__(self, msg: CRAMBaseMessage, pulseRate: float):
        """Initializes the socket, message element, pulse rate, and stop flag (to stop the thread)."""
        self.msg = msg
        self.stopFlag = Event()
        self.totalPulses = 0
        self.isPaused = False
        self.isStopped = False
        self.thread = PulseHelper(self.stopFlag, pulseRate, self.msg, self.incrementPulseCounter, self.lostConnection)


    def start(self):
        if self.isStopped: raise PulseDeadError('Start', 'Cannot start a stopped Pulse.')
        self.stopFlag = Event()
        self.thread.start()
        self.isPaused = False
        return self

    def stop(self):
        # print("Pulse stopping")
        self.thread.connectionValid = False
        self.stopFlag.set()

        self.thread.join()
        self.isStopped = True
        print("pulse stopped!")

    def pause(self):
        if self.isStopped: raise PulseDeadError('Pause', 'Cannot pause a stopped Pulse.')
        if not self.isPaused:
            self.stopFlag.set()
            self.thread.join()
            self.isPaused = True
    
    def resume(self):#Resumes operation by creating a new thread instance.
        if self.isStopped: raise PulseDeadError('Resume', 'Cannot resume a stopped Pulse.')
        if self.isPaused: self.start()

    def getNumPulses(self) -> int: return self.totalPulses

    def incrementPulseCounter(self):
        self.totalPulses += 1

    def lostConnection(self): self.isStopped = True


# from Server.NetworkThread import NetworkThread
class PulseHelper(Thread): #Defines the thread operation used by Pulse.
    def __init__(self, event: Event, pulseRate: float, msg: CRAMBaseMessage, incPulse: Callable, dropConn: Callable):
        Thread.__init__(self)
        self.stopped = event
        self.pulseRate = pulseRate
        self.msg = msg
        # self.conv = conv
        # self.CRAM = GSCRAMtofromCRAM.getInstance()

        # self.networkThread = NetworkThread.getInstance()
        self.incPulse = incPulse
        self.dropConn = dropConn
        self.connectionValid = True

    def run(self): #Runs a continuous while loop on a separate thread until the event is triggered to stop.
        self.connectionValid = True
        # while not self.stopped.wait(self.pulseRate) and self.connectionValid:
        while self.connectionValid and not self.stopped.wait(self.pulseRate) :
            try:
                self.msg.header.transmitTime.data = millisSinceMidnight()
                # print(self.msg.toJSON())
                # self.CRAM.sendCRAMmsg(self.msg)
                GSCRAMtofromCRAM.getInstance().sendCRAMmsg(self.msg)
            except ConnectionAbortedError as err:
                self.connectionValid = False
                self.dropConn()
                print('\nPulseHelper run err', 'Attempted to send data over a dead socket.', err)
            self.incPulse()


class PulseDeadError(Exception):
    def __init__(self, operation: str, message: str):
        self.operation = operation
        self.message = message
        return

