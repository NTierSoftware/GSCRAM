import socket
# sys.path.extend([ '\\GSCRAM', '\\GSCRAM\\src', '..\\' ])
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from CoordTransform.CRAMtofromLLA import LLApoint
from Server.connections import connections
from Simulator.threadedSimSocket import threadedSimSocket
from Utilities.CfgParse import KvpReader
from Utilities.console import console
from Utilities.Exceptions import selectErrs, NetworkThreadTimeout, threadedSocketNoTelemetryYet

class noDJITargetPositionData(Exception):
    def __init__(self): print("\n\t\t\tError: No position data from DJI Target!\n")


class CDS3drone:
    configr = KvpReader()
    deployment  = configr.getvalue(key_name="Deployment")
    CDS3UDP = configr.getvalue(key_name="CDS3UDP", section_name=deployment)
    FRIENDLYCoTport = 22501
    HOSTILECoTport = 22503

    FRIENDLY = 'a-f-A-M-F-Q'
    HOSTILE = 'a-h-A-M-F-Q'

    Registry = []

    InitXML = '''<event
            version="2.0"
            type="uninitialized Friendly or Hostile?"
            qos="0-r-c"
            opex=""
            how="m-g"
            uid="uninitialized"
            time="2001-04-01T01:01:01.0000001Z"
            start="2001-04-01T01:01:01.0000001Z"
            stale="2001-04-01T01:01:01.0000001Z">
            <point
                hae="0.0"
                lat="00.0000000000001"
                lon="-000.000000000001"/> </event>'''


    def __init__(self, friendOrfoe:str, home:LLApoint=None):
        self.Log:console = console.getConsole(console.TELEMETRY)
        self.CDS3conn = None
        self.server_address = ()

        self.curLLA:LLApoint = home or LLApoint(0,0,0)
        self.tree = ET.fromstring(CDS3drone.InitXML)
        self.pointAttrib = self.tree.find("point")

        self.setTime()
        if friendOrfoe == CDS3drone.HOSTILE:
            # self.tree.set('uid', 'Shadow:1')
            # self.tree.set('type', CDS3drone.HOSTILE)
            # self.server_address = (CDS3drone.CDS3UDP, CDS3drone.HOSTILECoTport )
            self.setHostile()
        else:
            # self.tree.set('uid', 'Airspace')
            # self.tree.set('type', CDS3drone.FRIENDLY)
            # self.server_address = (CDS3drone.CDS3UDP, CDS3drone.FRIENDLYCoTport)
            self.setFriendly()

        self.startup()
        CDS3drone.Registry.append(self) #register self
        self.nextPoint(self.curLLA)

    @classmethod
    def closeAll(cls):
        for drone in cls.Registry: drone.shutdown()
        cls.Registry.clear()

    # We receive telemetry from the GStarget app over TCP (usually). But we forward that telemetry to CDS3 over UDP.
    def startup(self): # Create a UDP socket
        self.CDS3conn= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def shutdown(self):
        print("\nCDS3drone.shutdown():", self.getUID() )
        try: self.CDS3conn.shutdown(socket.SHUT_RDWR)
        except AttributeError:pass
        try: self.CDS3conn.close()
        except AttributeError:pass

    def setFriendly(self):
        # self.shutdown()
        self.tree.set('uid', 'Airspace')
        self.tree.set('type', CDS3drone.FRIENDLY)
        self.server_address = (CDS3drone.CDS3UDP, CDS3drone.FRIENDLYCoTport )
        # self.startup()
    def setHostile(self):
        # self.shutdown()
        self.tree.set('uid', 'Shadow:1')
        self.tree.set('type', CDS3drone.HOSTILE)
        self.server_address = (CDS3drone.CDS3UDP, CDS3drone.HOSTILECoTport )
        # self.startup()

    def getUID(self): return self.tree.get("uid")
    def setUID(self, uid:str): self.tree.set('uid', uid)

    def setTime(self):
        now = datetime.utcnow()
        nowStr = now.isoformat() + 'Z'
        self.tree.set("time", nowStr)
        self.tree.set("start", nowStr)
        now += timedelta(seconds=1)
        self.tree.set("stale", now.isoformat() + 'Z')

    def nextPoint(self, point: LLApoint=None):
        if point is not None:
            self.curLLA = point
            self.pointAttrib.set("hae", str(point.Elev))
            self.pointAttrib.set("lat", str(point.Lat))
            self.pointAttrib.set("lon", str(point.Lon))

        self.setTime()
        self.CDS3conn.sendto(ET.tostring(self.tree), self.server_address)
        self.Log.log(str(self))


    def log(self, msg:str=None):
        if msg is None: msg = str(self)
        self.Log.log( msg )

    def printTree(self):
        # print(self.tree.attrib)
        for child in self.tree:
            print('child: ', 'tag: ', child.tag, 'attrib: ' , child.attrib)
            childcnt = 0
            for x in child:
                childcnt += 1
                print("childcnt", childcnt)
                print('x: ', 'tag: ' , x.tag, 'attrib: ' , x.attrib)

    def toLLA(self) ->LLApoint:
        return LLApoint(self.pointAttrib.get("lat"), self.pointAttrib.get("lon"), self.pointAttrib.get("hae"))

    def __repr__(self):
        return self.tree.get("uid") + " sent to CDS3:\t" + self.tree.get("time") \
               + "\thae:" + str(round(self.curLLA.Elev, 3)) \
               + "\tLat:" + str(round(self.curLLA.Lat, 6)) \
               + "\tLon:" + str(round(self.curLLA.Lon, 6))

    def TEST(self):
        while True: self.printTree()


