import numpy as np
import ADS1256 as adc
import time
from subprocess import call
from scipy.signal import find_peaks
#from PyQt4 import QtGui
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys

class Plotter(QtGui.QWidget):
    def __init__(self):
        super(Plotter, self).__init__()
        self.init_ui()
        self.qt_connections()
        self.plotcurve2 = pg.PlotCurveItem()
        self.plotcurve3 = pg.PlotCurveItem()
        self.plotwidget.addItem(self.plotcurve2)
        self.plotwidget.addItem(self.plotcurve3)        

        self.power = adc.ADS1256()
        self.power.ADS1256_init() 

        self.total_length = 200

        self.peak = 0
        self.xs = [0] * self.total_length
        self.ys0 = [0] * self.total_length
        self.ys1 = [0] * self.total_length
        self.ys2 = [0] * self.total_length
        self.ys3 = [0] * self.total_length

        self.pause = False
        self.autoSet = False

        self.update()
        self.calibrate()

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def init_ui(self):
        self.setWindowTitle('Plotter')
        win = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        
        self.plotwidget = pg.PlotWidget()
        win.addWidget(self.plotwidget)
        #self.combo = pg.ComboBox()
        #win.addWidget(self.combo)
        butt_win = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)        

        self.pauseButton = QtGui.QPushButton("Pause/Play")
        self.autoSetButton = QtGui.QPushButton("Autoset")
        self.calibrateButton = QtGui.QPushButton("Calibrate")
        self.saveButton = QtGui.QPushButton("Save")

        butt_win.addWidget(self.pauseButton)
        butt_win.addWidget(self.autoSetButton)
        butt_win.addWidget(self.calibrateButton)
        butt_win.addWidget(self.saveButton)

        self.setGeometry(20, 50, 1000, 600)

        win.addLayout(butt_win)

        self.setLayout(win)
        self.show()

    def qt_connections(self):
        self.pauseButton.clicked.connect(self.on_pauseButton_clicked)
        self.autoSetButton.clicked.connect(self.on_autoSetButton_clicked)
        self.calibrateButton.clicked.connect(self.calibrate)
        self.saveButton.clicked.connect(self.saveToFile)

    def update(self):
    
        if(not self.pause):
            
            if self.autoSet:
                timeout = 0

                while(True):
                    temp = (self.power.getValueAtPin(3)*5.0/0x7fffff)
                    if(temp > (self.peak * 0.99)):
                        break
                    timeout+=1
                    if timeout >= self.total_length:
                        print("Autoset Timeout")
                        self.autoSet = False
                        break

            begin = time.time()

            for i in range(self.total_length):
                #ys0[i] = (power.getValueAtPin(0)*5.0/0x7fffff)      #50 is our conversion factor for current
                #ys1[i] = (power.getValueAtPin(1)*5.0/0x7fffff)
                self.ys2[i] = (self.power.getValueAtPin(2)*5.0/0x7fffff)
                self.ys3[i] = self.power.getValueAtPin(3)*5.0/0x7fffff    
                self.xs[i] = time.time()-begin

            #curve0.setData(xs,ys0)
            #curve1.setData(xs, ys1)
            #curve2.setData(xs, ys2)
            #curve3.setData(xs, ys3)
            self.plotcurve2.setData(self.xs, self.ys2, pen='w', name='AD2')
            self.plotcurve3.setData(self.xs, self.ys3, pen='g', name='AD3')

    def on_pauseButton_clicked(self):
        print("Click")
        self.pause = not self.pause

    def on_autoSetButton_clicked(self):
        self.autoSet = not self.autoSet
        if self.autoSet:
            print("Autoset is now on")
        else:
            print("Autoset is now off")

    def calibrate(self):
        begin = time.time()

        for i in range(self.total_length):
            #ys0[i] = (power.getValueAtPin(0)*5.0/0x7fffff)      #50 is our conversion factor for current
            #ys1[i] = (power.getValueAtPin(1)*5.0/0x7fffff)
            self.ys2[i] = self.power.getValueAtPin(2)*5.0/0x7fffff
            self.ys3[i] = self.power.getValueAtPin(3)*5.0/0x7fffff    
            self.xs[i] = time.time()-begin

        peaks, _ = find_peaks(self.ys3, distance = 20)
        #ysi3 = [-i for i in self.ys3]
        #trough, _ = find_peaks(ysi3, distance = 10)
        peaks2, _ = find_peaks(self.ys2, height = 1, distance = 10)

        p2x = []
        p3x = []
        p2y = []
        p3y = []
        for i in peaks:
            p3y.append(self.ys3[i])
            p3x.append(self.xs[i])

        #for i in trough:
            #p3.append(-ysi3[i])

        self.peak = np.average(p3y)
        print("----------")
        print("Average Peak:", self.peak)

        #print("Peaks: ", p3)

        for i in peaks2:
            p2y.append(self.ys2[i])
            p2x.append(self.xs[i])

        period1 = np.average(np.diff(p3x))
        period2 = np.average(np.diff(p2x))
        print("Average Period1: ", period1, "sec Frequency1: ", 1.0/(period1*1.0), "Hz")
        print("Average Period2: ", period2, "sec Frequency2: ", 1.0/(period2*1.0), "Hz")

        ph = []
        for i in range(min(len(p3x), len(p2x))):
            ph.append((p2x[i] - p3x[i])/period1)

        phase = np.average(ph) * 360
        if phase < 0:
            phase += 360
        #p = [0] * total_length 
        #for i in range(total_length):
            #p[i] = ys2[i] * ys3[i]

        #phase = ((self.xs[peaks[1]]-self.xs[peaks2[1]])/period1) * 360 
        print("Phase =", phase, "degrees")

    def saveToFile(self):
        F = open("data", "w")
        for i in range (self.total_length):
            F.write(str(self.xs[i]) + "\t" + str(self.ys3[i]) + "\n")
        F.close()
        print("Saving to data file")

def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Test')
    ex = Plotter()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()