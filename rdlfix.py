import sys, os
from shutil import copyfile
from xml.dom import minidom as dom

filename = ''

def makeWorkingCopy(filename):
    workfile = filename + '_new'
    if(os.path.exists(workfile)):
        if (input("File " + workfile + " will be overwritten. Continue? (Y/N) ").upper() != "N"):
            copyfile(filename,workfile)
            return workfile
        else:
             return None
    else:
        copyfile(filename,workfile)
        return workfile
   
def main():
    workfile = makeWorkingCopy(filename)
    if(workfile == None):
        print("Unable to create file. Quitting")
        return -1
    if(os.path.exists(workfile)):
        print("File Created: "  + workfile + "\n");
        doc = dom.parse(workfile)
        #Fix Header
        root = doc.documentElement
        root.setAttribute("xmlns","http://schemas.microsoft.com/sqlserver/reporting/2008/01/reportdefinition")
        #Remove Report Parameters Layout Nodes
        for node in  root.childNodes:
            if(node.nodeName == "ReportParametersLayout"):
                root.removeChild(node)
        #Reparenting the granchildren nodes directly did not work correctly. Poorly written loop instead!
        nodesToSave = []
        for node in root.childNodes:
            if(node.nodeName == "ReportSections"):
                for childnode in node.childNodes:
                    if(childnode.nodeName == "ReportSection"):
                        for grandchildnode in childnode.childNodes:
                            nodesToSave.append(grandchildnode.cloneNode(True)) #Root adopts the grandchild
                root.removeChild(node)
        #Add the data that was in the ReportSection tag back into the report.
        for item in nodesToSave:
            root.appendChild(item)
        print("Done.")
        with open(workfile, 'w', encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            root.writexml(f)
main()

