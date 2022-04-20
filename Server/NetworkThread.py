# https://pymotw.com/3/select/index.html
# https://steelkiwi.com/blog/working-tcp-sockets/
# https://docs.python.org/3.7/howto/sockets.html#non-blocking-sockets
# https://stackoverflow.com/questions/3647539/socket-error-errno-ewouldblock
# https://medium.com/vaidikkapoor/understanding-non-blocking-i-o-with-python-part-1-ec31a2e2db9b
# https://www.quora.com/Network-Programming/Network-Programming-How-is-select-implemented
# https://stackoverflow.com/questions/5160980/use-select-to-listen-on-both-tcp-and-udp-message

import select, socket, time
from datetime import datetime
from threading import Thread
from typing import List, Dict

from Utilities.Exceptions import NetworkThreadRegistryNotConnected
from Server.baseGSCRAMsocket import baseGSCRAMsocket
# from CRAMmsg.rt702Spoof import rt702Spoof
# from Utilities.TimeUtils import millisSinceMidnight
# from CRAMmsg.rt702Spoof import rt702Spoof, rt915Consts

class NetworkThread(Thread):
    __instance: 'NetworkThread' = None

    LastGSmsgRecd:datetime = None

    # spoof:bytearray = None


    @staticmethod
    def getInstance(): # https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm
        if NetworkThread.__instance is None:
            NetworkThread()
            NetworkThread.__instance.start()
        return NetworkThread.__instance

    def __init__(self) : # Virtually private constructor.
        if NetworkThread.__instance is not None: raise Exception("NetworkThread class is a singleton! Use NetworkThread.getInstance().")
        Thread.__init__(self)

        self.isRunning:bool = False
        self.backoff = backoff()
        self.badConnectionCount:int = 0

        # https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html
        # https://www.jetbrains.com/help/pycharm/type-hinting-in-product.html
        self.inputs:List[socket.socket] = []   # List of Sockets from which we read
        self.outputs:List[socket.socket] = []  # List of Sockets to which we write
        self.registry: Dict[socket.socket, baseGSCRAMsocket] = {}    # Dictionary of baseGSCRAMsockets

        NetworkThread.__instance:NetworkThread = self

        # spooftime = millisSinceMidnight()
        # NetworkThread.spoof = rt702Spoof(rt915Consts.msgType.RESPONSE.value, 1, spooftime, spooftime,
        #                   responseTime=spooftime).getByteArray()

    def register(self, aBasesocket: baseGSCRAMsocket):
        if not aBasesocket.connected: raise NetworkThreadRegistryNotConnected()
        aBasesocket.sock.setblocking(False)
        self.registry[aBasesocket.sock] = aBasesocket
        self.outputs.append(aBasesocket.sock)
        self.inputs.append(aBasesocket.sock)
        print(aBasesocket.name, 'registered')

    def handleBadSockets(self, badSocket:socket, badSocketsLists:List[List[socket.socket]]=[]):
        for badList in badSocketsLists:
            if badSocket in badList: badList.remove(badSocket)
        self.registry[badSocket].connected = False
        self.badConnectionCount += 1

    def checkConnections(self):
        for sock in tuple(self.registry):  # https://stackoverflow.com/questions/11941817/how-to-avoid-runtimeerror-dictionary-changed-size-during-iteration-error
            baseSock = self.registry[sock]
            if not baseSock.connected: #always attempt reconnection
                try:
                    self.inputs.remove(sock)
                    self.outputs.remove(sock)
                except ValueError: pass  # the socket has been previously removed. Continue to attempt reconnection.

                NewbaseSock = baseSock.restart() #always attempt reconnection
                if NewbaseSock.connected:
                    del self.registry[sock]
                    self.registry[NewbaseSock.sock] = NewbaseSock
                    self.outputs.append(NewbaseSock.sock)
                    self.inputs.append(NewbaseSock.sock)
                    # NewbaseSock.Qinbound.put(NetworkThread.spoof)
                    self.badConnectionCount -= 1
                    # NewbaseSock.debug('\ncheckConnections')

    def run(self):  # Runs a continuous while loop on a separate thread until the event is triggered to stop.
        noSockets:int = 0
        self.isRunning = True
        while self.isRunning:
            # print('inputs', len(self.inputs))

            if self.inputs:
                readable, writable, errs = select.select(self.inputs, self.outputs, self.inputs) # Wait for at least one of the sockets to be ready for processing

                # print('readable, writable, errs', len(readable), len(writable), len(errs))
                for s in readable: # Handle inputs
                    try: self.registry[s].receivefrom()
                    except (socket.error, ConnectionAbortedError, ConnectionResetError) as err:
                        print("\n" + str(datetime.utcnow()) + ":NetworkThread.run.readable err:", err, end='', flush=True)
                        self.handleBadSockets(s, [writable, errs])


                for s in writable:# Handle outputs
                    try: self.registry[s].sendto()
                    except (socket.error, ConnectionAbortedError, ConnectionResetError) as err:
                        print("\n" + str(datetime.utcnow()) + ":NetworkThread.run.writable err:", err, end='', flush=True)
                        self.handleBadSockets(s, [errs])


                for s in errs:
                    print("\n" + str(datetime.utcnow()) + ":NetworkThread.run.errs:", err, end='', flush=True)
                    self.handleBadSockets(s)

                noSockets = 0
            else:
                if noSockets % 10 == 0: print(noSockets, 'No sockets to select.')
                noSockets += 1
                self.backoff.sleep()

            if self.badConnectionCount > 0: self.checkConnections()

        print('\nNetwork Thread stopped.')
        return #end of thread.

    def stop(self):
        self.isRunning = False
        print('\n' + str(datetime.utcnow()) + " NetworkThread stopping..")
        self.join()
        self.inputs.clear()  # termination condition for run(self); do this FIRST
        self.outputs.clear()
        self.registry.clear()



class backoff:
    def __init__(self):
        self.counter = 0
        self.max = 15
        self.scale = .2

    def sleep(self) -> float:
        if self.counter > self.max: self.counter = 0
        self.counter += 1
        retVal:float = self.counter * self.scale
        time.sleep(retVal )
        return ( retVal )



if __name__ == '__main__':

    MyDroneSim = NetworkThread()
    MyDroneSim.start()
    i: int = 0
    for i in range(0, 2100):
        i += 1
        try:
            # print('\n', i, ': ' , MyDroneSim.getMostRecentTelemetry(), end='', flush=True)
            time.sleep(.1)
        except Exception: continue

    MyDroneSim.stop()
