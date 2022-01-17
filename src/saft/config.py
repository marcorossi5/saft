def check_histograms(h1, h2):
    """
    Checks if h1 and h2 histograms have the same structure.

    Parameters
    ----------
        - h1: SAF_Histo, the first histogram
        - h2: SAF_Histo, the second histogram

    Raises
    ------
        - ValueError, if h1 and h2 structures are different
    """
    cond = h1.nb_bins == h2.nb_bins and h1.xmin == h2.xmin and h1.xmax == h2.xmax
    if not cond:
        raise ValueError(
            "histogram passed as argument has not the same structure as self."
        )
