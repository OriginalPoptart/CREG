import numpy as np
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import pyqtgraph as pg
import sys
import math
import pc_plotter_live
import generator
import waveform

class Noiseform:
    def __init__(self, name, amplitude=1.0, amp_scale=1.0, frequency=1.0, freq_scale=1.0, phase=0.0, color='w', time=5000, samp_per_msec=10):
        """Initializes Waveform object
        
        Arguments:
            name {str} -- Waveform name
        
        Keyword Arguments:
            amplitude {float} -- Amplitude of the waveform (default: {1.0})
            amp_scale {float} -- Units of amplitude (default: {1.0})
            frequency {float} -- Frequency of the waveform (default: {1.0})
            freq_scale {float} -- Units of frequency (default: {1.0})
            phase {float} -- Phase angle in degrees (default: {0.0})
            color {str} -- Color of the waveform (default: {'w'})
            time {int} -- Length of sample time in ms
            samp_per_msec {int} -- samples per millisecond
        """
        self.name = name
        self.amplitude = amplitude
        self.amp_scale = amp_scale
        self.frequency = frequency
        self.freq_scale = freq_scale
        self.phase = phase
        self.color = color
        self.time = time
        self.samp_per_msec = samp_per_msec
        self.harmonic = 2

        #self.plotcurve = pg.PlotCurveItem()
        self.x = np.linspace(0, time, time*samp_per_msec)
        self.y = self.amplitude * self.amp_scale * np.sin(2*np.pi * self.frequency/1000 * self.freq_scale * self.x + (2*self.phase*np.pi/360))
        self.y += self.amplitude * self.amp_scale * np.sin(2*np.pi * self.harmonic * self.frequency/1000 * self.freq_scale * self.x + (2*self.phase*np.pi/360))

        self.butt_win = QtGui.QFormLayout()

        # Name
        self.label = QtGui.QLabel(self.name)
        self.butt_win.addRow(self.label)

        # Frequency
        self.edit_freq_box = QtGui.QDoubleSpinBox()
        self.edit_freq_box.setMaximum(1000)
        self.edit_freq_box.setValue(self.frequency)
        self.edit_freq_box.setGeometry(1,1,1,1) 
        self.edit_freq_box.setSingleStep(1)
        self.butt_win.addRow("Frequency", self.edit_freq_box)

        self.freq_unit_box = QtGui.QComboBox()
        self.freq_unit_box.addItems(["Hz", "kHz", "MHz"])
        if(freq_scale == 1000):
            self.freq_unit_box.setCurrentIndex(1)
        self.butt_win.addRow(self.freq_unit_box)

        # Amplitude
        self.edit_amp_box = QtGui.QDoubleSpinBox()
        self.edit_amp_box.setRange(-1000, 1000)
        self.edit_amp_box.setValue(self.amplitude)
        self.edit_amp_box.setGeometry(1,1,1,1) 
        self.edit_amp_box.setSingleStep(.1)
        self.butt_win.addRow("Amplitude", self.edit_amp_box)

        self.amp_unit_box = QtGui.QComboBox()
        self.amp_unit_box.addItems(["V", "kV", "mV"])
        if(amp_scale == .001):
            self.amp_unit_box.setCurrentIndex(2)
        self.butt_win.addRow(self.amp_unit_box)

        # Phase
        self.edit_phase_box = QtGui.QDoubleSpinBox()
        self.edit_phase_box.setRange(-360, 360)
        self.edit_phase_box.setValue(self.phase)
        self.edit_phase_box.setGeometry(1,1,1,1) 
        self.edit_phase_box.setSingleStep(15)
        self.edit_phase_box.setWrapping(True)
        self.butt_win.addRow("Phase", self.edit_phase_box)

        self.edit_harmonic_box = QtGui.QSpinBox()
        self.edit_harmonic_box.setMaximum(1000)
        self.edit_harmonic_box.setValue(self.harmonic)
        self.edit_harmonic_box.setGeometry(1,1,1,1) 
        self.butt_win.addRow("Harmonic", self.edit_harmonic_box)

        # Color
        self.color_box = QtGui.QComboBox()
        self.color_box.addItems(["Red", "Blue", "Green", "Yellow", "White", "None"])
        if(self.color == 'r'):
            self.color_box.setCurrentIndex(0)
        elif(self.color == 'b'):
            self.color_box.setCurrentIndex(1)
        elif(self.color == 'g'):
            self.color_box.setCurrentIndex(2)
        elif(self.color == 'y'):
            self.color_box.setCurrentIndex(3)
        elif(self.color == 'w'):
            self.color_box.setCurrentIndex(4)
        else:
            self.color_box.serCurrentIndex(5)
        self.butt_win.addRow("Color", self.color_box)

        #self.space_label = QtGui.QLabel(" ")
        #self.butt_win.addRow(self.space_label)

        self.qt_connections()

    def set_data(self):
        #self.y = generator.sin_from_waveform(self.x, self) 
        self.y = self.amplitude * self.amp_scale * np.sin(2*np.pi * self.frequency/1000 * self.freq_scale * self.x + (2*self.phase*np.pi/360))
        self.y += self.amplitude * self.amp_scale * np.sin(2*np.pi * self.harmonic * self.frequency/1000 * self.freq_scale * self.x + (2*self.phase*np.pi/360))

    def qt_connections(self):
        """Connects the logic of the buttons to their respective functions"""
        print("Connecting Buttons...")
        # Waveform 1
        self.edit_freq_box.valueChanged.connect(self.edit_freq)
        self.freq_unit_box.currentIndexChanged.connect(self.freq_unit)
        self.edit_amp_box.valueChanged.connect(self.edit_amp)
        self.amp_unit_box.currentIndexChanged.connect(self.amp_unit)
        self.edit_phase_box.valueChanged.connect(self.edit_phase)
        self.color_box.currentIndexChanged.connect(self.edit_color)
        self.edit_harmonic_box.valueChanged.connect(self.edit_harmonic)

    def edit_freq(self):
        """Edits frquency"""
        self.frequency = self.edit_freq_box.value()
        self.set_data()

    def freq_unit(self, i):
        """Sets the units for frequency"""
        if i == 0:
            self.freq_scale = 1.0
        elif i == 1:
            self.freq_scale = 1000.0
        elif i == 2:
            self.freq_scale = 1000000.0
        else:
            self.freq_scale = 1
        self.set_data()

    def edit_amp(self):
        """Edits amplitude"""
        self.amplitude = self.edit_amp_box.value()
        self.set_data()

    def amp_unit(self, i):
        """Sets the units for amplitude"""
        if i == 0:
            self.amp_scale = 1
        elif i == 1:
            self.amp_scale = 1000
        elif i == 2:
            self.amp_scale = 0.001
        else:
            self.amp_scale = 1
        self.set_data()

    def edit_phase(self):
        """Edits phase in degrees""" 
        self.phase = self.edit_phase_box.value()
        self.set_data()

    def edit_harmonic(self):
        """Edits harmonics"""
        self.harmonic = self.edit_harmonic_box.value()
        self.set_data()

    def edit_color(self, i):
        """Edits color"""
        if i == 0:
            self.color = 'r'
        elif i == 1:
            self.color = 'b'
        elif i == 2:
            self.color = 'g'
        elif i == 3:
            self.color = 'y'
        elif i == 4:
            self.color = 'w'
        else:
            self.color = None