class DJITarget(CDS3drone): #self reporting target
    bufSize = 128
    MAXRECEIVEATTEMPTS: int = 100

    DJIsim: threadedSimSocket = None
    def __init__(self, home:LLApoint=None):
        DJITarget.DJIsim = threadedSimSocket()
        DJITarget.DJIsim.start()

        super().__init__(CDS3drone.HOSTILE, home)
        self.LastKnownPoint:LLApoint = LLApoint(37.8137502, -122.3723917, 1) #SF Treasure Island

        self.nextPoint(None)


    # sample output from drone simulator:
    # $don Target123|version:01|fakeMacAddress;
    # $pos 1541358707796|37.69425829413214|-122.02269567519862|40.0|0.0|0.0|-67.5;\n
    # $pos epoch in millis | lat | lon | elev | pitch | yaw | roll
    def getPoint(self) -> LLApoint:
        try:
            tmpBuf = DJITarget.DJIsim.getMostRecentTelemetry()

            tmpBuf = tmpBuf[(tmpBuf.index("$pos ") + 5): len(tmpBuf)]  # chop off '$pos '

            endTime = tmpBuf.index("|")
            epochMillis = int(tmpBuf[0:endTime]) #milliseconds from the Unix Epoch https://www.epochconverter.com/timezones?q=1552687053&tz=America%2FLos_Angeles
            tmpBuf = tmpBuf[endTime + 1: len(tmpBuf)]
            self.recdTime =  datetime.fromtimestamp(epochMillis/1000)#convert from epoch millis

            endLat = tmpBuf.index("|")
            self.lat = tmpBuf[0:endLat]
            tmpBuf = tmpBuf[endLat + 1: len(tmpBuf)]

            endLon = tmpBuf.index("|")
            self.lon = tmpBuf[0:endLon]
            tmpBuf = tmpBuf[endLon + 1: len(tmpBuf)]

            endHAE = tmpBuf.index("|")
            self.HeightAboveEllipsoid = tmpBuf[0:endHAE]

            self.log(str(self))
            self.LastKnownPoint = LLApoint(self.lat, self.lon, self.HeightAboveEllipsoid)
        except (selectErrs, NetworkThreadTimeout, threadedSocketNoTelemetryYet) as err: self.log("getPoint threadedSocket err: " +str(err))
        except ValueError as err: self.log("DJITarget.getPoint() ValueError: " + str(err))

        return self.LastKnownPoint

    def nextPoint(self, point: LLApoint=None): #method override
        if point is None:
            point = self.getPoint()
            # point = DJITarget.getPoint(self)
        super().nextPoint( point )

    def shutdown(self):
        self.DJIsim.stop()
        super().shutdown()



if __name__ == '__main__':
    from Simulator.CoTpulse import CoTpulse
    from CoordTransform.CRAMtofromLLA import ECEFtofromLLA, ECEFpoint
    myDJItarget = DJITarget()
    myCoTPulse = CoTpulse(myDJItarget)
    myCoTPulse.start()

    myInterceptor = CDS3drone(CDS3drone.FRIENDLY)
    myCoTPulse.register(myInterceptor)

    myLLA = LLApoint(37.695330, -122.023154, 100)
    myOtherLLA = LLApoint(37.6, -122.016, .1)
    for i in range(0, 115500):
        myDJItarget.nextPoint(None)
        myECEF: ECEFpoint = ECEFtofromLLA.LLAtoECEF(myLLA)
        myLLA: LLApoint = ECEFtofromLLA.ECEFtoLLA(myECEF)
        myInterceptor.nextPoint(myLLA)

        myECEF: ECEFpoint = ECEFtofromLLA.LLAtoECEF(myOtherLLA)
        myOtherLLA: LLApoint = ECEFtofromLLA.ECEFtoLLA(myECEF)
        myInterceptor.nextPoint(myOtherLLA)

    myCoTPulse.stop()
