from oldsav.ASInterceptorSim import ASInterceptorSimPulse
from ECEFpoint import LLApoint, ECEFpoint
from CRAMtofromWGS84 import CRAMtofromLLA

myLLA = LLApoint(37.7, -122.1, .9)
print("myLLA:", myLLA.toJSON())
myECEF: ECEFpoint = CRAMtofromLLA.LLAtoECEF(myLLA)
myLLA: LLApoint = CRAMtofromLLA.ECEFtoLLA(myECEF)
print("myLLA:", myLLA.toJSON())

MyDroneSim = ASInterceptorSimPulse( myLLA )
MyDroneSim.start()

for i in range(0, 5000):
# while True:
    myLLA = LLApoint(37.695330, -122.023154, 100)
    myECEF: ECEFpoint = CRAMtofromLLA.LLAtoECEF(myLLA)
    myLLA: LLApoint = CRAMtofromLLA.ECEFtoLLA(myECEF)
    # time.sleep(2)
    MyDroneSim.nextPoint(myLLA)
    myLLA = LLApoint(37.6, -122.016, .1)
    myECEF: ECEFpoint = CRAMtofromLLA.LLAtoECEF(myLLA)
    myLLA: LLApoint = CRAMtofromLLA.ECEFtoLLA(myECEF)
    # time.sleep(2)
    MyDroneSim.nextPoint(myLLA)


MyDroneSim.stop()


