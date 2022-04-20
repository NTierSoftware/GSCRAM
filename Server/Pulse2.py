# Pulse2.py  todo REFACTOR use of Pulse.py to Pulse2.py!
# https://stackoverflow.com/a/12435256

from threading import Event, Thread
from typing import Callable

from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from Utilities.TimeUtils import millisSinceMidnight
from Utilities.console import console

class Pulse(): #Pulse defines a socket connection that sends data at a specified rate.
    def __init__(self):
        self.stopFlag = Event()
        self.totalPulses = 0
        self.isPaused = False
        self.isStopped = False
        self.thread: Thread = None


    def setThread(self, thread:Thread):
        self.thread = thread
    
    def start(self):
        if self.isStopped: raise PulseDeadError('Start', 'Cannot start a stopped Pulse.')
        self.stopFlag = Event()
        if self.thread is None: raise PulseDeadError('Start', 'Pulse thread must be set with Pulse.setThread()')
        self.thread.start()
        self.isPaused = False
        return self

    def stop(self):
        print("stopping")
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
    
    def resume(self):
        """Resumes operation by creating a new thread instance."""
        if self.isStopped: raise PulseDeadError('Resume', 'Cannot resume a stopped Pulse.')
        if self.isPaused: self.start()

    def getNumPulses(self) -> int: return self.totalPulses

    def incrementPulseCounter(self):
        self.totalPulses += 1

    def lostConnection(self): self.isStopped = True


class PulseDeadError(Exception):
    def __init__(self, operation: str, message: str):
        self.operation = operation
        self.message = message
        return

#
# class PulseHelper(Thread):
#     """Defines the thread operation used by Pulse."""
#     def __init__(self, event: Event, pulseRate: float, msg: CRAMBaseMessage, conv: 'Conversation', incPulse: Callable, dropConn: Callable):
#         Thread.__init__(self)
#         self.stopped = event
#         self.pulseRate = pulseRate
#         self.msg = msg
#         self.conv = conv
#         self.incPulse = incPulse
#         self.dropConn = dropConn
#         self.connectionValid = True
#
#     def run(self):
#         """Runs a continuous while loop on a separate thread until the event is triggered to stop."""
#         self.connectionValid = True
#         while not self.stopped.wait(self.pulseRate) and self.connectionValid:
#             try:
#                 self.msg.header.transmitTime.data = millisSinceMidnight()
#                 self.conv.sendMsg(self.msg)
#             except ConnectionAbortedError as err:
#                 self.connectionValid = False
#                 self.dropConn()
#                 print('\nPulseHelper run err', 'Attempted to send data over a dead socket.', err)
#                 from Server.GSCRAM import GSCRAM
#                 GSCRAM.stop()
#
#             self.incPulse()
#
# class PulseHelperTest(PulseHelper):
#     def run(self):
#         """Runs a continuous while loop on a separate thread until the event is triggered to stop."""
#         self.connectionValid = True
#         while not self.stopped.wait(self.pulseRate) and self.connectionValid:
#             try:
#                 print("running PulseHelperTest ")
#             except ConnectionAbortedError as err:
#                 self.connectionValid = False
#                 self.dropConn()
#                 print('\nPulseHelper run err', 'Attempted to send data over a dead socket.', err)
#                 from Server.GSCRAM import GSCRAM
#                 GSCRAM.stop()
#
#             self.incPulse()
#
# class PulseLog(Pulse):
#     HEART = '♥'
#     METEOROLOGICAL = '☀'
#     INTERCEPTOR = '✈'
#
#     pulseConsole = None
#     pulseDisplayRate: int = 5
#     registry = []
#
#     def __init__(self, conv: 'Conversation', msg: CRAMBaseMessage, pulseRate: float, emoji: str, color=console.GREEN):
#         super().__init__(conv, msg, pulseRate)
#         self.emoji = emoji
#         self.thread.incPulse = self.incrementPulseCounter
#         self.color = color
#         if PulseLog.pulseConsole is None: PulseLog.pulseConsole = console(self.color, title="GSCRAM Pulse log")
#         PulseLog.registry.append(self)
#
#     def incrementPulseCounter(self):
#         super().incrementPulseCounter()
#
#         if ( self.totalPulses % PulseLog.pulseDisplayRate == 0):  # only print out every pulseDisplayRate emoji.
#             newLine = "\n" if (self.totalPulses  % 10 == 0) else ""
#             pulseStr = newLine + self.emoji + str(self.totalPulses ) + "  "
#             PulseLog.pulseConsole.log(pulseStr)
#
#     def stop(self):
#         super().stop()
#         if PulseLog.pulseConsole is not None:
#             PulseLog.pulseConsole.terminate()
#             PulseLog.pulseConsole = None
#
#     @staticmethod
#     def stopAll():
#         for pulseLog in PulseLog.registry: pulseLog.stop()
