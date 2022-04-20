import time

from Simulator.CoTpulse import CoTpulse
from ECEFpoint import LLApoint, ECEFpoint
from CRAMtofromWGS84 import CRAMtofromLLA

myLLA = LLApoint(37.7, -122.1, .9)
print("myLLA:", myLLA.toJSON())
myECEF: ECEFpoint = CRAMtofromLLA.LLAtoECEF(myLLA)
myLLA: LLApoint = CRAMtofromLLA.ECEFtoLLA(myECEF)
print("myLLA:", myLLA.toJSON())

MyDroneSim = CoTpulse( myLLA )
MyDroneSim.drone.setFriendly()
MyDroneSim.start()

for i in range(0, 15000):
# while True:
    myLLA = LLApoint(37.695330, -122.023154, 100)
    myECEF: ECEFpoint = CRAMtofromLLA.LLAtoECEF(myLLA)
    myLLA: LLApoint = CRAMtofromLLA.ECEFtoLLA(myECEF)
    # time.sleep(2)
    MyDroneSim.drone.nextPoint(myLLA)
    myLLA = LLApoint(37.6, -122.016, .1)
    myECEF: ECEFpoint = CRAMtofromLLA.LLAtoECEF(myLLA)
    myLLA: LLApoint = CRAMtofromLLA.ECEFtoLLA(myECEF)
    # time.sleep(2)
    MyDroneSim.drone.nextPoint(myLLA)


MyDroneSim.stop()


