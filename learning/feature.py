import os
from multiprocessing.connection import Client

import numpy as np

def get_chroma(path):
    address = ("localhost", 7000)
    connection = Client(address, authkey='strumamor')
    connection.send(os.path.abspath(path))
    data = connection.recv()
    connection.close()
    try:
        return data.T
    except AttributeError:
        return None

def filter_variance(data, level = 0.01):
    dev = np.std(data, axis = 1);
    data = data[dev > level]
    return data;
