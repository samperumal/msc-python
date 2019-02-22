import datetime
import numpy
import uproot
rootfile = uproot.open("alidata/000296934/18000296934019.100/AliESDs.root")
esd = rootfile["esdTree;10"]
runs = esd["AliESDRun."]
print(runs)