import queue, time
import sys
from typing import Optional, Union

from CoordTransform.CRAMtofromLLA import CRAMpoint
from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
from CRAMmsg.r920ThreatState import r920ThreatState
from CRAMmsg.rt702Spoof import rt702Spoof
from CRAMmsg.rt900WeaponCmd import rt900Consts, rt900WeaponCmd
from CRAMmsg.rt902WeaponHeartbeat import rt902WeaponHeartbeat
from CRAMmsg.rt912DoNotEngage import rt912DoNotEngage
from CRAMmsg.rt915NetTime import rt915NetTime
from CRAMmsg.t903WeaponStatus import t903_AI3, t903Consts
from GSmsg.GSBaseMessage import GSBaseMessage
from GSmsg.rErrNoDroneAvailable import rErrNoDroneAvailable
from GSmsg.rInterdiction import rInterdiction
from GSmsg.rtDroneStatus import rtDroneStatus
from GSmsg.tWeaponsFree import tWeaponsFree
from Server.baseGSCRAMsocket import GSCRAMtofromCRAM, GSCRAMtofromGS
from Utilities import constants
from Utilities.console import console, debugLog
from Utilities.Exceptions import GroundspaceConnectionErr, UnexpectedResponseFromGroundspace
from Utilities.TimeUtils import millisSinceMidnight
from Utilities.Utility import StoppableThread, Utility

telemetryLog:console = console.getConsole(console.TELEMETRY)

# https://stackoverflow.com/questions/2917372/how-to-search-a-list-of-tuples-in-python
dictControlCodeToFireControlMode = dict([
            (rt900Consts.ControlCode.RF_SILENCE.value, t903Consts.FireControlMode.RF_SILENCE),
            (rt900Consts.ControlCode.WEAPONS_HOLD.value, t903Consts.FireControlMode.WEAPONS_HOLD),
            (rt900Consts.ControlCode.WEAPON_TIGHT.value, t903Consts.FireControlMode.WEAPONS_TIGHT),
            (rt900Consts.ControlCode.WEAPONS_FREE.value, t903Consts.FireControlMode.WEAPONS_FREE),
            (rt900Consts.ControlCode.MAINTENANCE.value, t903Consts.FireControlMode.MAINTENANCE),
            (rt900Consts.ControlCode.REGISTRATION.value, t903Consts.FireControlMode.REGISTRATION),
            (rt900Consts.ControlCode.SIMULATED_FLIGHT.value, t903Consts.FireControlMode.SIM_FLIGHT),
            (rt900Consts.ControlCode.LOCAL_CONTROL.value, t903Consts.FireControlMode.LOCAL_CONTROL),
            (rt900Consts.ControlCode.REMOTE_INACTIVE.value, t903Consts.FireControlMode.REMOTE_INACTIVE),
            (rt900Consts.ControlCode.REMOTE_ACTIVE.value, t903Consts.FireControlMode.REMOVE_ACTIVE),
            (rt900Consts.ControlCode.CALIBRATION_MODE.value, t903Consts.FireControlMode.CALIB_MODE)
            ])

def process900msg(msg900: rt900WeaponCmd, msg903: t903_AI3) -> t903_AI3 :
    if msg900.fireControlMode == rt900Consts.FireControlMode.NO_STATEMENT:
        msg903.fireControlModes = [Looper.lastCommandedFireControlMode.value]

    if msg900.commandCode == rt900Consts.CommandCode.STATUS_REQU :
        Looper.lastCommandedFireControlMode = dictControlCodeToFireControlMode.get(Looper.msgFromCRAM.controlCode, Looper.lastCommandedFireControlMode)
        msg903.fireControlModes = [Looper.lastCommandedFireControlMode.value]

    msg903.header.transmitTime.data = millisSinceMidnight()
    return msg903


pulseDisplayRate: int = 10
#Filters out the Heartbeat and NetTime messages from CRAM.

