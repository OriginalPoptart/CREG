import numpy as np
import time
from subprocess import call
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
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
        self.powercurve1 = pg.PlotCurveItem()
        self.plotwidget.addItem(self.plotcurve1)
        self.plotwidget.addItem(self.plotcurve2)
        self.plotwidget.addItem(self.powercurve1)        

        self.total_length = 360                     # total sample size
        self.time = 1000                            #time of sample in ms

        self.amplitude1 = 1.0
        self.frequency1 = 1.0
        self.offset1 = 0.0
        self.color1 = 'g'

        self.amplitude2 = 1.0
        self.frequency2 = 1.0
        self.offset2 = 45.0
        self.color2 = 'w'

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
        self.plotwidget.setTitle("Test")
        self.plotwidget.setLabel('left', "Voltage(V)")
        self.plotwidget.setLabel('bottom', "Time(s)")
        self.plotwidget.showGrid(x=True, y=True)
        #self.plotwidget.addLegend()
        win.addWidget(self.plotwidget)
        #self.combo = pg.ComboBox()
        #win.addWidget(self.combo)
        butt_win = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom) 
        butt_win2 = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)       

        # labels the buttons
        self.edit_freq_button1 = QtGui.QPushButton("Edit Frequency")
        self.edit_amp_button1 = QtGui.QPushButton("Edit Amplitude")
        self.edit_color_button1 = QtGui.QPushButton("Edit Color")
        self.saveButton = QtGui.QPushButton("Save")

        self.edit_freq_button2 = QtGui.QPushButton("Edit Frequency")
        self.edit_amp_button2 = QtGui.QPushButton("Edit Amplitude")
        self.edit_color_button2 = QtGui.QPushButton("Edit Color")
        self.details_button = QtGui.QPushButton("Details")

        # adds the buttons to the button window
        butt_win.addWidget(self.edit_freq_button1)
        butt_win.addWidget(self.edit_amp_button1)
        butt_win.addWidget(self.edit_color_button1)
        butt_win.addWidget(self.saveButton)

        butt_win2.addWidget(self.edit_freq_button2)
        butt_win2.addWidget(self.edit_amp_button2)
        butt_win2.addWidget(self.edit_color_button2)
        butt_win2.addWidget(self.details_button)

        self.setGeometry(20, 50, 1000, 600)     # Sets the layout

        win.addLayout(butt_win)                 # adds the button window to the main window
        win.addLayout(butt_win2)

        self.setLayout(win)                     # sets the main layout
        self.show()                             # displays the window

    # Connects the logic of the buttons to their respective functions
    def qt_connections(self):
        self.edit_freq_button1.clicked.connect(self.edit_freq1)
        self.edit_amp_button1.clicked.connect(self.edit_amp1)
        self.edit_color_button1.clicked.connect(self.edit_color1)
        self.saveButton.clicked.connect(self.saveToFile)

        self.edit_freq_button2.clicked.connect(self.edit_freq2)
        self.edit_amp_button2.clicked.connect(self.edit_amp2)
        
        #self.details_button.clicked.connect(self.print_details)

    # Updates the graph with the new waveform
    def update(self):
        self.xs = np.linspace(0, 2*np.pi * self.time/1000, 360*(max(self.frequency1, self.frequency2)) + 1)/(2*np.pi)
        
        self.ys1 = self.amplitude1 * np.sin(2*np.pi*self.frequency1*self.xs + self.offset1)
        self.ys2 = self.amplitude2 * np.sin(2*np.pi*self.frequency2*self.xs + (2*self.offset2*np.pi/360))

        self.plotcurve1.setData(self.xs, self.ys1, pen=self.color1, name="AD1")
        self.plotcurve2.setData(self.xs, self.ys2, pen=self.color2, name="AD2")
        self.powercurve1.setData(self.xs, self.ys1 * self.ys2, pen='r', name="Power")

    def edit_amp1(self):
        d, okPressed = QInputDialog.getDouble(self, "Amplitude 1","Value:", self.amplitude1, 0, 2147483647, 2)
        if okPressed:
            self.amplitude1 = d
            self.update()

    def edit_amp2(self):
        d, okPressed = QInputDialog.getDouble(self, "Amplitude 2","Value:", self.amplitude2, 0, 2147483647, 2)
        if okPressed:
            self.amplitude2 = d
            self.update()

    def edit_freq1(self):
        d, okPressed = QInputDialog.getDouble(self, "Frequency 1","Value:", self.frequency1, 0, 2147483647, 2)
        if okPressed:
            self.frequency1 = d
            self.update()

    def edit_freq2(self):
        d, okPressed = QInputDialog.getDouble(self, "Frequency 2","Value:", self.frequency2, 0, 2147483647, 2)
        if okPressed:
            self.frequency2 = d
            self.update()

    def edit_color1(self):
        items = ("Red","Blue","Green", "White")
        item, okPressed = QInputDialog.getItem(self, "Choose Your Color","Color:", items, 0, False)
        if okPressed and item:
            if item == "Red":
                self.color1 = 'r'
            elif item == "Blue":
                self.color1 = 'b'
            elif item == "Green":
                self.color1 = 'g'
            elif item == "White":
                self.color1 = 'w'
            self.update()

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