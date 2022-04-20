from CoordTransform.CRAMtofromLLA import ECEFtofromLLA, CRAMpoint, LLApoint
from Simulator.CoTpulse import CoTpulse
from Simulator.DJITarget import CDS3drone, DJITarget
from Utilities.TimeUtils import millisSinceMidnight
from Utilities import constants

class NoDISPATCHnoAdvance(Exception):
    def __init__(self):
        print("\n\t\t\tThe fakeFlightStatus cannot advance() prior to fakeFlightStatus.dispatch()!!!")
        print("\t\t\t\t\tfakeFlightStatus.dispatch() must be executed!!!\n\n")

class InterpCRAM(CRAMpoint):
    def __init__(self,t,ECEF_X, ECEF_Y, ECEF_Z):
        super().__init__(ECEF_X, ECEF_Y, ECEF_Z)
        self.t:float = float(t)

    @staticmethod
    def fromCRAM(t, CRAM:CRAMpoint) -> 'InterpCRAM': return InterpCRAM(t, CRAM.ECEF_X, CRAM.ECEF_Y, CRAM.ECEF_Z)

    def toLLA(self) -> LLApoint: return ECEFtofromLLA.CRAMtoLLA(CRAMpoint(self.ECEF_X, self.ECEF_Y, self.ECEF_Z))

    def __str__(self): return 'InterpCRAM: t={},x={},y={},z={}'.format(self.t, self.ECEF_X, self.ECEF_Y, self.ECEF_Z)


class fakeFlightStatus():
    FLIGHTMILLIS:int = 30000 # Flighttime duration until Interdiction
    # startLLA = LLApoint(37.696373, -122.020752, 1) #PK FIELD
    startLLA = LLApoint(37.715078, -122.179229, 1) #DRAKES BREWERY
    startCRAM = ECEFtofromLLA.LLAtoCRAM(startLLA)

    def __init__(self, curLocation:InterpCRAM=None, flightmillis:int=FLIGHTMILLIS):
        self.flightmillis = flightmillis
        homeSite = InterpCRAM.fromCRAM(millisSinceMidnight(), fakeFlightStatus.startCRAM)
        self.curLocation: InterpCRAM = curLocation or homeSite
        self.target: InterpCRAM = None
        self.DISPATCH = False
        self.INTERDICTION = False
        self.millisToInterdiction:int = None

    def dispatch(self, target:LLApoint):
        self.DISPATCH = True
        self.INTERDICTION = False
        print("\n\n\tfakeFlightStatus().dispatch:", target.toJSON())
        self.millisToInterdiction = millisSinceMidnight() + self.flightmillis
        CRAM = ECEFtofromLLA.LLAtoCRAM(target)
        self.target = InterpCRAM.fromCRAM(self.millisToInterdiction, CRAM )

    def interpolate(p1: InterpCRAM, p2: InterpCRAM, t:int) -> InterpCRAM: # https://gis.stackexchange.com/questions/234364/interpolating-ecef-coordinates
        t_ratio = (t - p1.t) / (p2.t - p1.t)
        new_x = p1.ECEF_X + t_ratio * (p2.ECEF_X - p1.ECEF_X)
        new_y = p1.ECEF_Y + t_ratio * (p2.ECEF_Y - p1.ECEF_Y)
        new_z = p1.ECEF_Z + t_ratio * (p2.ECEF_Z - p1.ECEF_Z)

        return InterpCRAM(t, new_x, new_y, new_z)

    def interdiction(self) -> LLApoint: #returns the point of interdiction or None
        if millisSinceMidnight() >= self.millisToInterdiction:
            print("\n\n>>>> interpolator I N T E R D I C T I O N!!! <<<<<\n\n")
            self.INTERDICTION = True
            self.DISPATCH = False
            self.curLocation = self.target
            return self.curLocation.toLLA()
        return None


    def advance(self, newLocation: LLApoint) -> LLApoint:
        try:
            now = millisSinceMidnight()
            CRAM = ECEFtofromLLA.LLAtoCRAM(newLocation)
            self.target = InterpCRAM.fromCRAM(self.target.t, CRAM)

            if self.interdiction() is None:
                self.curLocation = fakeFlightStatus.interpolate(self.curLocation, self.target, now)
            return self.curLocation.toLLA()
        except AttributeError as err:
            if not self.DISPATCH: raise NoDISPATCHnoAdvance()
            raise(err)


if __name__ == '__main__':
    DISPATCH:bool = False
    WAITTIME:int = 3000
    startSimulation = millisSinceMidnight()

    myFakeFlightStatus = fakeFlightStatus(flightmillis=60000)
    # myDJItarget = CDS3drone.factory(True)
    myDJItarget = DJITarget()
    myCoTPulse = CoTpulse(myDJItarget)
    myCoTPulse.start()
    # myInterceptor = CDS3drone.factory(False, fakeFlightStatus.startLLA)
    myInterceptor = CDS3drone(CDS3drone.FRIENDLY, fakeFlightStatus.startLLA)
    CoTpulse.register(myInterceptor)

    while not DISPATCH:
        DISPATCH = (millisSinceMidnight() - startSimulation > WAITTIME)

    myFakeFlightStatus.dispatch(myDJItarget.curLLA)

    while myFakeFlightStatus.DISPATCH:
        LLA = myFakeFlightStatus.advance(myDJItarget.curLLA)
        myInterceptor.nextPoint(LLA)


    myCoTPulse.stop()
    CDS3drone.closeAll()
