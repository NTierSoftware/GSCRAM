#We receive telemetry from the GStarget app over TCP (usually). But we forward that telemetry to CDS3 over UDP.
import time
from threading import Event, Thread
from typing import Callable

from CoordTransform.CRAMtofromLLA import LLApoint
from Server.Pulse2 import Pulse
# from Simulator.DJITarget import CDS3drone
from Utilities.Exceptions import CoTpulseDeadError

class CoTpulse(Pulse):
    PULSE_RATE = .5
    drones = []

    def __init__(self, drone):
        super().__init__()
        CoTpulse.register(drone)

        if len( CoTpulse.drones ) == 1:
            self.setThread(CoTpulseHelper(self.stopFlag, self.incrementPulseCounter, self.lostConnection, self))

    @classmethod
    def register(cls, drone): cls.drones.append(drone)

    def stop(self):
        self.lostConnection()
        super().stop()
        CoTpulse.drones.clear()



class CoTpulseHelper(Thread): #Defines the thread operation used by CoTpulse.
    def __init__(self, event: Event, incPulse: Callable, dropConn: Callable, myCoTpulse:CoTpulse):
        Thread.__init__(self)
        self.stopped = event
        self.incPulse = incPulse
        self.dropConn = dropConn
        self.connectionValid = True
        self.myCoTpulse = myCoTpulse

    def run(self): #Runs a continuous while loop on a separate thread until the event is triggered to stop.
        while not self.stopped.wait(CoTpulse.PULSE_RATE) and self.connectionValid and not self.myCoTpulse.isStopped:
            try: #update the CDS3 w/ the latest telemetry
                for drone in CoTpulse.drones:
                    LLA: LLApoint = None
                    drone.nextPoint(LLA)

                self.incPulse()
            except ConnectionAbortedError:
                print("\nInterceptorStatusPulse: ConnectionAbortedError, shutting down.")
                raiseErr = not self.myCoTpulse.isStopped
                self.connectionValid = False
                self.dropConn()
                self.myCoTpulse.stop()
                if raiseErr: raise CoTpulseDeadError('\n\tCoTpulse', 'Attempted to send data over a dead socket.')



# if __name__ == '__main__':
#     from CoordTransform.CRAMtofromLLA import LLApoint, ECEFpoint, ECEFtofromLLA
#     # from CoordTransform.CRAMtofromWGS84 import CRAMtofromLLA
#
#     myLLA = LLApoint(37.7, -122.1, .9)
#     print("myLLA:", myLLA.toJSON())
#     myECEF: ECEFpoint = ECEFtofromLLA.LLAtoECEF(myLLA)
#     myLLA: LLApoint = ECEFtofromLLA.ECEFtoLLA(myECEF)
#     print("myLLA:", myLLA.toJSON())
#
#     myHostile:CDS3drone = CDS3drone()
#     myHostile.setHostile()
#     myFriendly:CDS3drone = CDS3drone()
#     myFriendly.setFriendly()
#     MyDroneSim = CoTpulse( myHostile )
#     MyDroneSim.register(myFriendly)
#
#     # MyDroneSim = CoTpulse( CDS3drone(), myLLA )
#     # MyDroneSim.drone.setHostile()
#     # MyDroneSim.drone.setFriendly()
#
#     MyDroneSim.start()
#
#     for i in range(0, 5500):
#         myLLA = LLApoint(37.695330, -122.023154, 100)
#         myECEF: ECEFpoint = ECEFtofromLLA.LLAtoECEF(myLLA)
#         myLLA: LLApoint = ECEFtofromLLA.ECEFtoLLA(myECEF)
#         # MyDroneSim.drone.nextPoint(myLLA)
#         time.sleep(1)
#         myLLA = LLApoint(37.6, -122.016, .1)
#         myECEF: ECEFpoint = ECEFtofromLLA.LLAtoECEF(myLLA)
#         myLLA: LLApoint = ECEFtofromLLA.ECEFtoLLA(myECEF)
#         # MyDroneSim.drone.nextPoint(myLLA)
#         time.sleep(1)
#
#     MyDroneSim.stop()
