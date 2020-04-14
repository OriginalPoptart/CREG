import numpy as np
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import pyqtgraph as pg
import sys
import math
import pc_plotter_live

def update(self):
        """Updates the graph with the new waveform\n 
            Checks if paused or set to still mode\n
            If set to live, updates one screen-full per second"""
        # checks if user has the still image mode selected
        if(self.still):
            update_still(self)
        else:    
            if(not self.pause):     # only updates if not paused
                # Controls how fast the graph updates (One screen-full per second)
                if(time.time() - self.timer_thing > self.chunk_size/self.total_length*1.0): 
                    # First pass through creates one screen-full of data
                    if self.t < self.total_length:
                        for i in range(self.total_length):
                            self.xs[self.t] = (self.t / self.time_scale) * self.time_unit

                            self.ys1[self.t] = self.amplitude1 * self.amp_scale1 * np.sin(2*np.pi * self.frequency1 * self.freq_scale1 * (self.t/self.time_scale) * self.time_unit + (-2*self.phase2*np.pi/360)) + (self.offset1 * self.offset_scale1)
                            self.ys2[self.t] = self.amplitude2 * self.amp_scale2 * np.sin(2*np.pi * self.frequency2 * self.freq_scale2 * (self.t/self.time_scale) * self.time_unit + (-2*self.phase2*np.pi/360)) + (self.offset2 * self.offset_scale2)
                            #self.ysp[self.t] = self.ys1[self.t] * self.ys2[self.t]

                            self.t += 1
                        self.ys1 = add_rand_noise(self, self.ys1, self.noise_magnitude, self.noise)
                        self.ys2 = add_rand_noise(self, self.ys2, self.noise_magnitude, self.noise)
                        self.ysp = self.ys1 * self.ys2 

                    # Shifts data chunk_size positions to the left and adds chunk_size more data points at the end
                    else:
                        self.timer_thing = time.time() # Refreshes the timer 

                        # Shifts the data 
                        self.xs[:self.total_length-self.chunk_size] = self.xs[self.chunk_size:]
                        self.ys1[:self.total_length-self.chunk_size] = self.ys1[self.chunk_size:]
                        self.ys2[:self.total_length-self.chunk_size] = self.ys2[self.chunk_size:]
                        self.ysp[:self.total_length-self.chunk_size] = self.ysp[self.chunk_size:]

                        # Adds chunk_size more inputs to the end of the array
                        for i in range(self.chunk_size):
                            self.xs[self.total_length-self.chunk_size + i] = (self.t/self.time_scale) * self.time_unit 
                            self.ys1[self.total_length-self.chunk_size + i] = self.amplitude1 * self.amp_scale1 * np.sin(2*np.pi * self.frequency1 * self.freq_scale1 * (self.t/self.time_scale) * self.time_unit + (-2*self.phase1*np.pi/360)) + (self.offset1 * self.offset_scale2)
                            self.ys2[self.total_length-self.chunk_size + i] = self.amplitude2 * self.amp_scale2 * np.sin(2*np.pi * self.frequency2 * self.freq_scale2 * (self.t/self.time_scale) * self.time_unit + (-2*self.phase2*np.pi/360)) + (self.offset2 * self.offset_scale2)
                            
                            #self.ys1[:self.total_length - self.chunk_size] = self.add_rand_noise(self.ys1[:self.total_length - self.chunk_size], .005)
                            #self.ys2 = self.add_rand_noise(self.ys2, .005)
                            
                            self.ysp[self.total_length-self.chunk_size + i] = self.ys1[self.total_length-1] * self.ys2[self.total_length-1]

                            self.t += 1

                    self.ys1[self.total_length - self.chunk_size:] = add_rand_noise(self, self.ys1[self.total_length - self.chunk_size:], self.noise_magnitude, self.noise)
                    self.ys2[self.total_length - self.chunk_size:] = add_rand_noise(self, self.ys2[self.total_length - self.chunk_size:], self.noise_magnitude, self.noise)

                    # Adds the data to the graphs
                    self.plotcurve1.setData(self.xs, self.ys1, pen=self.color1, name="AD1")
                    self.plotcurve2.setData(self.xs, self.ys2, pen=self.color2, name="AD2")
                    self.powercurve1.setData(self.xs, self.ys1 * self.ys2, pen='r', name="Power")
                    update_label(self, np.average((self.ys1 * self.ys2)))
                #else:
                    #temp = 0
                    #print("Waiting...")

def update_still(self):
        """Updates plots for still mode"""
        #xs_still = np.linspace(0, 2*np.pi * self.total_length/self.time_scale, 360*(max(self.frequency1, self.frequency2*self.freq_scale2)))/(2*np.pi)
        xs_still = np.linspace(0, 2*np.pi * (self.total_length/self.time_scale) * self.time_unit, 36000)/(2*np.pi)
        
        ys1_still = self.amplitude1 * self.amp_scale1 * np.sin(2*np.pi * self.frequency1 * self.freq_scale1 * xs_still + (-2*self.phase1*np.pi/360)) + (self.offset1 * self.offset_scale1)
        ys2_still = self.amplitude2 * self.amp_scale2 * np.sin(2*np.pi * self.frequency2 * self.freq_scale2 * xs_still + (-2*self.phase2*np.pi/360)) + (self.offset2 * self.offset_scale2)

        ys1_still = add_rand_noise(self, ys1_still, self.noise_magnitude, self.noise)
        ys2_still = add_rand_noise(self, ys2_still, self.noise_magnitude, self.noise)

        self.plotcurve1.setData(xs_still, ys1_still, pen=self.color1, name="AD1")
        self.plotcurve2.setData(xs_still, ys2_still, pen=self.color2, name="AD2")
        self.powercurve1.setData(xs_still, ys1_still * ys2_still, pen='r', name="Power")
        #self.update_labels()

        update_label(self, np.average((ys1_still * ys2_still)))
        

def update_label(self, pwr):
    """Updates the labels for power
    
    Arguments:
        pwr {[float array]} -- [Power array read by the update function]
    """
    reactive_power = (((self.amplitude1+self.offset1)*(self.amplitude2+self.offset2)))/2 * np.sin(2*(self.phase2 - self.phase1)*np.pi/360)
    apparent_power = np.sqrt((pwr * pwr) + (reactive_power * reactive_power))
    power_factor = np.cos((self.phase2 -self.phase1)*2*np.pi/360)
    if((self.phase2 - self.phase1) == 0):
        self.lead_lag_label.setText("Unity")
    elif((self.phase2 - self.phase1) < 0):
        self.lead_lag_label.setText("Leading")
    elif((self.phase2 - self.phase1) > 0):
        self.lead_lag_label.setText("Lagging")

    self.power_label.setText("Real Power = %.3f W" %(pwr)) 
    self.power_rms_label.setText("Power RMS = %.3f W" %(pwr * (1/math.sqrt(2))))
    self.reactive_power_label.setText("Reactive Power = %.3f VAr" %(reactive_power))
    self.apparent_power_label.setText("Apparent Power = %.3f VA" %(apparent_power))
    self.power_factor_label.setText("Power Factor = %.4f " %(power_factor))
    

def add_rand_noise(self, arr, magnitude, switch=True):
    """Adds random noise using np.random
    
    Arguments:
        arr {float array} -- The array to add noise to
        magnitude {float} -- The range of random numbers

    Keyword Arguments:
        switch {boolean} -- Set to true if you want to add noise
    
    Returns:
        [float array] -- Returns new array
    """
    if switch:
        retval = arr + (np.random.rand(len(arr)) * magnitude) - magnitude/2
        return retval
    else:
        return arr