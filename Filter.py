import numpy as np
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import pyqtgraph as pg
import sys
import math
from scipy.signal import butter, filtfilt

def filter(arr, fs, cutoff, order):
    nyquist = .5 * fs
    #n = int(sample_time * sample_rate)
    normal_cutoff = cutoff/nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    retval = filtfilt(b, a, arr)
    #retval = 2 * arr
    #print("Work in progress")
    return retval