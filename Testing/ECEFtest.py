
import sys, time
sys.path.extend(['\\Python37\\Lib\\json', '\\GSCRAM', '\\GSCRAM\\src'])

from CoordTransform.ECEFpoint import ECEFpoint #, LLApoint
from CoordTransform.CRAMtofromWGS84 import CRAMtofromLLA

print('Python %s on %s' % (sys.version, sys.platform))

myECEF = ECEFpoint(-2679471.7699948, -4284265.24613681, 3878704.25860951)
CRAMtofromLLA.log(myECEF)
# myLLA = ECEFtofromLLA.ECEFtoLLA(myECEF)
# ECEFtofromLLA.write(myLLA)
# myECEF = ECEFtofromLLA.LLAtoECEF(myLLA)
# ECEFtofromLLA.write(myECEF)

myNewLLA = CRAMtofromLLA.calc(myECEF)
myNewECEF = CRAMtofromLLA.calc(myNewLLA)
time.sleep(90)
CRAMtofromLLA.terminate()

