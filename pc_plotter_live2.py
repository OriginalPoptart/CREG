import numpy as np
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import pyqtgraph as pg
import sys
import math
import generator

class Plotter(QtGui.QWidget):
    def __init__(self):
        """Initializes all elements in the system"""
        super(Plotter, self).__init__()
        print("Starting init")
        self.total_length = 10000                  # total sample size
        self.time = 1000                           # time of sample in ms
        self.t = 0
        self.time_scale = 10000.0                  # samples per second, total time = total_length/time_scale
        self.chunk_size = 500
        self.time_unit = 1.0
        self.power = 0.0

        self.timer_thing = time.time()

        # Booleans for still, pause and noise
        self.still = True
        self.pause = False
        self.noise = False
        self.unoise = False
        self.noise_magnitude = .01

        # Waveform 1 information 
        self.amplitude1 = 1.0
        self.amp_scale1 = 1.0
        self.frequency1 = 1.0
        self.freq_scale1 = 1
        self.offset1 = 0.0
        self.offset_scale1 = 1.0
        self.phase1 = 0.0
        self.color1 = 'g'

        # Waveform 2 information
        self.amplitude2 = 1.0
        self.amp_scale2 = 1.0
        self.frequency2 = 1.0
        self.freq_scale2 = 1
        self.offset2 = 0.0
        self.offset_scale2 = 1.0
        self.phase2 = 0.0
        self.color2 = 'w'

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
        self.plotwidget.addItem(self.plotcurve1)
        self.plotwidget.addItem(self.plotcurve2)
        self.plotwidget.addItem(self.powercurve1)        

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

        butt_win = QtGui.QFormLayout()
        butt_win3 = QtGui.QFormLayout()

        # ** Column 1 **
        # Waveform 1
        # Label
        self.label1 = QtGui.QLabel("Current")
        butt_win.addRow(self.label1)

        # Frequency
        self.edit_freq_box1 = QtGui.QDoubleSpinBox()
        self.edit_freq_box1.setValue(self.frequency1)
        self.edit_freq_box1.setGeometry(1,1,1,1) 
        self.edit_freq_box1.setSingleStep(.1)
        self.edit_freq_box1.setMaximum(1000)
        butt_win.addRow("Frequency", self.edit_freq_box1)

        self.freq_unit_box1 = QtGui.QComboBox()
        self.freq_unit_box1.addItems(["Hz", "kHz"])
        butt_win.addRow(self.freq_unit_box1)

        # Amplitude
        self.edit_amp_box1 = QtGui.QDoubleSpinBox()
        self.edit_amp_box1.setValue(self.amplitude1)
        self.edit_amp_box1.setGeometry(1,1,1,1) 
        self.edit_amp_box1.setSingleStep(.1)
        self.edit_amp_box1.setRange(-1000, 1000)
        butt_win.addRow("Amplitude", self.edit_amp_box1)

        self.amp_unit_box1 = QtGui.QComboBox()
        self.amp_unit_box1.addItems(["V", "kV", "mV"])
        butt_win.addRow(self.amp_unit_box1)

        # Phase
        self.edit_phase_box1 = QtGui.QDoubleSpinBox()
        self.edit_phase_box1.setValue(self.phase2)
        self.edit_phase_box1.setGeometry(1,1,1,1) 
        self.edit_phase_box1.setSingleStep(15)
        self.edit_phase_box1.setRange(-360, 360)
        self.edit_phase_box1.setWrapping(True)
        butt_win.addRow("Phase", self.edit_phase_box1)

        # Offset
        self.edit_offset_box1 = QtGui.QDoubleSpinBox()
        self.edit_offset_box1.setValue(self.offset1)
        self.edit_offset_box1.setGeometry(1,1,1,1) 
        self.edit_offset_box1.setSingleStep(.1)
        self.edit_offset_box1.setRange(-1000, 1000)
        butt_win.addRow("Offset", self.edit_offset_box1)

        self.offset_unit_box1 = QtGui.QComboBox()
        self.offset_unit_box1.addItems(["V", "kV", "mV"])
        butt_win.addRow(self.offset_unit_box1)

        # Color
        self.color_box1 = QtGui.QComboBox()
        self.color_box1.addItems(["Red", "Blue", "Green", "White"])
        self.color_box1.setCurrentIndex(2)
        butt_win.addRow("Color", self.color_box1)

        self.space_label = QtGui.QLabel(" ")
        butt_win.addRow(self.space_label)

        self.details_button = QtGui.QPushButton("Details")

        # Waveform 2
        # Label
        self.label2 = QtGui.QLabel("Voltage")
        butt_win.addRow(self.label2)

        # Frequency
        self.edit_freq_box2 = QtGui.QDoubleSpinBox()
        self.edit_freq_box2.setValue(self.frequency2)
        self.edit_freq_box2.setGeometry(1,1,1,1) 
        self.edit_freq_box2.setSingleStep(.1)
        self.edit_freq_box2.setMaximum(1000)
        butt_win.addRow("Frequency", self.edit_freq_box2)

        self.freq_unit_box2 = QtGui.QComboBox()
        self.freq_unit_box2.addItems(["Hz", "kHz"])
        butt_win.addRow(self.freq_unit_box2)

        # Amplitude
        self.edit_amp_box2 = QtGui.QDoubleSpinBox()
        self.edit_amp_box2.setValue(self.amplitude2)
        self.edit_amp_box2.setGeometry(1,1,1,1) 
        self.edit_amp_box2.setSingleStep(.1)
        self.edit_amp_box2.setRange(-1000, 1000)
        butt_win.addRow("Amplitude", self.edit_amp_box2)

        self.amp_unit_box2 = QtGui.QComboBox()
        self.amp_unit_box2.addItems(["V", "kV", "mV"])
        butt_win.addRow(self.amp_unit_box2)

        # Phase
        self.edit_phase_box2 = QtGui.QDoubleSpinBox()
        self.edit_phase_box2.setValue(self.phase2)
        self.edit_phase_box2.setGeometry(1,1,1,1) 
        self.edit_phase_box2.setSingleStep(15)
        self.edit_phase_box2.setRange(-360, 360)
        self.edit_phase_box2.setWrapping(True)
        butt_win.addRow("Phase", self.edit_phase_box2)

        # Offset
        self.edit_offset_box2 = QtGui.QDoubleSpinBox()
        self.edit_offset_box2.setValue(self.offset2)
        self.edit_offset_box2.setGeometry(1,1,1,1) 
        self.edit_offset_box2.setSingleStep(.1)
        self.edit_offset_box2.setRange(-1000, 1000)
        butt_win.addRow("Offset", self.edit_offset_box2)

        self.offset_unit_box2 = QtGui.QComboBox()
        self.offset_unit_box2.addItems(["V", "kV", "mV"])
        butt_win.addRow(self.offset_unit_box2)

        # Color
        self.color_box2 = QtGui.QComboBox()
        self.color_box2.addItems(["Red", "Blue", "Green", "White"])
        self.color_box2.setCurrentIndex(3)
        butt_win.addRow("Color", self.color_box2)

        self.details_button = QtGui.QPushButton("Details")

        # ** Column 2 **
        # Label
        self.label3 = QtGui.QLabel("Sampling")
        butt_win3.addRow(self.label3)

        # Sample Time
        self.edit_time_box = QtGui.QDoubleSpinBox()
        self.edit_time_box.setValue(self.total_length/self.time_scale)
        self.edit_time_box.setGeometry(1,1,1,1) 
        self.edit_time_box.setSingleStep(.1)
        self.edit_time_box.setRange(0, 1000)
        butt_win3.addRow("Sample Time", self.edit_time_box)

        self.time_unit_box = QtGui.QComboBox()
        self.time_unit_box.addItems(["s", "ms", "us"])
        butt_win3.addRow(self.time_unit_box)

        # Live/Still
        self.still_button = QtGui.QPushButton("Still")
        self.still_button.setCheckable(True)
        butt_win3.addRow(self.still_button)

        # Pause
        self.pause_button = QtGui.QPushButton("Pause")
        self.pause_button.setCheckable(True)
        butt_win3.addRow(self.pause_button)

        # Save
        self.save_button = QtGui.QPushButton("Save")
        butt_win3.addRow(self.save_button)

        # Power Labels
        self.power_label = QtGui.QLabel()
        butt_win3.addRow(self.power_label)

        self.power_rms_label = QtGui.QLabel()
        butt_win3.addRow(self.power_rms_label)

        self.reactive_power_label = QtGui.QLabel()
        butt_win3.addRow(self.reactive_power_label)

        self.apparent_power_label = QtGui.QLabel()
        butt_win3.addRow(self.apparent_power_label)

        self.power_factor_label = QtGui.QLabel()
        butt_win3.addRow(self.power_factor_label)

        self.lead_lag_label = QtGui.QLabel()
        butt_win3.addRow(self.lead_lag_label)
        butt_win3.addRow(self.space_label)

        # Noise
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

        self.setGeometry(20, 50, 1200, 600)     # Sets the layout size

        win.addLayout(butt_win)                 # adds the windows to the main window
        win.addLayout(butt_win3)

        self.setLayout(win)                     # sets the main layout
        self.show()                             # displays the window
        print("init_ui complete!")

    
    def qt_connections(self):
        """Connects the logic of the buttons to their respective functions"""
        print("Connecting Buttons...")
        # Waveform 1
        self.edit_freq_box1.valueChanged.connect(self.edit_freq1)
        self.freq_unit_box1.currentIndexChanged.connect(self.freq_unit1)
        self.edit_amp_box1.valueChanged.connect(self.edit_amp1)
        self.amp_unit_box1.currentIndexChanged.connect(self.amp_unit1)
        self.edit_phase_box1.valueChanged.connect(self.edit_phase1)
        self.edit_offset_box1.valueChanged.connect(self.edit_offset1)
        self.offset_unit_box1.currentIndexChanged.connect(self.offset_unit1)
        self.color_box1.currentIndexChanged.connect(self.edit_color1)

        # Waveform 2
        self.edit_freq_box2.valueChanged.connect(self.edit_freq2)
        self.freq_unit_box2.currentIndexChanged.connect(self.freq_unit2)
        self.edit_amp_box2.valueChanged.connect(self.edit_amp2)
        self.amp_unit_box2.currentIndexChanged.connect(self.amp_unit2)
        self.edit_phase_box2.valueChanged.connect(self.edit_phase2)
        self.edit_offset_box2.valueChanged.connect(self.edit_offset2)
        self.offset_unit_box2.currentIndexChanged.connect(self.offset_unit2)
        self.color_box2.currentIndexChanged.connect(self.edit_color2)

        # Live/Timing menu
        self.edit_time_box.valueChanged.connect(self.edit_time)
        self.time_unit_box.currentIndexChanged.connect(self.edit_time_unit)
        self.save_button.clicked.connect(self.saveToFile)
        self.still_button.clicked.connect(self.still_toggle)
        self.pause_button.clicked.connect(self.pause_toggle)

        # Noise
        self.noise_button.clicked.connect(self.noise_toggle)
        self.rand_noise_box.valueChanged.connect(self.edit_noise)
        print("Buttons Complete!")
        

    def update(self):
        """Calls the function in the generator library"""
        generator.update(self)

    # Edits Variables using pop-up windows
    def edit_freq1(self):
        """Edits frquency1"""
        self.frequency1 = self.edit_freq_box1.value()

    def freq_unit1(self, i):
        """Sets the units for frequency1"""
        if i == 0:
            self.freq_scale1 = 1
        elif i == 1:
            self.freq_scale1 = 1000
        elif i == 2:
            self.freq_scale1 = 0.001
        else:
            self.freq_scale1 = 1

    def edit_amp1(self):
        """Edits amplitude1"""
        self.amplitude1 = self.edit_amp_box1.value()

    def amp_unit1(self, i):
        """Sets the units for amplitude1"""
        if i == 0:
            self.amp_scale1 = 1
        elif i == 1:
            self.amp_scale1 = 1000
        elif i == 2:
            self.amp_scale1 = 0.001
        else:
            self.amp_scale1 = 1

    def edit_phase1(self):
        """Edits phase1 in degrees""" 
        self.phase1 = self.edit_phase_box1.value()

    def edit_offset1(self):
        """Edits voltage offset1"""
        self.offset1 = self.edit_offset_box1.value()

    def offset_unit1(self, i):
        """Sets the units for offset1"""
        if i == 0:
            self.offset_scale1 = 1
        elif i == 1:
            self.offset_scale1 = 1000
        elif i == 2:
            self.offset_scale1 = 0.001
        else:
            self.offset_scale1 = 1
        #self.update()

    def edit_color1(self, i):
        """Edits color1"""
        if i == 0:
            self.color1 = 'r'
        elif i == 1:
            self.color1 = 'b'
        elif i == 2:
            self.color1 = 'g'
        else:
            self.color1 = 'w'
        #self.update()

    def edit_freq2(self):
        """Edits frequency2"""
        self.frequency2 = self.edit_freq_box2.value()

    def freq_unit2(self, i):
        """Sets the units for frequency2"""
        if i == 0:
            self.freq_scale2 = 1
        elif i == 1:
            self.freq_scale2 = 1000
        elif i == 2:
            self.freq_scale2 = 0.001
        else:
            self.freq_scale2 = 1

    def edit_amp2(self):
        """Edits amplitude2"""
        self.amplitude2 = self.edit_amp_box2.value()

    def amp_unit2(self, i):
        """Sets the units for amplitude2"""
        if i == 0:
            self.amp_scale2 = 1
        elif i == 1:
            self.amp_scale2 = 1000
        elif i == 2:
            self.amp_scale2 = 0.001
        else:
            self.amp_scale2 = 1

    def edit_phase2(self):
        """Edits phase2 in degrees"""
        self.phase2 = self.edit_phase_box2.value()

    def edit_offset2(self):
        """Edits voltage offset2"""
        self.offset2 = self.edit_offset_box2.value()

    def offset_unit2(self, i):
        """Sets units for offset2"""
        if i == 0:
            self.offset_scale2 = 1
        elif i == 1:
            self.offset_scale2 = 1000
        elif i == 2:
            self.offset_scale2 = 0.001
        else:
            self.offset_scale2 = 1

    def edit_color2(self, i):
        """Edits color2"""
        if i == 0:
            self.color2 = 'r'
        elif i == 1:
            self.color2 = 'b'
        elif i == 2:
            self.color2 = 'g'
        else:
            self.color2 = 'w'

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
            F.write(str(self.xs[i]) + "\t" + str(self.ys1[i]) + "\t" + str(self.ys2[i]) + "\n")
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

    def noise_toggle(self):
        """Toggle random noise"""
        self.noise = not self.noise

    def edit_noise(self):
        self.noise_magnitude = self.rand_noise_box.value()

def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Digital Wattmeter Simulator')
    ex = Plotter()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()