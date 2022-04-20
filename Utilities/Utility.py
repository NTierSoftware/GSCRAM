import errno, os, queue, threading, time
from datetime import datetime

from Utilities.constants import GroundZero
from CoordTransform.CRAMtofromLLA import LLApoint
from CRAMmsg.r920ThreatState import r920ThreatState
from GSmsg.GSBaseMessage import GSBaseMessage
from GSmsg.rErrNoDroneAvailable import rErrNoDroneAvailable
from GSmsg.rInterdiction import rInterdiction
from GSmsg.rtDroneStatus import rtDroneStatus
from GSmsg.tGoHome import tGoHome
from Server.baseGSCRAMsocket import baseGSCRAMsocket, GSCRAMtofromCRAM, GSCRAMtofromGS
from Server.connections import connections
from Server.NetworkThread import NetworkThread
from Simulator.CoTpulse import CoTpulse
from Simulator.DJITarget import CDS3drone, DJITarget
from Simulator.Interpolator import fakeFlightStatus
from Utilities import constants
from Utilities.console import console, debugLog
from Utilities.Exceptions import GSInterceptorDisconnected


class StoppableThread(threading.Thread):
# Thread class with a stop() method. The thread itself has to check regularly for the stopped() condition.
#     https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python
    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()
        self.join()

    def stopped(self): return self._stop_event.is_set()


    def run(self):
        from Server.Looper import Looper
        Looper.mainLoop(self)
        self._stop_event.set()
        Utility.shutDown(" END OF GSCRAM CYCLE\n")


class GSInterceptorStatus:
    GROUNDZERO =  prevStatus = rtDroneStatus(wsInstallId=None, ASdroneId=None, Lat=GroundZero['Lat'],
                                                         Lon=GroundZero['Lon'], Elev=GroundZero['Elev'])

    GoodClasses = (rtDroneStatus, rInterdiction, rErrNoDroneAvailable)
    pulseDisplayRate:int = 10
    DroneStatusQuery = rtDroneStatus()
    DroneStatusQuery.SentTime = constants.AprilFoolsDay2k

    @staticmethod
    def getInterceptorStatus(Query:rtDroneStatus=DroneStatusQuery) -> GSBaseMessage:
        NoGSreads: int = 0
        MaxNoGSreads: int = 1
        NoneStatus:int = 0
        while True:
            try: #Do not send faster than GroundspaceSendRate
                if (datetime.utcnow() - Query.SentTime) >= constants.Groundspacetimedelta :
                    # print('while getInterceptorStatus', end='\n', flush=True)
                    GSCRAMtofromGS.getInstance().sendGSmsg(Query)
                    InterceptorStatus = GSCRAMtofromGS.getInstance().recvGSmsg()
                    if InterceptorStatus is None:
                        NoneStatus +=1
                        if NoneStatus % 5 == 0: print('\nGSInterceptorStatus.getInterceptorStatus(): InterceptorStatus is None!! retrying...', NoneStatus)
                    else: break #Successful receipt of GS Status!
            except queue.Empty:  # if there are too many NoREADs it could be due to a bad connection. So wait a little for reconnection.
                # print('getInterceptorStatus().NoGSreads:', NoGSreads, MaxNoGSreads, end='\n', flush=True)
                NoGSreads  += 1
                if NoGSreads % MaxNoGSreads == 0:
                    print('getInterceptorStatus().NoGSreads:', NoGSreads, MaxNoGSreads, end='\n', flush=True)
                    NoGSreads = 0
                    MaxNoGSreads+= 1
            except Exception as err:
                print('GSInterceptorStatus.getInterceptorStatus EXCEPTION', err, end='\n', flush=True)

        if isinstance(InterceptorStatus, rtDroneStatus):
            GSInterceptorStatus.prevStatus = InterceptorStatus
        elif isinstance(InterceptorStatus, rErrNoDroneAvailable):
            print('No Interceptor avail:', InterceptorStatus)
            InterceptorStatus = GSInterceptorStatus.prevStatus

        # print('GSInterceptorStatus.getInterceptorStatus():', InterceptorStatus)
        return InterceptorStatus



    @staticmethod
    def dispatch(target:LLApoint): pass

    @staticmethod
    def shutDown(): print("GSInterceptorStatus.shutDown()") #this method is overrided by its subclasses.

