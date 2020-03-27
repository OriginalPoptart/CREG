import numpy as np
#import ADS1256 as adc
import time
from subprocess import call
#from scipy.signal import find_peaks
#from PyQt4 import QtGui
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys

class Plotter(QtGui.QWidget):
    # Initializes all element ins the system
    def __init__(self):
        super(Plotter, self).__init__()
        self.init_ui()                              # Initializes the UI
        self.qt_connections()                       # Connects the buttons to their functions
        
        # Creates curve items and adds them to the plot
        self.plotcurve1 = pg.PlotCurveItem()        
        self.plotcurve2 = pg.PlotCurveItem()
        self.plotwidget.addItem(self.plotcurve1)
        self.plotwidget.addItem(self.plotcurve2)        

        self.total_length = 360                     # total sample size
        self.time = 1000                            #time of sample in ms

        self.amplitude1 = 1.0
        self.frequency1 = 1.0
        self.offset1 = 0.0

        self.amplitude2 = 1.0
        self.frequency2 = 1.0
        self.offset2 = 90.0

        # All the needed arrays for graphing
        self.xs = []
        self.ys1 = []
        self.ys2 = []

        # Runs the update function on startup 
        self.update()

    # Initializes all UI elements
    def init_ui(self):
        # Sets title and UI layout
        self.setWindowTitle('Plotter')
        win = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        
        # creates a plot widget and adds it to the window
        self.plotwidget = pg.PlotWidget()
        win.addWidget(self.plotwidget)
        #self.combo = pg.ComboBox()
        #win.addWidget(self.combo)
        butt_win = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom) 
        butt_win2 = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)       

        # labels the buttons
        self.amp_plus_button = QtGui.QPushButton("Amplitude +")
        self.amp_minus_button = QtGui.QPushButton("Amplitude -")
        self.freq_plus_button = QtGui.QPushButton("Frequency +")
        self.freq_minus_button = QtGui.QPushButton("Frequency -")
        self.saveButton = QtGui.QPushButton("Save")

        self.amp_plus_button2 = QtGui.QPushButton("Amplitude +")
        self.amp_minus_button2 = QtGui.QPushButton("Amplitude -")
        self.freq_plus_button2 = QtGui.QPushButton("Frequency +")
        self.freq_minus_button2 = QtGui.QPushButton("Frequency -")
        self.details_button = QtGui.QPushButton("Details")

        # adds the buttons to the button window
        butt_win.addWidget(self.amp_plus_button)
        butt_win.addWidget(self.amp_minus_button)
        butt_win.addWidget(self.freq_plus_button)
        butt_win.addWidget(self.freq_minus_button)
        butt_win.addWidget(self.saveButton)

        butt_win2.addWidget(self.amp_plus_button2)
        butt_win2.addWidget(self.amp_minus_button2)
        butt_win2.addWidget(self.freq_plus_button2)
        butt_win2.addWidget(self.freq_minus_button2)
        butt_win2.addWidget(self.details_button)

        self.setGeometry(20, 50, 1000, 600)     # Sets the layout

        win.addLayout(butt_win)                 # adds the button window to the main window
        win.addLayout(butt_win2)

        self.setLayout(win)                     # sets the main layout
        self.show()                             # displays the window

    # Connects the logic of the buttons to their respective functions
    def qt_connections(self):
        self.amp_plus_button.clicked.connect(self.amp_plus)
        self.amp_minus_button.clicked.connect(self.amp_minus)
        self.freq_plus_button.clicked.connect(self.freq_plus)
        self.freq_minus_button.clicked.connect(self.freq_minus)
        self.saveButton.clicked.connect(self.saveToFile)

        self.amp_plus_button2.clicked.connect(self.amp_plus2)
        self.amp_minus_button2.clicked.connect(self.amp_minus2)
        self.freq_plus_button2.clicked.connect(self.freq_plus2)
        self.freq_minus_button2.clicked.connect(self.freq_minus2)
        self.details_button.clicked.connect(self.print_details)

    # Updates the graph with the new waveform
    def update(self):
        self.xs = np.linspace(0, 2*np.pi * self.time/1000, 360*(max(self.frequency1, self.frequency2)))/(2*np.pi)
        
        self.ys1 = self.amplitude1 * np.sin(2*np.pi*self.frequency1*self.xs + self.offset1)
        self.ys2 = self.amplitude2 * np.sin(2*np.pi*self.frequency2*self.xs + (2*self.offset2*np.pi/360))

        self.plotcurve1.setData(self.xs, self.ys1, pen='g')
        self.plotcurve2.setData(self.xs, self.ys2, pen='w')

        
    # Increments amplitude1
    def amp_plus(self):
        self.amplitude1 += 1
        self.update()

    # Decrements amplitude1
    def amp_minus(self):
        self.amplitude1 -= 1
        self.update()

    # Increments frequency1
    def freq_plus(self):
        self.frequency1 += 1
        self.update()

    # Decrements frequency1
    def freq_minus(self):
        self.frequency1 -= 1
        self.update()

    # Increments amplitude1
    def amp_plus2(self):
        self.amplitude2 += 1
        self.update()

    # Decrements amplitude1
    def amp_minus2(self):
        self.amplitude2 -= 1
        self.update()

    # Increments frequency1
    def freq_plus2(self):
        self.frequency2 += 1
        self.update()

    # Decrements frequency1
    def freq_minus2(self):
        self.frequency2 -= 1
        self.update()

    def print_details(self):
        print("Work in progress")

    # Calibrates the peak voltage for autosets, as well as 
    def calibrate(self):
        print("Bruh")

    # Writes the data into the save file
    def saveToFile(self):
        F = open("data", "w")
        for i in range (self.total_length):
            F.write(str(self.xs[i]) + "\t" + str(self.ys1[i]) + "\t" + str(self.ys2[i]) + "\n")
        F.close()
        print("Saving to data file")

def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Test')
    ex = Plotter()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()