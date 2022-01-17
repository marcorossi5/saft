# SAF files Treatment

A small library to process SAF files output by
[MadAnalysis 5](https://launchpad.net/madanalysis5). It provides a representation
of histograms that can then be manipulated in order to produce customized plots.
It relies on the Python library `xml.etree`.

## Install

The package can be install through `pip` command:

```bash
git clone https://github.com/marcorossi5/saft
cd saft
pip install -e .
```

It requires [numpy](https://numpy.org/) python package.

## Features

### File importation

The main class is the `SAF_File` class, which represents the file as a whole.

**Basic usage:** `mySAF = SAF_File(<filename>)` to import a SAF file.

**Note:** The file is modified to have a `<SAF>...</SAF>` as a root if needed.

### Histograms

`SAF_File` objects have an attribute called `histos` which is a list of `SAF_Histo`
objects representing the histograms defined in the [saft](src/saft/saft.py) module:

```python
from saft.saft import SAF_File
saf_file = SAF_File("MadAnalysis5job.saf")
```

The available histograms can be inspected with the `get_title_list` and
`get_from_title` methods:

```python
available = saf_file.get_title_list() # get available titles
hist = saf_file.get_from_title(available[0])
```

`hist` is a `SAF_Histo` instance, whose most important attributes are:

* `data` is a numpy array that contains the entries of the histogram
* `bins` is a list that contains the histogram bin edges
* `bin_size` is the size of the binsize, `nbins` is the number of bins
* `xmin` and `xmax` are the bounds of the histogram's x-axis
* `overflow` and `underflow` are the sums of weights of events right and left of
the histogram bounds.
* `title` holds the name of the histogram.

The following methods are implemented

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

* Add a `Cut` class
* Handle errors with "<" symbols in cut descriptions which cause parsing failures
* Better handling of the data (weights, normalization, cross sections etc.)
* Add error handling
* Better importation procedures: find a way to get the information on the
content of the histograms
