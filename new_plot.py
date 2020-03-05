import numpy as np
import ADS1256 as adc
import time
from subprocess import call
from scipy.signal import find_peaks
#from PyQt4 import QtGui
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

x_len = 10
y_range = [0, 1]

power = adc.ADS1256()
power.ADS1256_init()    

total_length = 100

xs = [0] * (total_length)
ys0 = [0] * (total_length)
ys1 = [0] * (total_length)
ys2 = [0] * (total_length)
ys3 = [0] * (total_length)

begin = time.time()

for i in range(total_length):
    ys0[i] = (power.getValueAtPin(0)*5.0/0x7fffff)      #50 is our conversion factor for current
    ys1[i] = (power.getValueAtPin(1)*5.0/0x7fffff)
    ys2[i] = (power.getValueAtPin(2)*5.0/0x7fffff)
    ys3[i] = (power.getValueAtPin(3)*5.0/0x7fffff)      
    xs[i] = (time.time()-begin)

end = time.time()

totalTime = end-begin

print(total_length," samples taken over ", totalTime, " seconds")
print(total_length/totalTime, " samples per second")

#F = open("data", "w")
#for i in range (total_length):
#    F.write(str(xs[i]) + "\t" + str(ys0[i]) + "\t" + str(ys1[i]) + "\t" + str(ys2[i]) + "\n")
#F.close()

peaks, _ = find_peaks(ys2, height = 1, distance = 10)
ysi2 = [-i for i in ys2]
trough, _ = find_peaks(ysi2, distance = 10)
peaks2, _ = find_peaks(ys3, height = 1, distance = 10)

p1 = []
p2 = []
p3 = []
for i in peaks:
    p1.append(xs[i])

for i in trough:
    p3.append(-ysi2[i])

print("Peaks: ", p3)

for i in peaks2:
    p2.append(xs[i])

period1 = np.average(np.diff(p1))
period2 = np.average(np.diff(p2))
print("Average Period1: ", period1, "sec Frequency1: ", 1.0/(period1*1.0), "Hz")
print("Average Period2: ", period2, "sec Frequency2: ", 1.0/(period2*1.0), "Hz")

p = [0] * total_length 
for i in range(total_length):
    p[i] = ys2[i] * ys3[i]

phase = ((p2[1]-p1[1])/period1) * 360 
print("Phase =", phase, "degrees")

###########################################

win = pg.GraphicsLayoutWidget(show=True, size=(1200,600))
win.setWindowTitle('Proof of Concept')

#plt = pg.plot(ys2, title="Test", pen='r')
#plt.showGrid(x=True, y=True)
plt1 = win.addPlot()
plt2 = win.addPlot()
plt1.setLabel('bottom', 'Time', 's')
plt2.setLabel('bottom', 'Time', 's')

plt1.setRange(xRange=[0,.15], yRange=[0,4])
plt1.showGrid(x=True, y=True)

plt1.setDownsampling(mode="peak")
plt1.setClipToView(True)
plt2.setDownsampling(mode="peak")
still1 = plt2.plot(xs, ys3, title="Still", pen='g')
still2 = plt2.plot(xs, ys2)

curve0 = plt1.plot(xs, ys0, title="Test", pen='r')
curve1 = plt1.plot(xs, ys1, title="Test", pen='g')
curve2 = plt1.plot(xs, ys2, title="Test", pen='w')
curve3 = plt1.plot(xs, ys3, title="Test", pen='b')

def update():

    temp = 0
    
    while(True):
        temp = (power.getValueAtPin(3)*5.0/0x7fffff)
        if(temp > 3.97):
            break

    begin = time.time()

    for i in range(total_length):
        ys0[i] = (power.getValueAtPin(0)*5.0/0x7fffff)      #50 is our conversion factor for current
        ys1[i] = (power.getValueAtPin(1)*5.0/0x7fffff)
        ys2[i] = (power.getValueAtPin(2)*5.0/0x7fffff)
        ys3[i] = (power.getValueAtPin(3)*5.0/0x7fffff)      
        xs[i] = (time.time()-begin)

    curve0.setData(xs,ys0)
    curve1.setData(xs, ys1)
    curve2.setData(xs, ys2)
    curve3.setData(xs, ys3)
    #end = time.time()
    #plt = pg.plot(ys2, title="Test", pen='r')

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.instance().exec_()

#app = QtGui.QApplication([])
#w = QtGui.QWidget()

#plot = pg.PlotWidget()
#plot.plotItem.plot(xs, ys0)

#w.show()
#app.exec_()
#win = pg.GraphicsWindow(title="Window Test")
#p = win.addPlot(title="Plot Test")
#curve = p.plot()

#curve.setData(ys0)
#app.processEvents()

#pg.app.exec_()
#pg.plot(xs, ys0)