class GSInterceptorStatPKField(GSInterceptorStatus):
    myDJItarget: DJITarget = None #the self-reporting target
    myCoTPulse: CoTpulse = None
    myInterceptor: CDS3drone = None
    GROUNDZEROLLApoint = LLApoint(constants.GroundZero['Lat'], constants.GroundZero['Lon'], constants.GroundZero['Elev'])


    def __init__(self):
        # GSInterceptorStatPKField.myDJItarget = SpoofedTarget()
        GSInterceptorStatPKField.myDJItarget = DJITarget()
        GSInterceptorStatPKField.myCoTPulse = CoTpulse(GSInterceptorStatPKField.myDJItarget)
        GSInterceptorStatPKField.myCoTPulse.start()
        GSInterceptorStatPKField.myInterceptor = CDS3drone(CDS3drone.FRIENDLY, fakeFlightStatus.startLLA)
        GSInterceptorStatPKField.myCoTPulse.register(GSInterceptorStatPKField.myInterceptor)


    @staticmethod
    def getInterceptorStatus() -> GSBaseMessage:
        myDroneStatus = GSInterceptorStatus.getInterceptorStatus()
        if isinstance(myDroneStatus, rInterdiction):
            debugLog.log("GSInterceptorStatPKField.getInterceptorStatus: Interdiction!!!")
            # GSInterceptorStatPKField.myCoTPulse.stop()  # SIM code

        elif isinstance(myDroneStatus, rtDroneStatus):
            try: LLA = LLApoint(myDroneStatus.Lat, myDroneStatus.Lon, myDroneStatus.Elev)
            except TypeError: #todo bug in Groundspace
                print('err bug in Groundspace: there are Nulls in the Lat/Lon! GSInterceptorStatPKField.getInterceptorStatus(): TypeError from GS:', myDroneStatus)
                myDroneStatus = GSInterceptorStatus.GROUNDZERO
                LLA = GSInterceptorStatPKField.GROUNDZEROLLApoint

            GSInterceptorStatPKField.myInterceptor.nextPoint(LLA)
        else: print('err GSInterceptorStatPKField.getInterceptorStatus(): unexpected status from GS:', myDroneStatus)
        # print('GSInterceptorStatPKField.getInterceptorStatus()', myDroneStatus )
        return myDroneStatus

    @staticmethod
    def dispatch(target: LLApoint):
        print('GSInterceptorStatPKField.dispatch()')
        return

    @staticmethod
    def shutDown():
        if GSInterceptorStatPKField.myCoTPulse is not None:
            GSInterceptorStatPKField.myCoTPulse.stop()
            GSInterceptorStatPKField.myCoTPulse = None
        print("GSInterceptorStatPKField.shutDown()")

