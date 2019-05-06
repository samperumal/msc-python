import datetime
import numpy
import uproot

class AliESDRun:
    pass

rootfile = uproot.open("alidata/000294925/18000294925036.100/AliESDs.root")
esd = rootfile["esdTree"]
runs = esd["AliESDRun."]["AliESDRun.fBeamEnergy"].lazyarray()
#a = esd["AliESDRun."]["AliESDRun.fBeamEnergy"]

print(list(runs))