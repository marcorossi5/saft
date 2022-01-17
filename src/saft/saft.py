###########################
#    SAFT MAIN FILE
#    N. Deutschmann
###########################

import xml.etree.ElementTree as ET
from xml.etree.ElementInclude import default_loader
from saft.histos import Histo


class SAFFile:
    def __init__(self, FileName):
        self.SourceFile = FileName
        try:
            self.XMLRoot = ET.XML(default_loader(FileName, ET.parse))
        except ET.ParseError:
            self.AddRootSAF(self.SourceFile)
            try:
                self.XMLRoot = ET.XML(default_loader(FileName, ET.parse))
            except:
                print("Something is wrong with your file")
        self.SampleGlobalInfo = self.XMLRoot.find("SampleGlobalInfo")
        self.Histos = [
            Histo(x) for x in self.XMLRoot.find("Selection").findall("Histo")
        ]

    def AddRootSAF(self, FileName):
        """
        Adds a root <SAF> tag to file. Allows the file parsing through the
        ElementTree XML API.

        Parameters
        ----------
            - fname: str, input file name
        """
        with open(FileName, "r") as original:
            data = original.read()
        with open(FileName, "w") as modified:
            modified.write("<SAF>")
            modified.write(data)
            modified.write("\n</SAF>")
