from openpyxl import load_workbook
import os
import json
import math


def loadDictionaryRowsFromWorkbook(path, headersAddress, dataAddress):
    wb = load_workbook(path)
    ws = wb.active
    headers = [header.value for row in ws[headersAddress] for header in row]

    nestedData = [list(zip(headers, [d.value for d in row]))
                  for row in ws[dataAddress]]

    data = []
    for row in nestedData:
        obj = {}
        for pair in row:
            obj[pair[0]] = pair[1]
        data.append(obj)

    return data


def createSupermoduleStackLayers(data, createPads=True):
    layers = [None for y in range(6)]

    for obj in data:
        layer = obj["layer"] = int(obj["type"][1])
        # Expect one C0 then corresponding C1
        if (obj["type"][3] == '0'):
            layers[layer] = obj.copy()
        else:
            # Create rows of type L?C1, L?C1, L?C0, L?C1, L?C1
            newLayer = [obj.copy() for x in range(5)]
            newLayer[2] = layers[obj["layer"]]
            # Enumerate stacks
            for stack in range(5):
                newLayer[stack]["stack"] = stack

            # Create pad planes
            createPadPlanes(newLayer, createPads)

            # Save completed layer
            layers[layer] = newLayer

    return layers


def createPadPlanes(modules, createPads=True):
    # Determine total length across all stacks
    lTotal = sum(map(lambda module: int(module["Lz"]), modules))
    l0 = int(-lTotal / 2)
    for module in modules:
        module["l0"] = l0
        module["l1"] = l0

        l0 = l0 + int(module["Lrim"])

        r0 = float(module["Rmin"])
        r1 = float(module["Rmax"])

        pads = []

        rows = module["rows"]
        for row in range(rows):
            l1 = l0
            if (row == 0 or row + 1 == rows):
                l1 = l1 + int(module["Lopad"])
            else:
                l1 = l1 + int(module["Lipad"])

            w0 = -(int(module["Wr"]) / 2)

            module["w0"] = round(w0, 2)

            w0 = w0 + (int(module["Wrim"]))
            for col in range(144):
                w1 = w0
                if (col == 0 or col + 1 == 144):
                    w1 = w0 + float(module["Wopad"])
                else:
                    w1 = w0 + float(module["Wipad"])

                pads.append({
                    "row": row,
                    "col": col,
                    "l0": l0,
                    "l1": l1,
                    "w0": round(w0, 2),
                    "w1": round(w1, 2),
                    "r0": r0,
                    "r1": r1
                })
                w0 = w1

            w0 = w0 + (int(module["Wrim"]))
            module["w1"] = round(w0, 2)

            l0 = l1

        l0 = l0 + int(module["Lrim"])

        module["l1"] = l0

        if (createPads):
            module["pads"] = pads


def outputJsonToFile(data, path):
    print("Writing: " + path)
    outfile = open(path, "w")
    json.dump(data, outfile, indent=4)
    outfile.close()

def outputJsonAsFunctionToFile(data, outfile, functionName):
    print("function " + functionName + "() { const dims = ", file = outfile, end = '')
    json.dump(data, outfile, indent = 4)
    print(";\n\n\treturn dims;\n}\n", file = outfile)


def rotate(point, degangle, origin=[0, 0]):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in degrees.
    """
    ox, oy = origin
    px, py = point

    angle = degangle / 180 * math.pi

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

    return {
        "x": round(qx, 2), 
        "y": round(qy, 2)
    }


def createSectorModules(supermodule):
    sectors = []
    for sectorNumber in range(18):
        rotation = 10 + (20 * sectorNumber)
        for layerArray in supermodule:
            for module in layerArray:
                if (module["stack"] != 2):
                    continue

                x0 = module["Rmin"]
                x1 = module["Rmax"]
                y0 = module["w0"] / 10
                y1 = module["w1"] / 10

                sector = {
                    "sec": sectorNumber,
                    "lyr": module["layer"],
                    # Projected coordinates in clockwise-order
                    "d": [
                        rotate([x0, y0], rotation),
                        rotate([x0, y1], rotation),
                        rotate([x1, y1], rotation),
                        rotate([x1, y0], rotation),
                    ]
                }

                sectors.append(sector)

    return sectors


if __name__ == "__main__":
    data = loadDictionaryRowsFromWorkbook(
        "jsroot/PadPlaneDimensions.xlsx", "A1:M1", "A2:M13")

    supermodule = createSupermoduleStackLayers(data, False)
    supermodulePads = createSupermoduleStackLayers(data, True)


    outfile = open("jsroot/geometry/geometries.js", "w")
    outputJsonAsFunctionToFile(createSectorModules(supermodule), outfile, "geomSectorXYPlane")
    outfile.close()

    #outputJsonToFile(supermodule, "jsroot/geometry/supermodule.json")
    #outputJsonToFile(supermodulePads, "jsroot/geometry/supermodule-pads.json")
