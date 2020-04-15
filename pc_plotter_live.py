import numpy as np
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import pyqtgraph as pg
import sys
import math
import generator
import waveform

class Plotter(QtGui.QWidget):
    def __init__(self):
        """Initializes all elements in the system"""
        super(Plotter, self).__init__()
        print("Starting init")
        self.total_length = 10000                  # total sample size
        self.time = 1000                           # time of sample in ms
        self.t = 0
        self.time_scale = 10000.0                  # samples per second, total time = total_length/time_scale
        self.chunk_size = 400
        self.time_unit = 1.0
        self.power = 0.0

        self.timer_thing = time.time()

        # Booleans for still, pause and noise
        self.still = True
        self.pause = False
        self.noise = False
        self.unoise = False
        self.show_noise = False
        self.noise_magnitude = .01

        self.waveform1 = waveform.Waveform("Current", color='g')
        self.waveform2 = waveform.Waveform("Voltage", color='w')
        self.noiseform = waveform.Waveform("Uniform Noise", amplitude = .5, frequency=10, color='b')

        # Power Waveform information
        self.show_power = True
        self.colorp = 'r'
        self.show_filtered_power = True
        self.colorfp = 'y'

        # All the needed arrays for graphing
        self.xs = np.zeros(self.total_length)
        self.ys1 = np.zeros(self.total_length)
        self.ys2 = np.zeros(self.total_length)
        self.ysp = np.zeros(self.total_length)
        
        self.init_ui()                              # Initializes the UI
        self.qt_connections()                       # Connects the buttons to their functions

        # Creates curve items and adds them to the plot
        self.plotcurve1 = pg.PlotCurveItem()        
        self.plotcurve2 = pg.PlotCurveItem()
        self.powercurve1 = pg.PlotCurveItem()
        self.noisecurve = pg.PlotCurveItem()
        self.filtercurve = pg.PlotCurveItem()
        self.plotwidget.addItem(self.plotcurve1)
        self.plotwidget.addItem(self.plotcurve2)
        self.plotwidget.addItem(self.powercurve1)  
        self.plotwidget.addItem(self.noisecurve)      
        self.plotwidget.addItem(self.filtercurve)      

        # Sets self.update() to repeat
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1)
        print("init complete!")

    def init_ui(self):
        """Initializes all UI elements"""
        # Sets title and UI layout
        print("Starting init_ui")
        self.setWindowTitle('Digital Wattmeter Simulator')
        win = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        
        # creates a plot widget and adds it to the window
        self.plotwidget = pg.PlotWidget()
        self.plotwidget.setTitle("Power")
        self.plotwidget.setLabel('left', "Voltage(V)")
        self.plotwidget.setLabel('bottom', "Time(s)")
        self.plotwidget.showGrid(x=True, y=True)
        win.addWidget(self.plotwidget) 

        butt_win1 = QtGui.QFormLayout()
        butt_win2 = QtGui.QFormLayout()
        butt_win3 = QtGui.QFormLayout()

        self.space_label = QtGui.QLabel("")

        # ** Column 1 **

        column1 = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        column1.addLayout(self.waveform1.butt_win)
        column1.addLayout(self.waveform2.butt_win)

        # ** Column 2 **
        # Label
        column2 = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        self.label3 = QtGui.QLabel("Sampling/Power")
        butt_win1.addRow(self.label3)

        # Sample Time
        self.edit_time_box = QtGui.QDoubleSpinBox()
        self.edit_time_box.setValue(self.total_length/self.time_scale)
        self.edit_time_box.setGeometry(1,1,1,1) 
        self.edit_time_box.setSingleStep(.1)
        self.edit_time_box.setRange(0, 1000)
        butt_win1.addRow("Sample Time", self.edit_time_box)

        self.time_unit_box = QtGui.QComboBox()
        self.time_unit_box.addItems(["s", "ms", "us"])
        butt_win1.addRow(self.time_unit_box)

        # Live/Still
        self.still_button = QtGui.QPushButton("Still")
        self.still_button.setCheckable(True)
        butt_win1.addRow(self.still_button)

        # Pause
        self.pause_button = QtGui.QPushButton("Pause")
        self.pause_button.setCheckable(True)
        butt_win1.addRow(self.pause_button)

        # Save
        self.save_button = QtGui.QPushButton("Save")
        butt_win1.addRow(self.save_button)

        # Power
        self.show_power_button = QtGui.QPushButton("Show Power")
        self.show_power_button.setCheckable(True)
        self.show_power_button.toggle()
        butt_win2.addRow(self.show_power_button)

        self.color_boxp = QtGui.QComboBox()
        self.color_boxp.addItems(["Red", "Blue", "Green", "White"])
        butt_win2.addRow(self.color_boxp)

        # Power Labels
        self.power_label = QtGui.QLabel()
        butt_win2.addRow(self.power_label)

        self.power_rms_label = QtGui.QLabel()
        butt_win2.addRow(self.power_rms_label)

        self.reactive_power_label = QtGui.QLabel()
        butt_win2.addRow(self.reactive_power_label)

        self.apparent_power_label = QtGui.QLabel()
        butt_win2.addRow(self.apparent_power_label)

        self.power_factor_label = QtGui.QLabel()
        butt_win2.addRow(self.power_factor_label)

        self.lead_lag_label = QtGui.QLabel()
        butt_win2.addRow(self.lead_lag_label)

        self.circuit_type = QtGui.QLabel()
        butt_win2.addRow(self.circuit_type)
        #butt_win2.addRow(self.space_label)

        column2.addLayout(butt_win1)
        column2.addLayout(butt_win2)

        # Column 3
        # Noise
        column3 = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        self.label4 = QtGui.QLabel("Noise")
        butt_win3.addRow(self.label4)

        self.noise_button = QtGui.QPushButton("Random Noise")
        self.noise_button.setCheckable(True)
        butt_win3.addRow(self.noise_button)

        self.rand_noise_box = QtGui.QDoubleSpinBox()
        self.rand_noise_box.setValue(self.noise_magnitude)
        self.rand_noise_box.setGeometry(1,1,1,1) 
        self.rand_noise_box.setSingleStep(.01)
        self.rand_noise_box.setRange(0, 1000)
        butt_win3.addRow("Random Noise", self.rand_noise_box)

        # Uniform noise
        self.noise_button2 = QtGui.QPushButton("Uniform Noise")
        self.noise_button2.setCheckable(True)
        butt_win3.addRow(self.noise_button2)

        self.show_noise_button = QtGui.QPushButton("Show Noise")
        self.show_noise_button.setCheckable(True)
        butt_win3.addRow(self.show_noise_button)

        column3.addLayout(butt_win3)
        column3.addLayout(self.noiseform.butt_win)

        #self.setGeometry(20, 50, 1200, 600)     # Sets the layout size

        win.addLayout(column1)
        win.addLayout(column2)                 # adds the windows to the main window
        win.addLayout(column3)

        #temp = waveform.Waveform("Test")
        #win.addLayout(temp.butt_win)

        self.setLayout(win)                     # sets the main layout
        self.show()                             # displays the window
        print("init_ui complete!")

    
    def qt_connections(self):
        """Connects the logic of the buttons to their respective functions"""
        print("Connecting Buttons...")

        # Live/Timing menu
        self.edit_time_box.valueChanged.connect(self.edit_time)
        self.time_unit_box.currentIndexChanged.connect(self.edit_time_unit)
        self.save_button.clicked.connect(self.saveToFile)
        self.still_button.clicked.connect(self.still_toggle)
        self.pause_button.clicked.connect(self.pause_toggle)
        self.show_power_button.clicked.connect(self.power_toggle)
        self.color_boxp.currentIndexChanged.connect(self.edit_colorp)

        # Noise
        self.noise_button.clicked.connect(self.noise_toggle)
        self.rand_noise_box.valueChanged.connect(self.edit_noise)
        self.noise_button2.clicked.connect(self.noise_toggle2)
        self.show_noise_button.clicked.connect(self.show_noise_toggle)

        print("Buttons Complete!")
        

    def update(self):
        """Calls the function in the generator library"""
        generator.update(self)

    def edit_time(self):
        """Adujusts the time_scale to match the given value with the total_time\n
        Total time in seconds = total_length/time_scale"""
        if(self.edit_time_box.value() > 0):
            self.time_scale = self.total_length / self.edit_time_box.value()
            self.total_time = self.total_length/self.time_scale

    def edit_time_unit(self, i):
        """Sets the units for time"""
        if i == 0:
            self.time_unit = 1.0
        elif i == 1:
            self.time_unit = .001
        elif i == 2:
            self.time_unit = .000001
        else:
            self.time_unit = 1

    def saveToFile(self):
        """# Writes the data into the save file"""
        F = open("data", "w")
        for i in range (self.total_length):
            F.write(str(self.xs[i]) + "\t" + str(self.ys1[i]) + "\t" + str(self.ys2[i]) + "\t" + str(self.ysp[i]) + "\n")
        F.close()
        print("Saving to data file")

    def still_toggle(self):
        """Toggles Still and Live modes"""
        self.still = not self.still
        if(self.still):
            self.t = 0
            self.still_button.setText("Still")
        else:
            self.still_button.setText("Live")
            self.timer_thing = time.time()      # Sets the live timer for timing

    def pause_toggle(self):
        """Toggles pause mode"""
        self.pause = not self.pause

    def power_toggle(self):
        self.show_power = not self.show_power

    def edit_colorp(self, i):
        """Edits color"""
        if i == 0:
            self.colorp = 'r'
        elif i == 1:
            self.colorp = 'b'
        elif i == 2:
            self.colorp = 'g'
        else:
            self.colorp = 'w'

    def noise_toggle(self):
        """Toggle random noise"""
        self.noise = not self.noise

    def noise_toggle2(self):
        """Toggle random noise"""
        self.unoise = not self.unoise

    def show_noise_toggle(self):
        self.show_noise = not self.show_noise

    def edit_noise(self):
        self.noise_magnitude = self.rand_noise_box.value()

def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Digital Wattmeter Simulator')
    ex = Plotter()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()