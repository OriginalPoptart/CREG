import numpy as np
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import pyqtgraph as pg
import sys
import math

class Plotter(QtGui.QWidget):
    # Initializes all element ins the system
    def __init__(self):
        super(Plotter, self).__init__()
        print("Starting init")
        self.total_length = 10000                   # total sample size
        self.time = 1000                           # time of sample in ms
        self.t = 0
        self.time_scale = 10000.0                   #samples per second, total time = total_length/time_scale
        self.chunk_size = 500
        self.time_unit = 1.0
        self.power = 0.0

        self.timer_thing = time.time()

        self.still = True
        self.pause = False

        #self.start_time = 

        self.amplitude1 = 1.0
        self.amp_scale1 = 1.0
        self.frequency1 = 1.0
        self.freq_scale1 = 1
        self.offset1 = 0.0
        self.offset_scale1 = 1.0
        self.phase1 = 0.0
        self.color1 = 'g'

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

        # Runs the update function on startup 
        #self.update()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1)
        print("init complete!")

    # Initializes all UI elements
    def init_ui(self):
        # Sets title and UI layout
        print("Starting init_ui")
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
        #butt_win3 = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom) 
        #butt_win2 = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom) 

        butt_win = QtGui.QFormLayout()
        butt_win2 = QtGui.QFormLayout()
        butt_win3 = QtGui.QFormLayout()

        # ** Column 1 **
        # Label
        self.label1 = QtGui.QLabel("Plot 1")
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

        # ** Column 2 **
        # Label
        self.label2 = QtGui.QLabel("Plot 2")
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

        # ** Column 3 **
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

        # Power Label
        self.power_label = QtGui.QLabel()
        butt_win3.addRow(self.power_label)

        self.power_rms_label = QtGui.QLabel()
        butt_win3.addRow(self.power_rms_label)

        self.apparent_power_label = QtGui.QLabel()
        butt_win3.addRow(self.apparent_power_label)

        self.reactive_power_label = QtGui.QLabel()
        butt_win3.addRow(self.reactive_power_label)

        self.setGeometry(20, 50, 1200, 600)     # Sets the layout

        win.addLayout(butt_win)                 # adds the button window to the main window
        #win.addLayout(butt_win2)
        win.addLayout(butt_win3)

        self.setLayout(win)                     # sets the main layout
        self.show()                             # displays the window
        print("init_ui complete!")

    # Connects the logic of the buttons to their respective functions
    def qt_connections(self):
        print("Connecting Buttons...")
        self.edit_freq_box1.valueChanged.connect(self.edit_freq1)
        self.freq_unit_box1.currentIndexChanged.connect(self.freq_unit1)
        self.edit_amp_box1.valueChanged.connect(self.edit_amp1)
        self.amp_unit_box1.currentIndexChanged.connect(self.amp_unit1)
        self.edit_phase_box1.valueChanged.connect(self.edit_phase1)
        self.edit_offset_box1.valueChanged.connect(self.edit_offset1)
        self.offset_unit_box1.currentIndexChanged.connect(self.offset_unit1)
        self.color_box1.currentIndexChanged.connect(self.edit_color1)

        #self.edit_freq_button2.clicked.connect(self.edit_freq2)
        self.edit_freq_box2.valueChanged.connect(self.edit_freq2)
        self.freq_unit_box2.currentIndexChanged.connect(self.freq_unit2)
        self.edit_amp_box2.valueChanged.connect(self.edit_amp2)
        self.amp_unit_box2.currentIndexChanged.connect(self.amp_unit2)
        self.edit_phase_box2.valueChanged.connect(self.edit_phase2)
        self.edit_offset_box2.valueChanged.connect(self.edit_offset2)
        self.offset_unit_box2.currentIndexChanged.connect(self.offset_unit2)
        self.color_box2.currentIndexChanged.connect(self.edit_color2)

        self.edit_time_box.valueChanged.connect(self.edit_time)
        self.time_unit_box.currentIndexChanged.connect(self.edit_time_unit)
        self.save_button.clicked.connect(self.saveToFile)
        self.still_button.clicked.connect(self.still_toggle)
        self.pause_button.clicked.connect(self.pause_toggle)
        print("Buttons Complete!")
        

    # Updates the graph with the new waveform
    def update(self):
        #print("Updating...")
        if(self.still):
            self.update_still()
        else:    
            if(not self.pause):
                if(time.time() - self.timer_thing > self.chunk_size/self.total_length*1.0):
                    if self.t < self.total_length:
                        for i in range(self.total_length):
                            self.xs[self.t] = (self.t / self.time_scale) * self.time_unit

                            self.ys1[self.t] = self.amplitude1 * self.amp_scale1 * np.sin(2*np.pi * self.frequency1 * self.freq_scale1 * (self.t/self.time_scale) * self.time_unit + (-2*self.phase2*np.pi/360)) + (self.offset1 * self.offset_scale1)
                            self.ys2[self.t] = self.amplitude2 * self.amp_scale2 * np.sin(2*np.pi * self.frequency2 * self.freq_scale2 * (self.t/self.time_scale) * self.time_unit + (-2*self.phase2*np.pi/360)) + (self.offset2 * self.offset_scale2)
                            self.ysp[self.t] = self.ys1[self.t] * self.ys2[self.t]

                            self.t += 1
                    else:
                        self.timer_thing = time.time()
                        self.xs[:self.total_length-self.chunk_size] = self.xs[self.chunk_size:]
                        self.ys1[:self.total_length-self.chunk_size] = self.ys1[self.chunk_size:]
                        self.ys2[:self.total_length-self.chunk_size] = self.ys2[self.chunk_size:]
                        self.ysp[:self.total_length-self.chunk_size] = self.ysp[self.chunk_size:]
                        for i in range(self.chunk_size):
                            self.xs[self.total_length-self.chunk_size + i] = (self.t/self.time_scale) * self.time_unit
                            self.ys1[self.total_length-self.chunk_size + i] = self.amplitude1 * self.amp_scale1 * np.sin(2*np.pi * self.frequency1 * self.freq_scale1 * (self.t/self.time_scale) * self.time_unit + (-2*self.phase1*np.pi/360)) + (self.offset1 * self.offset_scale2)
                            self.ys2[self.total_length-self.chunk_size + i] = self.amplitude2 * self.amp_scale2 * np.sin(2*np.pi * self.frequency2 * self.freq_scale2 * (self.t/self.time_scale) * self.time_unit + (-2*self.phase2*np.pi/360)) + (self.offset2 * self.offset_scale2)
                            self.ysp[self.total_length-self.chunk_size + i] = self.ys1[self.total_length-1] * self.ys2[self.total_length-1]

                            self.t += 1

                    self.plotcurve1.setData(self.xs, self.ys1, pen=self.color1, name="AD1")
                    self.plotcurve2.setData(self.xs, self.ys2, pen=self.color2, name="AD2")
                    self.powercurve1.setData(self.xs, self.ys1 * self.ys2, pen='r', name="Power")
                    self.update_labels(np.average((self.ys1 * self.ys2)))


    def update_still(self):
        #xs_still = np.linspace(0, 2*np.pi * self.total_length/self.time_scale, 360*(max(self.frequency1, self.frequency2*self.freq_scale2)))/(2*np.pi)
        xs_still = np.linspace(0, 2*np.pi * (self.total_length/self.time_scale) * self.time_unit, 36000)/(2*np.pi)
        
        ys1_still = self.amplitude1 * self.amp_scale1 * np.sin(2*np.pi * self.frequency1 * self.freq_scale1 * xs_still + (-2*self.phase1*np.pi/360)) + (self.offset1 * self.offset_scale1)
        ys2_still = self.amplitude2 * self.amp_scale2 * np.sin(2*np.pi * self.frequency2 * self.freq_scale2 * xs_still + (-2*self.phase2*np.pi/360)) + (self.offset2 * self.offset_scale2)

        self.plotcurve1.setData(xs_still, ys1_still, pen=self.color1, name="AD1")
        self.plotcurve2.setData(xs_still, ys2_still, pen=self.color2, name="AD2")
        self.powercurve1.setData(xs_still, ys1_still * ys2_still, pen='r', name="Power")
        #self.update_labels()

        self.update_labels(np.average((ys1_still * ys2_still)))
        #self.power_label.setText("Average Power = " + '%.3f'%(np.average((ys1_still * ys2_still))) + " W") 
        #self.power_rms_label.setText("Power RMS = %.3f W" %(np.average((ys1_still * ys2_still)) * (1/math.sqrt(2))))
        #if(self.phase1 == self.phase2):
            #self.apparent_power_label.setText("Apparent Power = %.3f VA" %(np.average((ys1_still * ys2_still)) ))
        #else:
        #self.apparent_power_label.setText("Apparent Power = %.3f VA" %(np.average((ys1_still * ys2_still))/np.cos(2*(self.phase2 - self.phase1)*np.pi/360)))

    def update_labels(self, pwr):
        reactive_power = (((self.amplitude1+self.offset1)*(self.amplitude2+self.offset2)))/2 * np.sin(2*(self.phase2 - self.phase1)*np.pi/360)
        apparent_power = np.sqrt((pwr * pwr) + (reactive_power * reactive_power))
        self.power_label.setText("True Power = %.3f W" %(pwr)) 
        self.power_rms_label.setText("Power RMS = %.3f W" %(pwr * (1/math.sqrt(2))))
        self.reactive_power_label.setText("Reactive Power = %.3f VAr" %(reactive_power))
        self.apparent_power_label.setText("Apparent Power = %.3f VA" %(apparent_power))


    # Edits Variables using pop-up windows
    def edit_freq1(self):
        self.frequency1 = self.edit_freq_box1.value()
        #self.update()

    def freq_unit1(self, i):
        if i == 0:
            self.freq_scale1 = 1
        elif i == 1:
            self.freq_scale1 = 1000
        elif i == 2:
            self.freq_scale1 = 0.001
        else:
            self.freq_scale1 = 1
        #self.update()

    def edit_amp1(self):
        self.amplitude1 = self.edit_amp_box1.value()
        #self.update()

    def amp_unit1(self, i):
        if i == 0:
            self.amp_scale1 = 1
        elif i == 1:
            self.amp_scale1 = 1000
        elif i == 2:
            self.amp_scale1 = 0.001
        else:
            self.amp_scale1 = 1
        #self.update()

    def edit_phase1(self):
        self.phase1 = self.edit_phase_box1.value()
        #self.update()

    def edit_offset1(self):
        self.offset1 = self.edit_offset_box1.value()
        #self.update()

    def offset_unit1(self, i):
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
        self.frequency2 = self.edit_freq_box2.value()
        #self.update()

    def freq_unit2(self, i):
        if i == 0:
            self.freq_scale2 = 1
        elif i == 1:
            self.freq_scale2 = 1000
        elif i == 2:
            self.freq_scale2 = 0.001
        else:
            self.freq_scale2 = 1
        #self.update()

    def edit_amp2(self):
        self.amplitude2 = self.edit_amp_box2.value()
        #self.update()

    def amp_unit2(self, i):
        if i == 0:
            self.amp_scale2 = 1
        elif i == 1:
            self.amp_scale2 = 1000
        elif i == 2:
            self.amp_scale2 = 0.001
        else:
            self.amp_scale2 = 1
        #self.update()

    def edit_phase2(self):
        self.phase2 = self.edit_phase_box2.value()
        #self.update()

    def edit_offset2(self):
        self.offset2 = self.edit_offset_box2.value()
        #self.update()

    def offset_unit2(self, i):
        if i == 0:
            self.offset_scale2 = 1
        elif i == 1:
            self.offset_scale2 = 1000
        elif i == 2:
            self.offset_scale2 = 0.001
        else:
            self.offset_scale2 = 1
        #self.update()

    def edit_color2(self, i):
        if i == 0:
            self.color2 = 'r'
        elif i == 1:
            self.color2 = 'b'
        elif i == 2:
            self.color2 = 'g'
        else:
            self.color2 = 'w'
        #self.update()

    def edit_time(self):
        self.time_scale = self.total_length / self.edit_time_box.value()
        self.total_time = self.total_length/self.time_scale
        #self.update()

    def edit_time_unit(self, i):
        if i == 0:
            self.time_unit = 1.0
        elif i == 1:
            self.time_unit = .001
        elif i == 2:
            self.time_unit = .000001
        else:
            self.time_unit = 1

    # Writes the data into the save file
    def saveToFile(self):
        F = open("data", "w")
        for i in range (self.total_length):
            F.write(str(self.xs[i]) + "\t" + str(self.ys1[i]) + "\t" + str(self.ys2[i]) + "\n")
        F.close()
        print("Saving to data file")

    def still_toggle(self):
        self.still = not self.still
        if(self.still):
            self.t = 0
            self.still_button.setText("Still")
        else:
            self.still_button.setText("Live")
            self.timer_thing = time.time()

    def pause_toggle(self):
        self.pause = not self.pause

    def print_details(self):
        print("Bruh")

def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Test')
    ex = Plotter()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()