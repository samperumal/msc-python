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
    print("function getDimensions() { return ", file = outfile, end = '')
    json.dump(data, outfile, indent = 4)
    print(";\n}", file = outfile)

    outfile.close()

if __name__ == "__main__":
    main("A3:O3", "A4:O33")