class GSInterceptorStatTableTop(GSInterceptorStatus):
    wsInstallId:int = 888
    ASdroneId:int = 555
    mySimFlightStatus: fakeFlightStatus = None
    # myDJItarget: SpoofedTarget = None
    myDJItarget: DJITarget = None

    myCoTPulse: CoTpulse = None
    myInterceptor: CDS3drone = None

    def __init__(self):
        GSInterceptorStatTableTop.mySimFlightStatus = fakeFlightStatus()
        GSInterceptorStatTableTop.myDJItarget = DJITarget()
        # GSInterceptorStatTableTop.myDJItarget = SpoofedTarget()
        GSInterceptorStatTableTop.myCoTPulse = CoTpulse(GSInterceptorStatTableTop.myDJItarget)
        GSInterceptorStatTableTop.myCoTPulse.start()
        GSInterceptorStatTableTop.myInterceptor = CDS3drone(CDS3drone.FRIENDLY, fakeFlightStatus.startLLA)
        GSInterceptorStatTableTop.myCoTPulse.register(GSInterceptorStatTableTop.myInterceptor)


    @staticmethod
    def getInterceptorStatus() -> GSBaseMessage:
        if Utility.Dispatch:
            LLA = GSInterceptorStatTableTop.mySimFlightStatus.advance(GSInterceptorStatTableTop.myDJItarget.curLLA)
            GSInterceptorStatTableTop.myInterceptor.nextPoint(LLA)

        InterceptorStat = rtDroneStatus(GSInterceptorStatTableTop.wsInstallId,
                                        GSInterceptorStatTableTop.ASdroneId,
                                        GSInterceptorStatTableTop.myInterceptor.curLLA.Lat,
                                        GSInterceptorStatTableTop.myInterceptor.curLLA.Lon,
                                        GSInterceptorStatTableTop.myInterceptor.curLLA.Elev)
        # print('GSInterceptorStatTableTop InterceptorStat', InterceptorStat)
        return GSInterceptorStatus.getInterceptorStatus(InterceptorStat)


    @staticmethod
    def dispatch(target: LLApoint):  # https://docs.python.org/3.7/library/functions.html#super
        GSInterceptorStatTableTop.mySimFlightStatus.dispatch(target)

    @staticmethod
    def shutDown():
        print("GSInterceptorStatTableTop.shutting Down()")
        if GSInterceptorStatTableTop.myCoTPulse is not None:
            GSInterceptorStatTableTop.myCoTPulse.stop()
            GSInterceptorStatTableTop.myCoTPulse = None
        # CDS3drone.closeAll()
        GSInterceptorStatTableTop.mySimFlightStatus = None
        print("GSInterceptorStatTableTop.shutDown()")


