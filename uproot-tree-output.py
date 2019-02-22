import datetime
import numpy
import uproot
from string import Template

inputFile = "alidata/000296934/18000296934019.100/AliESDs.root"
outputFile = "python/treeOutput/test.html"
rootfile = uproot.open(inputFile)

def printNode(file, node):
    for key in node.iterkeys():
        child = node.get(key)
        
        hasKeys = hasattr(child, "keys") and len(child.keys()) > 0
        itemCount = 0
        if hasattr(child, "array"): 
            pass#itemCount = len(child.array())
        className = node.get(key)._classname.decode('utf-8')

        if str(key.decode('utf-8')).find("AliESD") >= 0:
            print(className)
        #dataJsTree = Template("{ ""type"": ""$classname"" }").substitute(classname = className)

        file.write(Template("<li class='node' data-jstree='{ \"type\": \"$classname\" }'>").substitute(classname = className if hasKeys else "leaf"))
        file.write(Template("$name $array ($className)\n").substitute(name = key.decode('utf-8'), array = "[" + str(itemCount) + "]" if itemCount > 0 else "", className = className))
        
        if hasKeys:
            file.write("<ul>\n")
            printNode(file, child)
            file.write("</ul>\n")
        
        file.write("</li>\n")

def printHeader(file):
    file.write("<head>\n")
    file.write("<link href='./bootstrap/css/bootstrap.min.css' rel='stylesheet' />\n")
    file.write("<link href='./proton/style.min.css' rel='stylesheet' />\n")
    file.write("<link href='style.css' rel='stylesheet' />\n")
    file.write("<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'></script>\n")
    file.write("<script src='https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.7/jstree.min.js'></script>\n")
    file.write("</head>\n")

def printBody(file):
    file.write("<body>\n")
    file.write("<div>\n")
    file.write(inputFile + "\n")
    file.write("<div id='treeContainer'>\n")
    file.write("<ul>\n")
    printNode(file, rootfile)
    file.write("</ul>\n")
    file.write("</div>\n")
    file.write("</div>\n")
    file.write("</body>\n")
    
with open(outputFile, "w") as file:
    file.write("<html>\n")
    printHeader(file)
    printBody(file)
    file.write("<script type='text/javascript' src='collapse.js'></script>\n")
    file.write("</html>\n")
    file.close()
    pass

