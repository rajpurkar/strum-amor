"""
Facilitates efficient feature extraction with Matlab bridge.

Run as script to start server. Import and use extraction methods
as clients.

"""
import itertools
import operator
import os

import ipc

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

def load_matlab():
    """
    Imports and starts matlab bridge if not started.

    """
    global mlab
    global MatlabError

    from mlabwrap import mlab
    from mlabraw import error as MatlabError

    mlab.addpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "features/matlab-chroma-toolbox"))


def fetch_data(command):
    """
    Fetches data based on command received by client.

    """
    typ, path = command
    dir, file = os.path.split(path)
    arguments = (dir + "/", file)
    try:
        if typ == "chroma":
            return mlab.extract_chroma(*arguments).T
        if typ == "crp":
            return mlab.extract_crp(*arguments).T
    except MatlabError as e:
        return "Error: %s" %(str(e))


def get_chroma(path):
    """
    Extract chroma.

    """
    return ipc.get_response(("chroma", os.path.abspath(path)))

def get_crp(path):
    """
    Extract crp.

    """
    return ipc.get_response(("crp", os.path.abspath(path)))


def filter_variance(data, level = 0.23):
    """
    Filter frames with low level of variance out.

    """
    dev = np.std(data, axis = 1);
    plt.plot(dev)
    plt.show()
    data = data[dev > level]
    if data.shape[0] < 10:
        print "bad filter variance", data.shape
    return data;

def split(data, n):
    """
    Split data into groups of n (discard last if not multiple of n)

    """
    return [data[i * n:(i + 1) * n] for i in xrange(1, len(data) / n)]

def combine_concat(data):
    """
    Take predictions for each frame and make one flattened list.

    """
    return np.hstack(data)

def combine_maxcount(data):
    """
    Take mode of each frame and combine into one list.

    """
    return np.hstack(scipy.stats.mode(data, axis = 1)[0].squeeze())

def filter_groups(data, mingroup):
    """
    Collapse groups, discarding less than mingroup size.

    """
    gdata = [(elem, len(list(repeats))) for elem, repeats in
             itertools.groupby(data)]
    gfilt = [elem for elem, num in gdata if num >= mingroup]
    return list(itertools.imap(operator.itemgetter(0),
                               itertools.groupby(gfilt)))

def remove_neg(data):
    data = np.array(data)
    data[data < 0 ] = 0
    return data

if '__main__' in __name__:
    load_matlab()
    ipc.run_server(fetch_data)

