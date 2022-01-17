from copy import deepcopy
import numpy as np
from saft.config import check_histograms


class SAF_Histo:
    """
    Histogram from SAF file.
    """

    def __init__(self, xml_histo):
        """
        Parameters
        ----------
            - xml_histo: xml.etree.ElementTree.Element, the parsed histogram
        """
        (
            self.num_hist,
            self.title,
            self.nb_bins,
            self.xmin,
            self.xmax,
        ) = parse_description(xml_histo.find("Description").text)

        (
            self.nb_events,
            self.total_weight,
            self.nb_events_in_histo,
            self.total_weight_in_histo,
        ) = parse_statistics(xml_histo.find("Statistics").text)

        self.underflow, self.data, self.uncertainties, self.overflow = parse_data(
            xml_histo.find("Data").text
        )

        # store the bin edges
        self.bin_size = (self.xmax - self.xmin) / self.nb_bins
        self.bins = np.linspace(self.xmin, self.xmax, self.nb_bins + 1)

    def __repr__(self):
        return """Histogram: %s, %d bins in [%.3f,%.3f]""" % (
            self.title,
            self.nb_bins,
            self.xmin,
            self.xmax,
        )

    def __str__(self):
        return np.array_str(self.data)

    def Mathematica(self):
        """ Outputs a Mathematica histogram. """
        points = zip(self.lbins, self.data)
        spoints = ["{{{:f},{:f}}}".format(x, y) for (x, y) in points]
        spoints = ",".join(spoints)
        mathematica_output = "ListStepPlot[{{{}}}, PlotRange -> Full, PlotRangePadding -> None, Frame -> True]".format(
            spoints
        )
        return mathematica_output

    def MathematicaList(self):
        """ Outputs a list of Mathematica histograms. """
        #
        points = zip(self.lbins, self.data)
        spoints = ["{{{:f},{:f}}}".format(x, y) for (x, y) in points]
        spoints = ",".join(spoints)
        mathematica_output = "{{{}}}".format(spoints)
        return mathematica_output

    def __add__(self, h2):
        """
        Adds self to h2 histogram.

        Parameters
        ----------
            - h2: SAF_Histo, the histogram to multiply self

        Returns
        -------
            - SAF_Histo, the resulting histogram
        """
        h1 = deepcopy(self)
        h1.title += "+" + h2.title
        add_fn = lambda x, y: x + y
        return histograms_op(add_fn, h1, h2)

    def __sub__(self, h2):
        """
        Subtracts self to h2 histogram.

        Parameters
        ----------
            - h2: SAF_Histo, the histogram to multiply self

        Returns
        -------
            - SAF_Histo, the resulting histogram
        """
        h1 = deepcopy(self)
        h1.title += "-" + h2.title
        sub_fn = lambda x, y: x - y
        return histograms_op(sub_fn, h1, h2)

    def __mul__(self, h2):
        """
        Multiplies self to h2 histogram.

        Parameters
        ----------
            - h2: SAF_Histo, the histogram to multiply self

        Returns
        -------
            - SAF_Histo, the resulting histogram
        """
        h1 = deepcopy(self)
        h1.title += "*" + h2.title
        mul_fn = lambda x, y: x * y
        return histograms_op(mul_fn, h1, h2)

    def get_normalized(self):
        """
        Returns a normalized copy of the histogram

        Returns
        -------
            - SAF_Histo, the normalized histogram

        """
        h = deepcopy(self)
        norm = h.data.sum() + h.underflow[0] + h.overflow[0]
        h.data /= norm
        h.underflow /= norm
        h.overflow /= norm
        return h


def parse_description(description_text):
    """
    Get elements from histogram <Description> tag.
    Parameters
    ----------
        - description_text: str, the description content

    Returns
    -------
        - int, the histogram number in the SAF file
        - str, the histogram title
        - int, the histogram number of bins
        - float, the histogram first bin lower edge
        - float, the histogram last bin upper edge
    """
    descr = description_text.strip("\n").split("\n")
    num_h, title = descr[0].strip(' "').split("_")
    nb_bins, xmin, xmax = descr[2].strip().split()
    return int(num_h), title, int(nb_bins), float(xmin), float(xmax)


def parse_statistics(statistics_text):
    textlines = statistics_text.strip("\n").split("\n")
    return [float((x.split())[0]) for x in textlines[0:4]]


def parse_data(data_text):
    """
    Parses data and saves histogram into an array.

    Parameters
    ----------
        - data_text: str, the parsed histogram as a string

    Returns
    -------
        - np.array, histogram underflow value and uncertainty of shape=(2,)
        - np.array, the histogram of shape=(nb_bins,)
        - np.array, the histogram uncertainties of shape=(nb_bins,)
        - np.array, histogram overflow value and uncertainty of shape=(2,)
    """
    lines = data_text.strip(" \n").split("\n")
    underflow = np.array(lines[0].split()[:2], dtype=float)
    overflow = np.array(lines[-1].split()[:2], dtype=float)
    data = list(map(lambda x: x.split()[:2], lines[1:-1]))
    data = np.array(data, dtype=float)
    return underflow, data[:, 0], data[:, 1], overflow


def histograms_op(fn, h1, h2):
    """
    Generic operation between two histograms.

    Parameters
    ----------
        - function: the histograms function
        - h1: SAF_Histo, the first histogram
        - h2: SAF_Histo, the second histogram

    Returns
    -------
        - SAF_Histo, the resulting histogram
    """
    check_histograms(h1, h2)

    h1.underflow = fn(h1.underflow, h2.underflow)
    h1.overflow = fn(h1.overflow, h2.overflow)
    h1.nb_events = fn(h1.nb_events, h2.nb_events)
    h1.total_weight = fn(h1.total_weight, h2.total_weight)
    h1.nb_events_in_histo = fn(h1.nb_events_in_histo, h2.nb_events_in_histo)
    h1.total_weight_in_histo = fn(h1.total_weight_in_histo, h2.total_weight_in_histo)
    h1.data = fn(h1.data, h2.data)
    return h1
