import numpy as np
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import pyqtgraph as pg
import sys
import math
import pc_plotter_live

class Waveform:
    def __init__(self, name, amplitude=1.0, amp_scale=1.0, frequency=1.0, freq_scale=1.0, offset=0.0, offset_scale=1.0, phase=0.0, color='w'):
        """Initializes Waveform object
        
        Arguments:
            name {str} -- Waveform name
        
        Keyword Arguments:
            amplitude {float} -- Amplitude of the waveform (default: {1.0})
            amp_scale {float} -- Units of amplitude (default: {1.0})
            frequency {float} -- Frequency of the waveform (default: {1.0})
            freq_scale {float} -- Units of frequency (default: {1.0})
            offset {float} -- Offset of waveform (default: {0.0})
            offset_scale {float} -- Units of offset (default: {1.0})
            phase {float} -- Phase angle in degrees (default: {0.0})
            color {str} -- Color of the waveform (default: {'w'})
        """
        self.name = name
        self.amplitude = amplitude
        self.amp_scale = amp_scale
        self.frequency = frequency
        self.freq_scale = freq_scale
        self.offset = offset
        self.offset_scale = offset_scale
        self.phase = phase
        self.color = color

        self.butt_win = QtGui.QFormLayout()

        # Name
        self.label = QtGui.QLabel(self.name)
        self.butt_win.addRow(self.label)

        # Frequency
        self.edit_freq_box = QtGui.QDoubleSpinBox()
        self.edit_freq_box.setValue(self.frequency)
        self.edit_freq_box.setGeometry(1,1,1,1) 
        self.edit_freq_box.setSingleStep(.1)
        self.edit_freq_box.setMaximum(1000)
        self.butt_win.addRow("Frequency", self.edit_freq_box)

        self.freq_unit_box = QtGui.QComboBox()
        self.freq_unit_box.addItems(["Hz", "kHz", "MHz"])
        self.butt_win.addRow(self.freq_unit_box)

        # Amplitude
        self.edit_amp_box = QtGui.QDoubleSpinBox()
        self.edit_amp_box.setValue(self.amplitude)
        self.edit_amp_box.setGeometry(1,1,1,1) 
        self.edit_amp_box.setSingleStep(.1)
        self.edit_amp_box.setRange(-1000, 1000)
        self.butt_win.addRow("Amplitude", self.edit_amp_box)

        self.amp_unit_box = QtGui.QComboBox()
        self.amp_unit_box.addItems(["V", "kV", "mV"])
        self.butt_win.addRow(self.amp_unit_box)

        # Phase
        self.edit_phase_box = QtGui.QDoubleSpinBox()
        self.edit_phase_box.setValue(self.phase)
        self.edit_phase_box.setGeometry(1,1,1,1) 
        self.edit_phase_box.setSingleStep(15)
        self.edit_phase_box.setRange(-360, 360)
        self.edit_phase_box.setWrapping(True)
        self.butt_win.addRow("Phase", self.edit_phase_box)

        # Offset
        self.edit_offset_box = QtGui.QDoubleSpinBox()
        self.edit_offset_box.setValue(self.offset)
        self.edit_offset_box.setGeometry(1,1,1,1) 
        self.edit_offset_box.setSingleStep(.1)
        self.edit_offset_box.setRange(-1000, 1000)
        self.butt_win.addRow("Offset", self.edit_offset_box)

        self.offset_unit_box = QtGui.QComboBox()
        self.offset_unit_box.addItems(["V", "kV", "mV"])
        self.butt_win.addRow(self.offset_unit_box)

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

    def qt_connections(self):
        """Connects the logic of the buttons to their respective functions"""
        print("Connecting Buttons...")
        # Waveform 1
        self.edit_freq_box.valueChanged.connect(self.edit_freq)
        self.freq_unit_box.currentIndexChanged.connect(self.freq_unit)
        self.edit_amp_box.valueChanged.connect(self.edit_amp)
        self.amp_unit_box.currentIndexChanged.connect(self.amp_unit)
        self.edit_phase_box.valueChanged.connect(self.edit_phase)
        self.edit_offset_box.valueChanged.connect(self.edit_offset)
        self.offset_unit_box.currentIndexChanged.connect(self.offset_unit)
        self.color_box.currentIndexChanged.connect(self.edit_color)

    def edit_freq(self):
        """Edits frquency"""
        self.frequency = self.edit_freq_box.value()

    def freq_unit(self, i):
        """Sets the units for frequency"""
        if i == 0:
            self.freq_scale = 1
        elif i == 1:
            self.freq_scale = 1000.0
        elif i == 2:
            self.freq_scale = 1000000
        else:
            self.freq_scale = 1

    def edit_amp(self):
        """Edits amplitude"""
        self.amplitude = self.edit_amp_box.value()

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

    def edit_phase(self):
        """Edits phase in degrees""" 
        self.phase = self.edit_phase_box.value()

    def edit_offset(self):
        """Edits voltage offset"""
        self.offset = self.edit_offset_box.value()

    def offset_unit(self, i):
        """Sets the units for offset"""
        if i == 0:
            self.offset_scale = 1
        elif i == 1:
            self.offset_scale = 1000
        elif i == 2:
            self.offset_scale = 0.001
        else:
            self.offset_scale = 1
        #self.update()

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