# def applicationLevelLinkage() -> GSBaseMessage:
def applicationLevelLinkage() -> Union[r920ThreatState, rt900WeaponCmd, GSBaseMessage]:
    prevNumPulses: int = -1
    NoCRAMinQ:int = 0
    while not Looper.loopThread.stopped():
        try:
            myMsgFromCRAM = GSCRAMtofromCRAM.getInstance().recvCRAMmsg()
            # NoCRAMreads = 0
        except queue.Empty: #https://stackoverflow.com/questions/13795758/what-is-sys-maxint-in-python-3
            NoCRAMinQ += 1 #Python 3 ints do not have a maximum.
            myMsgFromCRAM = None
            if NoCRAMinQ % 100000000 == 0:
                print('applicationLevelLinkage() NoCRAMinQ:', NoCRAMinQ)
                # if NoCRAMinQ >= 9223372000000000000: NoCRAMinQ = 1 #sys.maxsize = 9223372036854775807
        else: #successful receive, parse the CRAMmsg:
            if isinstance(myMsgFromCRAM, rt900WeaponCmd): return myMsgFromCRAM #expw

            # "The 902 message shall be transmitted at a rate of 0.5 Hz."
            if isinstance(myMsgFromCRAM, rt902WeaponHeartbeat):
                numPulses:int = GSCRAMtofromCRAM.getInstance().numBeats
                if (prevNumPulses < numPulses) and (numPulses % pulseDisplayRate == 0): #only print out every pulseDisplayRate heartbeat.
                    newLine = "\n" if (numPulses % 20 == 0) else ""
                    pulseStr = newLine + " " + constants.Heartbeat + str(numPulses)
                    debugLog.log(pulseStr)
                    prevNumPulses = numPulses

            # The 915 message is event driven. The 915 message shall be transmitted at a rate not to exceed 0.1 Hz by either the C2S or the WES.
            elif isinstance(myMsgFromCRAM, rt915NetTime):
                myMsgFromCRAM.sendResponse(GSCRAMtofromCRAM.getInstance(), millisSinceMidnight())


        if GSCRAMtofromCRAM.getInstance().mostRecentThreat: return GSCRAMtofromCRAM.getInstance().mostRecentThreat

        if myMsgFromCRAM and not isinstance(myMsgFromCRAM, (rt902WeaponHeartbeat, rt915NetTime)):
            print('applicationLevelLinkage().myMsgFromCRAM', myMsgFromCRAM)
            return myMsgFromCRAM





# def applicationLevelLinkage() -> GSBaseMessage:
#     prevNumPulses: int = -1
#     myMsgFromCRAM: CRAMBaseMessage = None
#     NoCRAMreads:int = 0
#     MaxNoCRAMreads:int = 1
#     while not Looper.loopThread.stopped():
#         try:
#             myMsgFromCRAM = GSCRAMtofromCRAM.getInstance().recvCRAMmsg(timeout=(MaxNoCRAMreads%4)/5)
#             NoCRAMreads = 0
#         except queue.Empty: #if there are too many NoREADs it could be due to a bad connection. So wait a little for reconnection.
#             NoCRAMreads += 1
#             if NoCRAMreads %MaxNoCRAMreads  == 0:
#                 # print('applicationLevelLinkage().NoCRAMreads:', NoCRAMreads, MaxNoCRAMreads)
#                 NoCRAMreads = 0
#                 MaxNoCRAMreads+=1
#                 # time.sleep((MaxNoCRAMreads%4)/5) #this sleep is necessary for reconn. Try commenting it out and see how reconn doesn't happen.
#             continue
#         except Exception as err:
#             print('applicationLevelLinkage() err', err)
#             continue
#
#         if GSCRAMtofromCRAM.getInstance().mostRecentThreat: return GSCRAMtofromCRAM.getInstance().mostRecentThreat
#
#         if isinstance(myMsgFromCRAM, (r920ThreatState, rt900WeaponCmd)): break #expw
#
# # The 915 message is event driven. The 915 message shall be transmitted at a rate not to exceed 0.1 Hz by either the C2S or the WES.
#         if isinstance(myMsgFromCRAM, rt915NetTime):
#             myMsgFromCRAM.sendResponse(GSCRAMtofromCRAM.getInstance(), millisSinceMidnight())
#             continue
#
#         # "The 902 message shall be transmitted at a rate of 0.5 Hz."
#         if isinstance(myMsgFromCRAM, rt902WeaponHeartbeat):
#             numPulses:int = GSCRAMtofromCRAM.getInstance().numBeats
#             if (prevNumPulses < numPulses) and (numPulses % pulseDisplayRate == 0): #only print out every pulseDisplayRate heartbeat.
#                 newLine = "\n" if (numPulses % 20 == 0) else ""
#                 pulseStr = newLine + " " + constants.Heartbeat + str(numPulses)
#                 debugLog.log(pulseStr)
#                 prevNumPulses = numPulses
#             continue #rt902WeaponHeartbeat
#
#         print('applicationLevelLinkage().myMsgFromCRAM', myMsgFromCRAM)
#
#         # if isinstance(myMsgFromCRAM, rt702Spoof):
#         #     if NoCRAMreads %10 == 0: print('applicationLevelLinkage().NoCRAMreads:', NoCRAMreads)
#         #     NoCRAMreads += 1
#         #     time.sleep(.11)
#         #     continue
#
#     return myMsgFromCRAM
# ^^^^^  APPLICATION LEVEL LINKAGE ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


