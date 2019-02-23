import datetime
import numpy
import uproot
from string import Template

inputFile = "alidata/AliESDs.root"
outputFile = "python/treeOutput/test.html"
rootfile = uproot.open(inputFile)

def printNode(file, node, key, depth):
    className = node._classname.decode('utf-8')
    hasKeys = hasattr(node, "keys") and len(node.keys()) > 0
        
    display = Template("($className)\n").substitute(className = className)
    if isinstance(node, uproot.rootio.ROOTDirectory):
        display = Template("$name [$compress compression] ($className)").substitute(name = node.name.decode("utf-8"), compress = node.compression.algoname, className = className)
    elif isinstance(node, uproot.tree.TTreeMethods):
        display = Template("$name - $title [$numentries entries] ($className)").substitute(name = node.name.decode("utf-8"), title = node.title.decode("utf-8"), numentries = node.numentries, className = className)
    elif isinstance(node, uproot.tree.TBranchMethods):
        numBytes = -1
        try: numBytes = node.uncompressedbytes(None)
        except: pass
        display = Template("$name [$bytes bytes] ($className)").safe_substitute(name = node.name.decode("utf-8"), className = type(node).__name__, bytes = numBytes)

    file.write(Template("<li data-jstree='{ \"type\": \"$classname\", $open }'>").substitute(classname = className if hasKeys else "leaf", open = "\"opened\": \"true\"" if depth < 2 else ""))
    file.write(display)

    if hasKeys:
        for key, child in node.iteritems():
            file.write("<ul>\n")
            printNode(file, child, key, depth + 1)
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
    printNode(file, rootfile, None, 0)
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

