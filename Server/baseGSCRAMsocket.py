#https://www.programiz.com/python-programming/methods/built-in/super
# https://docs.python.org/3.7/howto/sockets.html#non-blocking-sockets "you’re supposed to use shutdown on a socket before closing it. shutdown is an advisory to socket at other end."
# https://stackoverflow.com/questions/409783/socket-shutdown-vs-socket-close
# https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm

import queue, socket, time
from typing import Optional
from datetime import datetime, timedelta

from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from GSmsg.GSBaseMessage import GSBaseMessage
# from CRAMmsg.rt702Spoof import rt702Spoof #, rt915Consts
from Utilities import constants
from Utilities.BytesToMessage import getMessageFromBytes
from Utilities.console import console
from Utilities.Exceptions import baseMethodErr, MessageReceiveError
from Utilities.JSONToGSmsg import JSONToGSmsg
from CRAMmsg.r920ThreatState import r920ThreatState
from CRAMmsg.rt915NetTime import rt915NetTime


class baseGSCRAMsocket():
    Registry = []

    def __init__(self):
        self.name: str = type(self).__name__
        self.connected:bool = False
        self.Qinbound:queue.Queue = queue.Queue()
        self.Qoutbound:queue.Queue= queue.Queue()
        self.console = console.getConsole(console.DEBUG)
        # self.name:str = 'baseGSCRAMsocket'
        self.sock:socket.socket = None
        self.emptyREADs:int = 0
        self.register()

    def receivefrom(self):#used in NetworkThread
        try: data = self.sock.recv(1024)
        except (socket.error, ConnectionAbortedError, ConnectionResetError) as err:
            print("\n" + str(datetime.utcnow()) + ": baseGSCRAMsocket.receivefrom() err:", "NoREADs:", self.emptyREADs, self, err, end='\n', flush=True)
            self.emptyREADs = 0
            raise err

        if data: self.Qinbound.put(data) # A readable client socket has data
        else: self.emptyREADs += 1
            # print("baseGSCRAMsocket.receivefrom(): no READ data from:" + str(self.sock.getpeername()))


    def sendto(self):#used in NetworkThread
        try:
            next_msg = self.Qoutbound.get(False)
        except queue.Empty: return
        else:
            self.sock.send(next_msg)



    def register(self):
        baseGSCRAMsocket.Registry.append(self)

    # def debug(self, tag:str=None):
        # print(tag, self.name, '\n\tQinbound', self.Qinbound.qsize(), 'Qoutbound', self.Qoutbound.qsize(), 'connected', self.connected, '\n', end='', flush=True)

    def __repr__(self):
        return self.name + '\tQinbound:' + str(self.Qinbound.qsize()) + '\tQoutbound:' + str(self.Qoutbound.qsize()) + '\tconnected:' + str(self.connected)


    @classmethod
    def shutdownAll(cls):
        for s in cls.Registry: s.shut()
        cls.Registry.clear()
        print("all baseGSCRAMsockets shutdown")


    def restart(self) -> 'baseGSCRAMsocket':
        self.shut()
        retVal = self.getInstance(restart=True)
        if retVal is None: print('restart retVal is NONE!!', retVal, end='', flush=True)
        return retVal

    def shut(self):
        print('shut()', self)
        self.connected = False
        try: self.sock.shutdown(socket.SHUT_RDWR)
        except (OSError, AttributeError): pass
        try: self.sock.close()
        except (OSError, AttributeError): pass

        # https://stackoverflow.com/questions/6517953/clear-all-items-from-the-queue/18873213#18873213
        while not self.Qinbound.empty():
            try:self.Qinbound.get(False)
            except queue.Empty: continue

        while not self.Qoutbound.empty():
            try:self.Qoutbound.get(False)
            except queue.Empty: continue


    @staticmethod
    def getInstance(restart:bool = False): raise baseMethodErr("baseGSCRAMsocket.getInstance()")


from Server.connections import connections

