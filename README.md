# SAF files Treatment

A small library to process SAF files output by
[MadAnalysis 5](https://launchpad.net/madanalysis5). It provides a representation
of histograms that can then be manipulated in order to produce customized plots.
It relies on the Python library `xml.etree`.

## Features

### File importation

The main class is the `SAFFile` class, which represents the file as a whole.

**Basic usage:** `mySAF=SAFFile(<filename>)` to import a SAF file.

**Note:** The file is modified to have a `<SAF>...</SAF>` as a root if needed.

### Histograms

`SAF_File` objects have an attribute called `histos` which is a list of `SAF_Histo`
objects representing the histograms defined in the [saft](src/saft/saft.py) module:

```python
from saft.saft import SAF_FILE
saf_file = SAF_File("MadAnalysis5job.saf")
h = saf_file.histos[0]
```

The following attributes are the most important:

* `Data` is a list that contains the entries of the histogram
* `lbins` is a list that contains the left-hand limit of each data point's bins
* `binsize` is the size of the binsize, `nbins` is the number of bins
* `xmin` and `xmax` are the bounds of the histogram's x-axis
* `Overflow` and `Underflow` are the sums of weights of events right and left of
the histogram bounds.
* `DataNorm` is the sum of the weights over all entries of the histogram and the
over- and underflow
* `Title` holds the name of the histogram. At the moment this is just a string of
the form `selection*` since SAF files do not store any meaningful titles. It
should be edited by the user.

The following methods are implemented

* `Normalize` takes no argument and returns a histogram normalized such that the
sum of weights below, in and above the histogram evaluates to 1.
* Algebraic operations on histograms with the same `nbins`, `xmin` and `xmax`:
`+,-,*,/` return a histogram with the operation applied bin by bin.
* `str(h)` returns `Histogram: <Title>, <nbins> bins in [<xmin>,<xmax>]`
* `print h` returns `Data` line by line.
* `MathematicaList` takes no argument and returns a string in the format of a
Mathematica list of the form `{{x1,y1},...,{xN,yN}}` where the `xi` are the
left-hand limit of each bin
* `Mathematica` takes no argument and returns a string in the format of a
Mathematica command using `ListStepPlot`, which can be directly evaluated to
produce a histogram.

---

## Important note

Forked from [here](https://github.com/ndeutschmann/saft) and turned into a
python package.

At the moment SAFT only works out of the box with SAF files for MA5 analyses
that *do not* contain cuts due to a parsing issue with "<" symbols inside tag
texts. One needs to find them and remove them by hand in the cut descriptions in
order to be able to handle cuts.

---

## Todo list

* Rework the nomenclature (choose capitalization rules once and for all)
* Add a `Cut` class
* Handle errors with "<" symbols in cut descriptions which cause parsing failures
* Better handling of the data (weights, normalization, cross sections etc.)
* Add error handling
* Better importation procedures: find a way to get the information on the
content of the histograms
