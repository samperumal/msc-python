import os
import os.path 
import AliceTrd2018 as rdr
import numpy as np

path = "D:/Dev/alice/alidata/TRDSampleData"
file = "1910_101_+1400_-1100_30k_0393"

if __name__ == "__main__":
    filepath = os.path.join(path, file)
    reader = rdr.o32reader(filepath)
    analyser = rdr.adcarray()    

    l = set()

    # sm = Super-Module Sector number (0-17, module position on ring from circular cross-section [which pizza slice])
    # layer = Plane Number (0-5, depth within module, increases away from central anode [which peel])
    # stack = Chamber Number (0-4, offset of circular cross-section from central cathode [which donut slice])
    # sidestr = Side on chamber (left or right of the central cathode)

    # data = (16 x 144 x 30) 16 pad rows, 144 channels (8 MCMs x 18 Channels), 30 timebins

    for evno, data in enumerate(reader):
        if evno == 0: continue
        elif evno > 10: break

        #print(evno, data["timestamp"], len(data["datablocks"]), data["datablocks"][0]["size"])
        try:
            analyser.analyse_event(data)
            #print(analyser.sm, analyser.layer, analyser.stack, analyser.sidestr)
            l.add((analyser.sm, analyser.layer, analyser.stack, analyser.sidestr))
        except rdr.datafmt_error as e:
            continue

    print(l)

        

