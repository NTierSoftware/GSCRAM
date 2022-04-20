from CRAMmsg.r909EngagementPlan import r909EngagementPlan
from GSmsg.GSBaseMessage import GSBaseMessage
from datetime import datetime
from CoordTransform.CRAMtofromLLA import ECEFtofromLLA, CRAMpoint, LLApoint
from CRAMmsg.r920ThreatState import r920ThreatState

import json


class tWeaponsFree(GSBaseMessage):
    # MSG_TYPE = 'tWeaponsFree'
    # MSG_TYPE = 900

    def __init__(self, wsInstallId: int, targetId: int,
                 Lat: int, Lon: int, Elev: int,
                 ECEF_Vx: int, ECEF_Vy: int, ECEF_Vz: int, CRAMreqTime: datetime=None):
        self.wsInstallId = wsInstallId
        self.targetId = targetId
        self.Lat = Lat
        self.Lon = Lon
        self.Elev = Elev
        self.ECEF_Vx = ECEF_Vx
        self.ECEF_Vy = ECEF_Vy
        self.ECEF_Vz = ECEF_Vz
        self.CRAMreqTime = CRAMreqTime or datetime.utcnow()

    # def getMsgType(self): return self.MSG_TYPE

    def getDataObject(self) -> dict:
        return {
            'msgType': type(self).__name__,
            'wsInstallId' : self.wsInstallId,
            'targetId' : self.targetId,
            'Lat' : self.Lat,
            'Lon' : self.Lon,
            'Elev' : self.Elev,
            'ECEF_Vx' : self.ECEF_Vx,
            'ECEF_Vy' : self.ECEF_Vy,
            'ECEF_Vz' : self.ECEF_Vz,
            'CRAMreqTime' : self.CRAMreqTime.isoformat(),
        }


    # def getDataObject(self) -> dict:
    #     wf = {}
    #     wf['msgType'] = self.MSG_TYPE
    #     wf['ASdroneId'] = self.ASdroneId
    #     wf['targetId'] = self.targetId
    #     wf['Lat'] = self.Lat
    #     wf['Lon'] = self.Lon
    #     wf['Elev'] = self.Elev
    #     wf['ECEF_Vx'] = self.ECEF_Vx
    #     wf['ECEF_Vy'] = self.ECEF_Vy
    #     wf['ECEF_Vz'] = self.ECEF_Vz
    #     wf['CRAMreqTime'] = self.CRAMreqTime.isoformat()
    #     return wf

    @classmethod
    def fromJSON(cls, jsonStr: str) -> 'GSBaseMessage':
        wf = json.loads(jsonStr)
        dateString = wf['CRAMreqTime']
        return cls(wf['wsInstallId'], wf['targetId'],
                   wf['Lat'], wf['Lon'], wf['Elev'],
                   wf['ECEF_Vx'], wf['ECEF_Vy'], wf['ECEF_Vz'],
                   datetime.fromisoformat(dateString))

        # return cls(wf['ASdroneId'], wf['targetId'],
        #            wf['Lat'], wf['Lon'], wf['Elev'],
        #            wf['ECEF_Vx'], wf['ECEF_Vy'], wf['ECEF_Vz'],
        #            datetime.fromisoformat(dateString))



    def clone(self) -> 'tWeaponsFree':
        return tWeaponsFree(self.wsInstallId, self.targetId, self.Lat, self.Lon, self.Elev,
                            self.ECEF_Vx, self.ECEF_Vy, self.ECEF_Vz, self.CRAMreqTime)



    @classmethod
    def fromThreatState(cls, threat: r920ThreatState): #for expw
        cram = CRAMpoint(threat.trackECEF_X.data, threat.trackECEF_Y.data, threat.trackECEF_Z.data,)
        LLA:LLApoint = ECEFtofromLLA.CRAMtoLLA(cram)
        return cls(wsInstallId=threat.weaponId.data, targetId=threat.sysTrackId.data,
                   Lat=LLA.Lat, Lon=LLA.Lon, Elev=LLA.Elev,
                   ECEF_Vx=threat.trackECEF_Vx.data,
                   ECEF_Vy=threat.trackECEF_Vy.data,
                   ECEF_Vz=threat.trackECEF_Vz.data,
                   CRAMreqTime=datetime.utcnow())


    @classmethod
    def fromEngagementPlan(cls, EngagementPlan: r909EngagementPlan): #for cyte
        cram = CRAMpoint(EngagementPlan.trackECEF_X.data, EngagementPlan.trackECEF_Y.data, EngagementPlan.trackECEF_Z.data,)
        LLA:LLApoint = ECEFtofromLLA.CRAMtoLLA(cram)
        return cls(wsInstallId=EngagementPlan.weaponId.data, targetId=EngagementPlan.sysTrackId.data,
                   Lat=LLA.Lat, Lon=LLA.Lon, Elev=LLA.Elev,
                   ECEF_Vx=EngagementPlan.trackECEF_Vx.data,
                   ECEF_Vy=EngagementPlan.trackECEF_Vy.data,
                   ECEF_Vz=EngagementPlan.trackECEF_Vz.data,
                   CRAMreqTime=datetime.utcnow())