def DISPATCH(threat : r920ThreatState):  # The drone has been dispatched to the target.
    # if not threat.isaThreat(): return

    logStr = "\n\n" + threat.RecvTime.isoformat() + ">>>>\t\t\t\t WEAPONS FREE !!!\t\t FIRE!! \t\t\t\t<<<<\n\n"
    telemetryLog.log(logStr )
    debugLog.log(logStr)

    Utility.Dispatch = True
    Utility.state = constants.currentState.DISPATCH
    Utility.Interdiction = None

    Utility.DISPATCH(threat.toLLA())

    wf = tWeaponsFree.fromThreatState(threat) #expw
    GSCRAMtofromGS.getInstance().sendGSmsg(wf)

    # Looper.EngagementStatus910.engagementStatus =  t910Consts.EngagementStatus.MISSILE_AWAY.value #ElementUInt8(myMsgFromCRAM.Numr920ThreatStates) #expw
    # CRAMtofromGSCRAM.sendMsg(Looper.EngagementStatus910) #expw

    while Utility.Dispatch:
        myMsgFromCRAM = applicationLevelLinkage()

        # when we receive a r920ThreatState update, notify Groundspace
        if isinstance(myMsgFromCRAM, r920ThreatState): #GSCRAM: "Here's the target; where are you?"
            if myMsgFromCRAM.forwardToGroundspace(GSCRAMtofromGS.getInstance()) is constants.currentState.GOHOME:
                Utility.GOHOME( threat= myMsgFromCRAM)
                return


            # if myMsgFromCRAM.isaThreat():
            #     if myMsgFromCRAM.forwardToGroundspace(GSCRAMtofromGS.getInstance()) is constants.currentState.GOHOME:
            #         Utility.GOHOME( threat= myMsgFromCRAM)
            #         return


            # if not Utility.Dispatch: #If DISPATCH is reset to false then we're in INTERDICTION!
            #     # Utility.GOHOME(threat=myMsgFromCRAM)
            #     myMsgFromCRAM.INTERDICTION()
            #     debugLog.log("LOOPER INTERDICTION Utility.Dispatch FALSE")
            #     return  # After Interdiction, we are no longer in DISPATCH.

            try: InterceptorStatus: GSBaseMessage = Utility.getInterceptorStatus() #We are currently in DISPATCH mode, so we might receive back from GS "Interdiction"
            except GroundspaceConnectionErr as err:
                print("\napplicationLevelLinkage() err: ", err)
                continue

            if InterceptorStatus is None: continue

            if isinstance(InterceptorStatus, rInterdiction):
                myMsgFromCRAM.INTERDICTION()
                Utility.GOHOME(interdiction=InterceptorStatus) #todo confirm w/ Karthik and Guy: GOHOME after INTERDICTION?

                print(InterceptorStatus.RecvTime.isoformat() + "\tLOOPER INTERDICTION rInterdiction " + InterceptorStatus.toJSON() + "\t Utility.Dispatch:" + str(Utility.Dispatch))
                print(GSCRAMtofromCRAM.getInstance())
                return

            if isinstance(InterceptorStatus, (rtDroneStatus, rErrNoDroneAvailable)):
                # print('DISPATCH InterceptorStatus:', InterceptorStatus.toJSON())
                continue #todo send 925 (after further CRAM protocol discussions.

            raise UnexpectedResponseFromGroundspace("\n\ttype: " + str(type(InterceptorStatus))+ " : " + InterceptorStatus.toJSON())

        # if isinstance(myMsgFromCRAM, rt900WeaponCmd):
        #     # process900inDispatch(myMsgFromCRAM, EngagementPlan909) #expw
        #     continue #rt900WeaponCmd
        #
        # if isinstance(myMsgFromCRAM, rt924InterceptorWaypoint):
        #     # myMsgFromCRAM.WILLCOMPLY() #expw
        #     # print("DISPATCH: Airspace response: WILL COMPLY" + myMsgFromCRAM.toJSON(), end='', flush=True)
        #     continue #rt924InterceptorWaypoint
        #
        # if isinstance(myMsgFromCRAM, rt912DoNotEngage):
        #     # doNotEngage(myMsgFromCRAM) #expw
        #     return #rt912DoNotEngage

        # raise UnexpectedResponseFromCRAM("\n\ttype: " + str(type(myMsgFromCRAM))+ " : " + myMsgFromCRAM.toJSON())
        return  #todo kluge


