###########################
#    SAFT MAIN FILE
#    N. Deutschmann
###########################

import xml.etree.ElementTree as ET
from xml.etree.ElementInclude import default_loader
from saft.saf_histo import SAF_Histo


class SAF_File:
    """
    The main API to read MadAnalysis5 histogram SAF files.
    """

    def __init__(self, fname):
        """
        Parameters
        ----------
            - fname: str, input file name
        """
        self.source_file = fname
        try:
            self.xml_root = ET.XML(default_loader(fname, ET.parse))
        except ET.ParseError:
            self.add_root_to_saf(self.source_file)
            try:
                self.xml_root = ET.XML(default_loader(fname, ET.parse))
            except:
                raise ValueError("Something is wrong with your file")
        self.sample_global_info = self.xml_root.find("SampleGlobalInfo")
        self.histos = [SAF_Histo(x) for x in self.xml_root.findall("Histo")]

    def get_from_title(self, title):
        """
        Returns the histogram whose title matches title (case insensitive).

        Parameters
        ----------
            - title: str, the query title

        Returns
        -------
            - SAF_Histo, the queried histogram. None if the histogram is not found.
        """
        for hist in self.histos:
            if hist.title == title.upper():
                return hist
        return None
    
    def get_title_list(self):
        """
        Returns the list of all the available histogram titles.

        Returns
        -------
            - list, the available histogram titles
        """
        return [hist.title for hist in self.histos]

    def add_root_to_saf(self, fname):
        """
        Adds a root <SAF> tag to file. Allows the file parsing through the
        ElementTree XML API.

        Parameters
        ----------
            - fname: str, input file name
        """
        with open(fname, "r") as original:
            data = original.read()
        with open(fname, "w") as modified:
            modified.write("<SAF>\n")
            modified.write(data)
            modified.write("\n</SAF>")
