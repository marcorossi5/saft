###########################
#    SAFT MAIN FILE
#    N. Deutschmann
###########################

from xml.etree.ElementTree import *
from xml.etree.ElementInclude import *
from histos import *


class SAFFile:
    def __init__(self,FileName):
        self.SourceFile=FileName
        try:
            self.XMLRoot=XML(default_loader(FileName,parse))
        except ParseError:
            self.AddRootSAF(self.SourceFile)
            try:
                self.XMLRoot=XML(default_loader(FileName,parse))
            except:
                print "Something is wrong with your file"
        self.SampleGlobalInfo=self.XMLRoot.find("SampleGlobalInfo")
        self.Histos=[Histo(x) for x in self.XMLRoot.find("Selection").findall("Histo")]

    def AddRootSAF(self,FileName):
        with file(FileName, 'r') as original: data = original.read()
        with file(FileName, 'w') as modified: modified.write("<SAF>\n" + data+"\n</SAF>")