#SINGLETON!
class Utility:
    state: constants.currentState = constants.currentState.LOOP
    Dispatch:bool=False
    Interdiction: rInterdiction = None

    __instance = None

    networkThread: NetworkThread = None

    GSCRAMlooper: StoppableThread = None

    GSstat:GSInterceptorStatus = None
    numInterceptorStats:int = 0

    @staticmethod
    def getInstance(): # https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm
        if Utility.__instance is None: Utility()
        return Utility.__instance

    def __init__(self): # Virtually private constructor.
        if Utility.__instance is not None: raise Exception("Utility class is a singleton! Use Utility.getInstance().")

        if connections.SIMULATE == connections.LIVE:
            Utility.GSstat = GSInterceptorStatus()
        else:
            if connections.SIMULATE == connections.SELFREPORTINGTARGET: Utility.GSstat = GSInterceptorStatPKField()
            else:
                Utility.GSstat = GSInterceptorStatTableTop()
                # print("\nUtility.GSstat = GSInterceptorStatTableTop()")

        Utility.__instance = self

    @staticmethod
    def startUp() -> bool:
        Utility.networkThread = NetworkThread.getInstance()

        # while not GSCRAMtofromGS.getInstance(restart=True).connected: time.sleep(backoff.backoffTime())
        while not GSCRAMtofromGS.getInstance(restart=True).connected: time.sleep(connections.Timeout)
        Utility.networkThread.register(GSCRAMtofromGS.getInstance())
        # ^^^ END Groundspace Server startUp ^^^

        noInterceptorAvailable:int = 1
        myDroneStatus = Utility.getInterceptorStatus()
        #wait for a drone to become available.
        while myDroneStatus == GSInterceptorStatus.GROUNDZERO:
            debugLog.log(str(noInterceptorAvailable)+'startup: No Interceptor available.')#, "🛪")
            noInterceptorAvailable += 1
            time.sleep(backoff.backoffTime())
            myDroneStatus = Utility.getInterceptorStatus()
            # print('myDroneStatus:', myDroneStatus.toJSON(   ))

        debugLog.log("Groundspace Interceptor status\n" + type(Utility.GSstat ).__name__ + str(myDroneStatus) )

        # print('startUp:myDroneStatus', myDroneStatus)
        # ***BEGIN C-RAM startUp ***
        while not GSCRAMtofromCRAM.getInstance(restart=True).connected: time.sleep(connections.Timeout)
        Utility.networkThread.register(GSCRAMtofromCRAM.getInstance())
        GSCRAMtofromCRAM.getInstance().startHeartBeat(newWeaponId=myDroneStatus.wsInstallId)

        # ^^^ END C-RAM startUp ^^^

        if GSCRAMtofromCRAM.getInstance().is_alive():
            debugLog.log("startUp(): C-RAM client connected:\t\t" + str(connections.CRAMaddress) )
            Utility.GSCRAMlooper = StoppableThread()
            Utility.GSCRAMlooper.start()
            return True

        return False


    @staticmethod
    def DISPATCH(LLA:LLApoint):
        Utility.Dispatch = True
        Utility.Interdiction = None
        Utility.GSstat.dispatch(target=LLA)

    @staticmethod
    def shutDown(msg:str):

        print("\n\n\t\tGSCRAM SHUTTING DOWN:\t" + msg + "\n")
        if Utility.GSCRAMlooper is None: return
        if not Utility.GSCRAMlooper.stopped() :
            try: Utility.GSCRAMlooper.stop()
            except RuntimeError: pass

        try:
            Utility.GSstat.shutDown()
            CDS3drone.closeAll()
            Utility.networkThread.stop()
            baseGSCRAMsocket.shutdownAll()
            console.closeAll()

        except (AttributeError, ConnectionResetError, GSInterceptorDisconnected): pass
        except OSError as err: #https://stackoverflow.com/questions/35179317/python-user-defined-exceptions-to-handle-specific-oserror-codes
            if err.errno == errno.ENOTSOCK: pass

        # os._exit(1) allows the batch file to loop; using any other forms of exit and the batch file fails to loop.
        finally: os._exit(0) # https://stackoverflow.com/questions/19747371/python-exit-commands-why-so-many-and-when-should-each-be-used

    # @staticmethod
    # def isCRAMconnected() -> bool:
    #     try: retVal = Utility.heartBeatPulse.thread.connectionValid and not Utility.heartBeatPulse.isStopped
    #     except Exception: retVal = False
    #     return retVal

    # @staticmethod
    # def isGroundspaceconnected() -> bool:
    #     retVal = True
    #     try:  Utility.getInterceptorStatus()
    #     except (AttributeError, GroundspaceConnectionErr) as err:
    #         retVal = False
    #     return retVal

    @staticmethod
    def getInterceptorStatus() -> GSBaseMessage:
        Utility.numInterceptorStats+= 1
        return Utility.GSstat.getInterceptorStatus()


    @staticmethod
    def GOHOME(interdiction: rInterdiction = None, threat: r920ThreatState = None ):
        GSCRAMtofromCRAM.getInstance().mostRecentThreat = None
        Utility.Dispatch = False
        Utility.Interdiction = None

        if interdiction is None:
            weaponId = threat.weaponId.data
            RecvTime = threat.RecvTime
        else:
            weaponId = interdiction.wsInstallId
            RecvTime = interdiction.RecvTime

        goHome:tGoHome = tGoHome(weaponId)
        GSCRAMtofromGS.getInstance().sendGSmsg(goHome)

        logStr = "\n" + RecvTime.isoformat() + "\tUtility.GOHOME(): " + "\ngoHome: " + goHome.toJSON()
        console.getConsole(console.TELEMETRY).log(logStr)
        debugLog.log(logStr)

        return


    @staticmethod
    def restart():
        # if Utility.GSCRAMlooper is None: return
        if not Utility.GSCRAMlooper.stopped() :
            try: Utility.GSCRAMlooper.stop()
            except RuntimeError: pass
        Utility.GSCRAMlooper = StoppableThread()
        Utility.GSCRAMlooper.start()




class backoff:
    counter = 0
    max = 15
    scale = .2

    @classmethod
    def backoffTime(cls) -> float:
        if cls.counter > cls.max: cls.counter = 0
        cls.counter += 1
        return ( cls.counter * cls.scale)
