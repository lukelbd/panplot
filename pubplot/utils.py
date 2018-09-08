#!/usr/bin/env python3
#------------------------------------------------------------------------------#
# Just a few tools
# These aren't strictly plot-related functions, but will be useful for user
# in the context of making plots.
#------------------------------------------------------------------------------#
import numpy as np

#------------------------------------------------------------------------------#
# Definitions
#------------------------------------------------------------------------------#
def arange(min_, *args):
    """
    Duplicate behavior of np.arange, except with inclusive endpoints; dtype is
    controlled very carefully, so should be 'most precise' among min/max/step args.
    Input:
        stop
        start, stop, [step]
        Just like np.arange!
    Output:
        The array sequence.
    """
    # Optional arguments just like np.arange
    if len(args)==0:
        max_ = min_
        min_ = 0 # this re-assignes the NAME "min_" to 0
        step = 1
    elif len(args)==1:
        max_ = args[0]
        step = 1
    elif len(args)==2:
        max_ = args[0]
        step = args[1]
    else:
        raise ValueError('Function takes from one to three arguments.')
    # All input is integer? Get new "max"
    if min_//1==min_ and max_//1==max_ and step//1==step:
        min_, max_, step = np.int64(min_), np.int64(max_), np.int64(step)
        max_ += 1
    # Input is float or mixed; cast all to float64, then get new "max"
    else:
        # Get the next FLOATING POINT, in direction of the second argument
        # Forget this; round-off errors from continually adding step to min mess this up
        # max_ = np.nextafter(max_, np.finfo(np.dtype(np.float64)).max)
        min_, max_, step = np.float64(min_), np.float64(max_), np.float64(step)
        max_ += step/2
    return np.arange(min_, max_, step)

def autolevels(min_, max_, N=50):
    """
    Function for rounding to nearest <base>.
    """
    def round_(x, base=5): return base*round(float(x)/base)
    # Get the optimal units bases on the range of min to max
    # numbers; N is the number of contour intervals we want to shoot for
    max_tens = np.log10(np.abs(max_))//1
    min_tens = np.log10(np.abs(min_))//1 # e.g. .003 returns -2.7..., -2.7//1 = -3
    if np.isnan(min_tens): min_tens = max_tens
    if np.isnan(max_tens): max_tens = min_tens
        # and 542 returns 2.5..., 2.5//1 = 2
    # And choose a nice, human-readable range from min-to-max
    # for spacing in [tens/2, tens/5, tens/10, tens/20, tens/50,
    #         tens/100, tens/200, tens/500, tens/1000]:
    tens = 10**max(min_tens, max_tens)
    locators, levels = [], []
    factors = [2, 5, 10, 20, 50, 100, 200, 500, 1000]
    for factor in factors:
        spacing = tens/factor
        if str(factor)[0]=='5':
            locator = 5*tens/factor
        else:
            locator = 10*tens/factor
        locators.append(locator)
        levels.append(arange(round_(min_,spacing),round_(max_,spacing),spacing))
        # print(f"For spacing {spacing:.0f}, resulting length: {len(levels[-1]):.0f}")
    lengths = [level.size for level in levels]
    diffs = [abs(length-N) for length in lengths]
    levels = levels[diffs.index(min(diffs))]
    locator = locators[diffs.index(min(diffs))]
    # print(f"From range {min_:.3e} to {max_:.3e}, number of levels: {len(levels):d}")
    return levels, locator
