import numpy as np
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import pyqtgraph as pg
import sys
import math
from scipy.signal import butter, filtfilt 

def filter(arr):
    retval = 2 * arr
    print("Work in progress")
    return retval