class GSCRAMtofromGS(baseGSCRAMsocket):
    __instance: 'GSCRAMtofromGS' = None

    numRetries:int = 0

    @staticmethod
    def getInstance(restart:bool = False): # https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm
        if restart or GSCRAMtofromGS.__instance is None:
            GSCRAMtofromGS.__instance = None
            GSCRAMtofromGS()
        return GSCRAMtofromGS.__instance


    def __init__(self):
        if GSCRAMtofromGS.__instance is not None: raise Exception("GSCRAMtofromGS class is a singleton! Use GSCRAMtofromGS.getInstance().")
        super().__init__()

        # self.name = 'GS'
        self.name: str = type(self).__name__

        self.sock = connections.clientToGroundspaceSvr()


        if self.sock is not None:
            self.console.log("Groundspace connected: " + str(connections.GSaddress))
            GSCRAMtofromGS.numRetries = 0
            self.connected = True
        else:
            GSCRAMtofromGS.numRetries += 1
            self.console.log(constants.ConnectFail + str(GSCRAMtofromGS.numRetries) + " retry Groundspace server: " + str(connections.GSaddress) )

        GSCRAMtofromGS.__instance = self

    # DELIMITER: bytes = b';'
    def sendGSmsg(self, msg: GSBaseMessage): #used in Main Looper
        self.Qoutbound.put(msg.toJSON().encode('UTF-8') + b';' )
        msg.SentTime = datetime.utcnow()

    # def recvGSmsg(self, timeout:float=constants.GroundspaceSendRate) -> GSBaseMessage: #used in Main Looper.
    def recvGSmsg(self, timeout:float=0) -> Optional[GSBaseMessage]: #used in Main Looper.
        #convert the get() to a string and remove out any 'Ok\r\n'
        # data = self.Qinbound.get(block=True, timeout=timeout).decode().replace(constants.GSOk, '') # this can raise Exception queue.Empty!
        # return JSONToGSmsg(data)
        return JSONToGSmsg(self.Qinbound.get(block=True, timeout=timeout).decode().replace(constants.GSOk, ''))
        # if data: return JSONToGSmsg(data)
        # # if data == '': return self.recvGSmsg() #if all the Ok\r\n were stripped out leaving nothing at all, then receive again.
        # return None


    # Ok: bytes = b'Ok\r\n'
    # def recvGSmsg(self, timeout:float=constants.GroundspaceSendRate) -> GSBaseMessage: #used in Main Looper.
    #     data = self.Qinbound.get(block=True, timeout=timeout) # this can raise Exception queue.Empty!
    #     # self.debug('recvGSmsg:\n\t' + str(data))
    #     # while data == GSCRAMtofromGS.Ok:
    #     while data == constants.GSOkbytes:
    #         data = self.Qinbound.get(block=True, timeout=timeout)
    #         # self.debug('recvGSmsg:\n\t' + str(data))
    #
    #
    #     return JSONToGSmsg(data.decode())



from CRAMmsg.rt902WeaponHeartbeat import rt902Consts, rt902WeaponHeartbeat
from threading import Timer
# https://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


from Utilities.TimeUtils import millisSinceMidnight
# from CRAMmsg.rt702Spoof import rt702Spoof, rt915Consts

import errno, os
class getCRAMmsgEmpty(Exception): pass #used in GSCRAMtofromCRAM.receivefrom()

