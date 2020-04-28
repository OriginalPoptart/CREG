import numpy as np
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import pyqtgraph as pg
import sys
import math
from scipy import signal 

def filter(arr, fs, cutoff, order):
    """Uses scipy butterworth filter with the given params

    Arguments:
        arr {float array} -- data to be filtered
        fs {int} -- sampling rate per second
        cutoff {float} -- cutoff frequency
        order {int} -- order of the filter

    Returns:
        float array -- filtered data array
    """    
    nyquist = .5 * fs
    normal_cutoff = cutoff/nyquist
    sos = signal.butter(order, normal_cutoff, btype='lp', analog=False, output='sos')
    retval = signal.sosfilt(sos, arr)

    return retval