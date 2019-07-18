from openpyxl import load_workbook;
import os;
import json;

def main(headersAddress, dataAddress):
    wb = load_workbook("jsroot/TRDDimensions.xlsx")
    ws = wb.active
    headers = [header.value for row in ws[headersAddress] for header in row ]
    
    nestedData = [list(zip(headers, [d.value for d in row])) for row in ws[dataAddress]]
    data = []
    for row in nestedData:
        obj = {}
        for pair in row:
            obj[pair[0]] = pair[1]
        data.append(obj)

    outfile = open("jsroot/components/trd-dimensions.js", "w")
    print("function getDimensions() { const dims = ", file = outfile, end = '')
    json.dump(data, outfile, indent = 4)
    print("\t;\n\n\treturn dims;\n}", file = outfile)
    outfile.close()

    padrows = []
    for module in data:
        for row in range(16):
            used = row < module["zegments"]
            obj = {}
            obj["rid"] = (module["stack"] * 6 + module["layer"]) * 16 + row
            obj["use"] = used
            if (used):
                obj["stk"] = module["stack"]
                obj["lyr"] = module["layer"]
                obj["row"] = row
                obj["rows"] = module["zegments"]
                obj["p0"] = {
                    "y": module["minR"],
                    "z": round(module["minZ"] + row * module["zsize"], 2)
                }
                obj["p1"] = {
                    "y": module["maxR"],
                    "z": round(module["minZ"] + (row + 1) * module["zsize"], 2)
                }
            padrows.append(obj)

    padrows.sort(key = lambda x: x["rid"])

    modules = []
    for module in data:
        obj = {}
        obj["rid"] = (module["stack"] * 6 + module["layer"]) * 16
        obj["stk"] = module["stack"]
        obj["lyr"] = module["layer"]
        obj["row"] = row
        obj["rows"] = module["zegments"]
        obj["p0"] = {
            "y": module["minR"],
            "z": round(module["minZ"], 2)
        }
        obj["p1"] = {
            "y": module["maxR"],
            "z": round(module["maxZ"], 2)
        }
        modules.append(obj)

    modules.sort(key = lambda x: x["rid"])

    outfile = open("jsroot/components/padrow-dimensions.js", "w")
    print("function getPadrowDimensions() {\nconst dims = ", file = outfile, end = '')
    json.dump(padrows, outfile, indent = 4)
    print(";\n\n\treturn dims;\n}", file = outfile)
    
    print("\n\n")

    print("function getModuleDimensions() {\nconst dims = ", file = outfile, end = '')
    json.dump(modules, outfile, indent = 4)
    print(";\n\n\treturn dims;\n}", file = outfile)
    outfile.close()

if __name__ == "__main__":
    main("A3:R3", "A4:S33")