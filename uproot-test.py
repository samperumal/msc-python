import datetime
import numpy
import uproot

class AliESDRun:
    pass

rootfile = uproot.open("alidata/AliESDs.root")#"alidata/000296934/18000296934019.100/AliESDs.root")
esd = rootfile["esdTree"]
runs = esd["AliESDRun."]["AliESDRun.fBeamEnergy"].lazyarray()
#a = esd["AliESDRun."]["AliESDRun.fBeamEnergy"]

print(list(runs))