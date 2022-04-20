# JD, Alex Erf, Airspace, alex.erf@airspace.co, 7/31/2018
from CRAMmsg.CRAMBaseMessage import CRAMBaseMessage
# from CRAMmsg.Element import Element
from CRAMmsg.r909EngagementPlan import r909EngagementPlan
from CRAMmsg.r920ThreatState import r920ThreatState
from CRAMmsg.rt900WeaponCmd import rt900WeaponCmd
from CRAMmsg.rt902WeaponHeartbeat import rt902WeaponHeartbeat
from CRAMmsg.rt912DoNotEngage import rt912DoNotEngage
from CRAMmsg.rt915NetTime import rt915NetTime
from CRAMmsg.rt922MeteorlogicalData import rt922MeteorlogicalData
# from CRAMmsg.rt924InterceptorWaypoint import rt924InterceptorWaypoint
# from GSmsg.ErrDisconnect import ErrDisconnect
from CRAMmsg.rt702Spoof import rt702Spoof
from Utilities.NumConversion import uint16FromBytes
from Utilities.Exceptions import UnexpectedResponseFromCRAM

CRAMmsgtypes = {
    915: rt915NetTime,
    900: rt900WeaponCmd,
    902: rt902WeaponHeartbeat,
    909: r909EngagementPlan,
    912: rt912DoNotEngage,
    920: r920ThreatState,
    922: rt922MeteorlogicalData,
    # 7001: ErrDisconnect,
    702: rt702Spoof,
}
# 924: rt924InterceptorWaypoint
# 903: t903WeaponStatus,
# 910: t910EngagementStatus,
# 925: t925InterceptorStatus,
# 926: r926WeaponEmplacement

# https://softwareengineering.stackexchange.com/questions/351389/dynamic-dispatch-from-a-string-python
def getMessageFromBytes(msgBytes: bytearray) -> CRAMBaseMessage:
    msgId = uint16FromBytes(msgBytes[4:6])

    try:
        # retVal = CRAMmsgtypes[msgId].genFromBytes(msgBytes)
        # print('getMessageFromBytes', retVal)
        return CRAMmsgtypes[msgId].genFromBytes(msgBytes)
    except KeyError: raise UnexpectedResponseFromCRAM(msgId, msgBytes)