class Looper:
    # networkThread:NetworkThread = NetworkThread.getInstance()
    # loopThread: 'Server.GSCRAM.StoppableThread'
    loopThread: StoppableThread
    lastCommandedFireControlMode = t903Consts.FireControlMode.WEAPONS_HOLD
    msgFromCRAM: GSBaseMessage = None

    @staticmethod
    def mainLoop(myThread:StoppableThread):
        Looper.loopThread = myThread
        debugLog.setShutDownEvent(myThread._stop_event)

        while not Looper.loopThread.stopped():
            try:
                InterceptorStatus: GSBaseMessage = Utility.getInterceptorStatus()
                debugLog.log("\ngetInterceptorStatus()" + str(Utility.numInterceptorStats) + ": " + InterceptorStatus.toJSON())
            except GroundspaceConnectionErr as err: raise err

            Looper.msgFromCRAM = applicationLevelLinkage()
            # todo if Looper.msgFromCRAM is none LOOP continue

            if isinstance(Looper.msgFromCRAM, r920ThreatState):
                DISPATCH(Looper.msgFromCRAM)
                continue

            if isinstance(Looper.msgFromCRAM, rt900WeaponCmd):
                debugLog.log('\n\nRECEIVED from C2S: ' + Looper.msgFromCRAM.toJSON(humanReadable=True))
                response900 = Looper.msgFromCRAM.WILLCOMPLY()
                # Looper.networkThread.sendCRAMmsg(response900)
                GSCRAMtofromCRAM.getInstance().sendCRAMmsg(response900)
                debugLog.log("\nAirspace response: WILL COMPLY: " + response900.toJSON(humanReadable=True))

                if (Looper.msgFromCRAM.commandCode == rt900Consts.CommandCode.STATUS_REQU.value):
                    #6.	Upon receiving a 900 message with Command Code set to 1, the WES shall send the 903 Weapon Status
                    myDroneStatus: rtDroneStatus = Utility.getInterceptorStatus()
                    CRAM: CRAMpoint = CRAMpoint.fromDroneStatus(myDroneStatus)

                    my903 = t903_AI3(weaponId=myDroneStatus.wsInstallId,
                        fireControlModes = [t903Consts.FireControlMode.WEAPONS_HOLD.value],
                        firingUnitECEF_Xs= [CRAM.ECEF_X],
                        firingUnitECEF_Ys= [CRAM.ECEF_Y],
                        firingUnitECEF_Zs= [CRAM.ECEF_Z] )
                    my903 = process900msg(Looper.msgFromCRAM, my903)

                    GSCRAMtofromCRAM.getInstance().sendCRAMmsg(my903)

                    debugLog.log("\nAirspace response: 903 " + my903.toJSON(humanReadable=True))
                    continue

                continue #rt900WeaponCmd


            # if isinstance(Looper.msgFromCRAM, rt912DoNotEngage):
            #     # doNotEngage(Looper.msgFromCRAM) #expw
            #     continue
            #
            # if isinstance(Looper.msgFromCRAM, rt702Spoof):
            #     print('ErrDisconnect:', Looper.msgFromCRAM.toJSON())
            #     # doNotEngage(Looper.msgFromCRAM) #expw
            #     continue


            # print("\n\n\t\tUNEXPECTED MESSAGE FROM CRAM EXPW!!!\n\n" + Looper.msgFromCRAM.toJSON(humanReadable=True))

        # Utility.shutDown(" END OF GSCRAM CYCLE\n")

