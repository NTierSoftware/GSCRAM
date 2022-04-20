import select, socket, time
from Utilities.CfgParse import KvpReader
from datetime import datetime
from threading import Thread
from Utilities.console import console

from Server.connections import connections
from Utilities.Exceptions import selectErrs, threadedSocketNoTelemetryYet

class threadedSimSocket(Thread):
    TCP = 'TCP'
    UDP = 'UDP'
    bufSize:int = 80
    timeout:int = 1.5 #seconds
    numTimeouts = numConsecutiveTimeouts = maxConsecutiveTimeouts = 0
    maxTimeouts:int = 5

    def __init__(self):
        self.Log:console = console.getConsole(console.TELEMETRY)

        configr = KvpReader()
        deployment  = configr.getvalue(key_name="Deployment")
        TCPorUDP = configr.getvalue(key_name="TCPorUDP", section_name=deployment)
        Thread.__init__(self)
        self.target = DJITargetUDP() if TCPorUDP == threadedSimSocket.UDP else DJITargetTCP()
        self.inputs = [self.target.sock]
        self.buffer:str = ''


    def run(self):
        while self.inputs : #https://pymotw.com/3/select/index.html
            # Wait for at least one of the sockets to be ready for processing
            readable, writable, errs = select.select(self.inputs, [], self.inputs, threadedSimSocket.timeout)
            for s in readable:
                self.buffer+= self.target.get(s) #can receive from either UDP or TCP!
                # print("\nthreadedSimSocket run(): read:", self.buffer, '\n',end='', flush=True)

            for s in errs:
                print("\ns in errs", s.getpeername)
                self.inputs.remove(s) #Stop listening for input on the connection
                raise selectErrs(s.getpeername)

            if not (readable or errs):  # if not (readable or writable or errs):
                self.Log.log("threadedSimSocket run(): not (readable or errs)")
                # todo ? print("\nthreadedSimSocket run(): not (readable or errs)!")
                threadedSimSocket.numTimeouts+= 1
                threadedSimSocket.numConsecutiveTimeouts+= 1

                if threadedSimSocket.numConsecutiveTimeouts > threadedSimSocket.maxConsecutiveTimeouts:
                    threadedSimSocket.maxConsecutiveTimeouts = threadedSimSocket.numConsecutiveTimeouts
                    if threadedSimSocket.maxConsecutiveTimeouts > threadedSimSocket.maxTimeouts:
                        print('\n', datetime.utcnow(), 'threadedSimSocket timed out: numTimeouts:', threadedSimSocket.numTimeouts, '\tmaxConsecutiveTimeouts:', threadedSimSocket.maxConsecutiveTimeouts, end='', flush=True)
                        # raise threadedSocketTimeout()

                continue

            threadedSimSocket.numConsecutiveTimeouts = 0
        print("\nthreadedSimSocket run(): END!")

    def stop(self):
        print('\n', datetime.utcnow(), "threadedSimSocket stopping")
        self.inputs.clear() #termination condition for run(self)
        self.join()
        self.target.sock.shutdown(socket.SHUT_RDWR)
        self.target.sock.close()

    # sample output from drone simulator:
    # $don Target123|version:01|fakeMacAddress;
    # $pos 1541358707796|37.69425829413214|-122.02269567519862|40.0|0.0|0.0|-67.5;\n
    # format:  $pos epoch in millis | lat | lon | elev | pitch | yaw | roll

    #good Telemetry is when '$pos ' is followed by a semicolon (see above example)
    def goodTelemetry(self)->bool: #todo use regular expressions
        firstDelimiter = self.buffer.find('$pos ')
        return (firstDelimiter  >= 0) and self.buffer.find(';', firstDelimiter )

    numNoTelemetries:int = 0
    maxNoTelemetries:int = 6
    def getMostRecentTelemetry(self) -> str:
        while not self.goodTelemetry():
            threadedSimSocket.numNoTelemetries += 1
            if threadedSimSocket.numNoTelemetries > threadedSimSocket.maxNoTelemetries:
                threadedSimSocket.numNoTelemetries = 0
                self.Log.log("err threadedSocket.NoTelemetryYet")
                return '' #todo raise threadedSocketNoTelemetryYet
            time.sleep(threadedSimSocket.timeout)
            continue
        retVal = self.buffer[-threadedSimSocket.bufSize:]  # pull off the last part and let the caller parse.
        self.buffer = ''
        return retVal




class DJITargetTCP():
    def __init__(self):
        print('\nthreadedSimSocket DJITargetTCP()')
        self.sock = connections.DJISimulatorToGSCRAM(FIRSTCONNECT=True) #receives telemetry from DJI drone simulator self reporting target
        # self.testConn()

    def get(self, sock:socket) ->str: return sock.recv(threadedSimSocket.bufSize).decode()

    def testConn(self):
        while True:
            print("\nDJITargetTCP.get()",  self.get(self.sock ))
            time.sleep(.1)


class DJITargetUDP():
    def __init__(self):
        print('\nthreadedSimSocket DJITargetUDP()')
        self.sock = connections.DJISimulatorToGSCRAMudp(FIRSTCONNECT=True) #receives telemetry from DJI drone simulator

    @staticmethod
    def get(sock:socket) ->str:
        telemetry, address = sock.recvfrom(threadedSimSocket.bufSize)
        return telemetry.decode()



if __name__ == '__main__':
    import time
    # MyDroneSim = threadedSimSocket(TCPorUDP=threadedSimSocket.UDP)
    MyDroneSim = threadedSimSocket()
    MyDroneSim.start()
    i:int = 0
    for i in range(0, 2100):
        i+= 1
        try:
            print('\n', i, ': ' , MyDroneSim.getMostRecentTelemetry(),  end='', flush=True)
            time.sleep(.1)
        except threadedSocketNoTelemetryYet: continue

    MyDroneSim.stop()