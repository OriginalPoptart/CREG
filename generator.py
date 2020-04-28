import numpy as np
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import pyqtgraph as pg
import sys
import math
import waveform
import Filter

#import pc_plotter_live

def update_label(self, rp):
    """Updates the labels for rp
    
    Arguments:
        rp {[float array]} -- [Power array read by the update function]
    """
    pwr = np.average(rp)
    fp = np.average(self.yf)
    reactive_power = (((self.waveform1.amplitude+self.waveform1.offset)*(self.waveform2.amplitude+self.waveform2.offset)))/2 * np.sin(2*(self.waveform2.phase - self.waveform1.phase)*np.pi/360)
    apparent_power = np.sqrt((pwr * pwr) + (reactive_power * reactive_power))
    power_factor = np.cos((self.waveform2.phase - self.waveform1.phase)*2*np.pi/360)
    
    self.power_label.setText("Real Power = %.3f W" %(pwr)) 
    self.power_rms_label.setText("Power RMS = %.3f W" %(pwr * (1/math.sqrt(2))))
    self.filtered_power_label.setText("Filtered = %.3f" %(fp))
    self.reactive_power_label.setText("Reactive Power = %.3f VAr" %(reactive_power))
    self.apparent_power_label.setText("Apparent Power = %.3f VA" %(apparent_power))
    self.power_factor_label.setText("Power Factor = %.4f " %(power_factor))
    
    # Power Factor Labels and Circuit Type 
    if((self.waveform2.phase - self.waveform1.phase) == 0):
        self.lead_lag_label.setText("Unity")
        self.circuit_type.setText("Purely Resistive Circuit")
    elif((self.waveform2.phase - self.waveform1.phase) < 0):
        self.lead_lag_label.setText("Leading")
        self.circuit_type.setText("Capacitive Circuit")
    elif((self.waveform2.phase - self.waveform1.phase) > 0):
        self.lead_lag_label.setText("Lagging")
        self.circuit_type.setText("Inductive Circuit")

def add_rand_noise(self, arr, magnitude, x, switchn=True, switchu=True):
    """Adds random noise using np.random
    
    Arguments:
        arr {float array} -- The array to add noise to
        magnitude {float} -- The range of random numbers
        x {float array} -- The x range for the uniform noise

    Keyword Arguments:
        switchn {boolean} -- Set to true if you want to add noise
    
    Returns:
        [float array] -- Returns new array
    """
    #x = np.linspace(0, 1, len(arr))
    retval = arr
    if switchn:
        retval += (np.random.rand(len(arr)) * magnitude) - magnitude/2# + add_sin_wave(x, 1, 1, 2, 1, 0)
    if switchu:
        noise = self.noiseform.y#[self.st*self.ms_scale:self.et*self.ms_scale] #+ sin_from_waveform(x, self.noiseform) + add_sin_wave(x, amp=self.noiseform.amplitude, freq=2*self.noiseform.frequency, amp_scl=self.noiseform.amp_scale, freq_scl=self.noiseform.freq_scale)
        retval += noise
    return retval
    

def add_sin_wave(x, amp=1, amp_scl=1, freq=1, freq_scl=1, offset=0, offset_scl=1, phase=0):
    """Adds a sin wave as uniform noise
    
    Arguments:
        x {array} -- x-axis to create waveform
        amp {float} -- amplitude of wave
        amp_scl {float} -- scaling units of amplitude
        freq {float} -- frequency of wave
        freq_scl {float} -- scaling units of frequency
        phase {float} -- phase angle in degrees from 0
    
    Returns:
        float array -- returns the sin wave from the function
    """
    return amp * amp_scl * np.sin(2*np.pi * freq * freq_scl * x + (2*phase*np.pi/360)) + (offset * offset_scl)

def sin_from_waveform(x, waveform_object):
    """Creates a sin wave from the Waveform object
    
    Arguments:
        x {float array} -- Array for the x-axis
        waveform_object {Waveform} -- Waveform object being used
    
    Returns:
        float array -- An array with the sin wave data that goes with given x
    """
    return add_sin_wave(x, waveform_object.amplitude, waveform_object.amp_scale, waveform_object.frequency/1000, waveform_object.freq_scale, waveform_object.offset, waveform_object.offset_scale, waveform_object.phase)

def updatePlots2(self, x, ys1, ys2):
    """Updates the waveforms

    Arguments:
        x {float array} -- x-axis for graphing
        ys1 {float array} -- first array
        ys2 {float array} -- second array
    """        

    self.ypp = ys1 * ys2
    y1, y2 = applyNoise(self, ys1, ys2)
    getPower(self, ys1, ys2)

    self.plotcurve1.setData(x[(self.st*self.ms_scale):(self.et*self.ms_scale)], y1[(self.st*self.ms_scale):(self.et*self.ms_scale)], pen=self.waveform1.color, name="AD1")
    self.plotcurve2.setData(x[(self.st*self.ms_scale):(self.et*self.ms_scale)], y2[(self.st*self.ms_scale):(self.et*self.ms_scale)], pen=self.waveform2.color, name="AD2")

    if(self.show_power):
        self.powercurve1.setData(self.x[(self.st*self.ms_scale):(self.et*self.ms_scale)], self.yp[(self.st*self.ms_scale):(self.et*self.ms_scale)], pen=self.colorp, name="Power")
    else:
        self.powercurve1.setData([],[])
    if(self.show_pure_power):
        self.powercurve2.setData(self.x[(self.st*self.ms_scale):(self.et*self.ms_scale)], self.ypp[(self.st*self.ms_scale):(self.et*self.ms_scale)], pen=self.colorpp, name="Pure Power")
    else:
        self.powercurve2.setData([],[])
    if(self.show_filtered_power):
        self.filtercurve.setData(self.x[(self.st*self.ms_scale):(self.et*self.ms_scale)], self.yf[(self.st*self.ms_scale):(self.et*self.ms_scale)], pen=self.colorfp)
    else:
        self.filtercurve.setData([],[])
    if(self.show_noise):
        self.noisecurve.setData(x[(self.st*self.ms_scale):(self.et*self.ms_scale)], self.noiseform.y[(self.st*self.ms_scale):(self.et*self.ms_scale)], pen=self.noiseform.color)
    else:
        self.noisecurve.setData([],[])

    update_label(self, self.yp)

    if(not self.pause):
        if(self.et < self.total_time):
            self.edit_time_box.setValue(self.st+self.speed)
            self.edit_time_box2.setValue(self.et+self.speed)
        else:
            self.pause = True
            self.pause_button.toggle()

def getPower(self, y1, y2):
    """Calculates power based on y1 and y2

    Arguments:
        y1 {float array} -- first waveform
        y2 {float array} -- second waveform
    """    
    self.yp = y1 * y2
    self.yf = Filter.filter(self.yp, self.ms_scale*1000, self.cutoff, self.order)

def applyNoise(self, y1, y2):
    """Adds noise to the given waveforms

    Arguments:
        y1 {float array} -- first waveform
        y2 {float array} -- second waveform

    Returns:
        floatarray, float array -- the new waveforms with noise
    """    
    new_y1 = y1
    new_y1 = add_rand_noise(self, new_y1, self.noise_magnitude, self.x, self.noise, self.unoise)
    new_y2 = y2
    new_y2 = add_rand_noise(self, new_y2, self.noise_magnitude, self.x, self.noise, self.unoise)
    return new_y1, new_y2