class GSCRAMtofromCRAM(baseGSCRAMsocket):
    __instance: 'GSCRAMtofromCRAM' = None

    numRetries: int = 0

    weaponId = None
    # spoof:bytearray = None

    heartBeatmsg:rt902WeaponHeartbeat = None

    @staticmethod
    def getInstance(restart:bool = False): # https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm
        if restart or GSCRAMtofromCRAM.__instance is None:
            GSCRAMtofromCRAM.__instance = None
            GSCRAMtofromCRAM()
        return GSCRAMtofromCRAM.__instance


    def __init__(self):
        super().__init__()
        # self.name = 'CRAM'
        self.name: str = type(self).__name__

        self.numBeats:int = 0
        self.timer:RepeatTimer = None

        self.sock = connections.serverToCRAMclient()
        if self.sock is not None:
            self.connected = True
            self.console.log("CRAM connected: " + str(connections.CRAMaddress))
            GSCRAMtofromCRAM.numRetries = 0
            if GSCRAMtofromCRAM.weaponId is not None: self.startHeartBeat(GSCRAMtofromCRAM.weaponId)
        else:
            GSCRAMtofromCRAM.numRetries += 1
            self.console.log(constants.ConnectFail + str(GSCRAMtofromCRAM.numRetries) + " retry CRAM client: " + str(connections.CRAMaddress) )

        self.mostRecentThreat: Optional[r920ThreatState] = None
        GSCRAMtofromCRAM.__instance = self


    def sendHeartBeat(self):
        GSCRAMtofromCRAM.heartBeatmsg.header.transmitTime.data = millisSinceMidnight()
        self.sendCRAMmsg(GSCRAMtofromCRAM.heartBeatmsg)
        # self.debug('sendHeartBeat: ' + GSCRAMtofromCRAM.heartBeatmsg.toJSON() )
        self.numBeats += 1

    def startHeartBeat(self, newWeaponId=None):
        print('starting HeartBeat. weaponId:', newWeaponId)
        if self.timer is not None:
            self.timer.cancel()
            self.timer.join()
            print('heartbeat joined')

        if newWeaponId: GSCRAMtofromCRAM.weaponId = newWeaponId
        if not GSCRAMtofromCRAM.weaponId: raise Exception("startHeartBeat() must have a weaponId ")

        GSCRAMtofromCRAM.heartBeatmsg = rt902WeaponHeartbeat(weaponId=GSCRAMtofromCRAM.weaponId)
        self.timer =  RepeatTimer(rt902Consts.PULSE_RATE, self.sendHeartBeat)
        self.timer.start()

    def restart(self) -> 'baseGSCRAMsocket':
        retVal = super().restart()
        if GSCRAMtofromCRAM.weaponId: self.startHeartBeat(GSCRAMtofromCRAM.weaponId)
        return retVal

    def sendCRAMmsg(self, msg: CRAMBaseMessage):
        self.Qoutbound.put(msg.getByteArray())
        # self.debug('sendCRAMmsg')



    LENGTHBYTES: int = 4

    def receivefrom(self):  # used in NetworkThread
        def getCRAMmsg() -> bytearray:
            try:
                hexLength: bytearray = self.sock.recv(
                    GSCRAMtofromCRAM.LENGTHBYTES)  # get the message length in the message header
                if hexLength:
                    CRAMmsg = self.sock.recv(int(hexLength.hex(), 16) - GSCRAMtofromCRAM.LENGTHBYTES)
                    if CRAMmsg:
                        return hexLength + CRAMmsg
                    else:
                        print('\error GSCRAMtofromCRAM..getCRAMmsg(): no data received with hexlength:',
                              int(hexLength.hex(), 16))
            except OSError as err:
                # EWOULDBLOCK means there is nothing to read: "[WinError 10035] A non-blocking socket operation could not be completed immediately"
                # https://stackoverflow.com/questions/3647539/socket-error-errno-ewouldblock

                if err.errno != errno.EWOULDBLOCK: raise err
            except (socket.error, ConnectionAbortedError, ConnectionResetError) as err:
                print("\n" + str(datetime.utcnow()) + ": GSCRAMtofromCRAM..getCRAMmsg() err:", "NoREADs:",
                      self.emptyREADs, self, err, end='\n', flush=True)
                self.emptyREADs = 0
                raise err

            raise getCRAMmsgEmpty

        CRAMmsg: Optional[CRAMBaseMessage] = None
        beginTime: datetime = datetime.utcnow()
        # consumedThreats: int = 0
        # curThreat:Optional[r920ThreatState] = None
        try:
            CRAMmsg = getMessageFromBytes(getCRAMmsg())
            while isinstance(CRAMmsg, r920ThreatState):  # keep on consuming r920ThreatState
                # http://effbot.org/pyfaq/what-kinds-of-global-value-mutation-are-thread-safe.htm
                if CRAMmsg.CEASEFIRE():
                    self.mostRecentThreat = None
                    break #stop consuming threats and add CRAMmsg CEASEFIRE threat to Qinbound.

                self.mostRecentThreat = CRAMmsg
                CRAMmsg = getMessageFromBytes(getCRAMmsg())

        except getCRAMmsgEmpty: CRAMmsg = None

        if CRAMmsg:
            self.Qinbound.put(CRAMmsg)
            if not isinstance(CRAMmsg, (r920ThreatState, rt902WeaponHeartbeat, rt915NetTime)):
                print('\nreceivefrom', CRAMmsg, '\n\t', self)

    # def receivefrom(self):#used in NetworkThread
    #     def getCRAMmsg() -> bytearray:
    #         try:
    #             hexLength: bytearray = self.sock.recv(GSCRAMtofromCRAM.LENGTHBYTES) #get the message length in the message header
    #             if hexLength:
    #                 CRAMmsg = self.sock.recv( int(hexLength.hex(), 16) - GSCRAMtofromCRAM.LENGTHBYTES )
    #                 if CRAMmsg: return hexLength + CRAMmsg
    #                 else: print('\error GSCRAMtofromCRAM..getCRAMmsg(): no data received with hexlength:', int(hexLength.hex(), 16))
    #         except OSError as err:
    #             # EWOULDBLOCK means there is nothing to read: "[WinError 10035] A non-blocking socket operation could not be completed immediately"
    #             #https://stackoverflow.com/questions/3647539/socket-error-errno-ewouldblock
    #
    #             if err.errno != errno.EWOULDBLOCK: raise err
    #         except (socket.error, ConnectionAbortedError, ConnectionResetError) as err:
    #             print("\n" + str(datetime.utcnow()) + ": GSCRAMtofromCRAM..getCRAMmsg() err:", "NoREADs:", self.emptyREADs, self, err, end='\n', flush=True)
    #             self.emptyREADs = 0
    #             raise err
    #
    #         raise getCRAMmsgEmpty
    #
    #     CRAMmsg:Optional[CRAMBaseMessage] = None
    #     beginTime: datetime = datetime.utcnow()
    #     # consumedThreats: int = 0
    #     # curThreat:Optional[r920ThreatState] = None
    #     try:
    #         CRAMmsg = getMessageFromBytes( getCRAMmsg() )
    #         # if not isinstance(CRAMmsg, (rt902WeaponHeartbeat, rt915NetTime)): print('\nreceivefrom', CRAMmsg)
    #         while ((CRAMmsg.RecvTime - beginTime) < constants.Groundspacetimedelta): #keep on consuming r920ThreatState
    #             if isinstance(CRAMmsg, r920ThreatState):
    #                 if CRAMmsg.isaThreat():
    #                     #this is threadsafe: http://effbot.org/pyfaq/what-kinds-of-global-value-mutation-are-thread-safe.htm
    #                     self.mostRecentThreat = CRAMmsg
    #                     CRAMmsg = None #we're consuming threats so don't put it on the Queue.
    #                     if not self.mostRecentThreat.CEASEFIRE():
    #                         # consumedThreats += 1
    #                         # print('\nconsumedThreats', consumedThreats)
    #                         CRAMmsg = getMessageFromBytes(getCRAMmsg())
    #                             # if not isinstance(CRAMmsg, (rt902WeaponHeartbeat, rt915NetTime)):
    #                             #     print('\nreceivefrom', CRAMmsg)
    #                         continue
    #                 # curThreat = CRAMmsg
    #                 # if not self.mostRecentThreat.CEASEFIRE():
    #                 #     consumedThreats += 1
    #                 #     print('\nconsumedThreats', consumedThreats)
    #                 #     CRAMmsg = getMessageFromBytes( getCRAMmsg())
    #                 #     if not isinstance(CRAMmsg, (rt902WeaponHeartbeat, rt915NetTime)): print('\nreceivefrom',CRAMmsg)
    #                 #     continue
    #             break
    #     except getCRAMmsgEmpty: pass #print('\ngetCRAMmsgEmpty', self)
    #     # except (socket.error, ConnectionAbortedError, ConnectionResetError) as err:
    #     #     print("\n" + str(datetime.utcnow()) + ": GSCRAMtofromCRAM.receivefrom() err:", "NoREADs:", self.emptyREADs, self, err, end='\n', flush=True)
    #     #     self.emptyREADs = 0
    #     #     raise err
    #
    #     # if curThreat:
    #     #     self.Qinbound.put(curThreat)
    #     #     print('\ncurThreat put', curThreat,  '\n\t',self)
    #
    #     if CRAMmsg:
    #         self.Qinbound.put(CRAMmsg)
    #         if not isinstance(CRAMmsg, (r920ThreatState, rt902WeaponHeartbeat, rt915NetTime)):
    #             print('\nreceivefrom', CRAMmsg, '\n\t', self)





    def recvCRAMmsg(self, timeout:float=0) -> CRAMBaseMessage:
        # print('recvCRAMmsg\n\t', self)
        return self.Qinbound.get(block=True, timeout=timeout) #throws queue.Empty

    # def recvCRAMmsg(self, timeout:float=.01) -> CRAMBaseMessage:
    #     data = self.Qinbound.get(block=True, timeout=timeout) #throws queue.Empty
    #     return getMessageFromBytes(data)



    def shut(self):
        self.timer.cancel()
        self.timer.join()
        super().shut()

    def is_alive(self) ->bool:
        if self.timer is None: return False
        return self.connected and self.timer.is_alive()

    def __repr__(self):
        return super().__repr__() + '\n\t\tmostRecentThreat:' + str(self.mostRecentThreat)

