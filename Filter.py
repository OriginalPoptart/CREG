import numpy as np
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import pyqtgraph as pg
import sys
import math
from scipy import signal 

def filter(arr, fs, cutoff, order, passes=1):
    nyquist = .5 * fs
    #n = int(sample_time * sample_rate)
    normal_cutoff = cutoff/nyquist
    #b, a = butter(order, normal_cutoff, btype='low', analog=False)
    sos = signal.butter(order, normal_cutoff, btype='lp', analog=False, output='sos')
    #retval = filtfilt(b, a, arr)
    retval = signal.sosfilt(sos, arr)

    for i in range(passes - 1):
        retval = signal.sosfilt(sos, retval)

    #print("Work in progress")
    return retval