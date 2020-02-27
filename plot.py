import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import ADS1256 as adc
import time
from subprocess import call
from scipy.signal import find_peaks


x_len = 10
y_range = [0, 1]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)   #Current
#ax2 = fig.add_subplot(2, 1, 2)  #Voltage

power = adc.ADS1256()
power.ADS1256_init()    

total_length = 200

xs = [0] * (total_length)
ys0 = [0] * (total_length)
ys1 = [0] * (total_length)
ys2 = [0] * (total_length)

numberOfTests = 1
times = [0] * numberOfTests

#for j in range(numberOfTests):
begin = time.time()

for i in range(total_length):
    #ys0[i] = (power.getValueAtPin(0)*5.0/0x7fffff)      #50 is our conversion factor for current
    ys1[i] = (power.getValueAtPin(0)*5.0/0x7fffff)
    ys2[i] = (power.getValueAtPin(2)*5.0/0x7fffff)
    #ys1[i] = (power.getValueAtPin(1)*5.0/0x7fffff)      
    xs[i] = (time.time()-begin)

#ys[0] = 2.5

end = time.time()

    #times [j] = end - begin

totalTime = end-begin

print(total_length," samples taken over ", totalTime, " seconds")
print(total_length/totalTime, " samples per second")
#print("Average samples per second = ", sum(times)/numberOfTests)

F = open("data", "w")
for i in range (total_length):
    F.write(str(xs[i]) + "\t" + str(ys0[i]) + "\t" + str(ys1[i]) + "\t" + str(ys2[i]) + "\n")
F.close()

peaks, _ = find_peaks(ys2, height = 1, distance = 10)
peaks2, _ = find_peaks(ys1, height = 1, distance = 10)

p1 = []
p2 = []
for i in peaks:
    p1.append(xs[i])

for i in peaks2:
    p2.append(xs[i])

period1 = np.average(np.diff(p1))
period2 = np.average(np.diff(p2))
print("Average Period1: ", period1, "sec Frequency1: ", 1.0/(period1*1.0), "Hz")
print("Average Period2: ", period2, "sec Frequency2: ", 1.0/(period2*1.0), "Hz")


plt.title("Power")
plt.xlabel("Time")
plt.ylabel("Watts")

p = [0] * total_length 
for i in range(total_length):
    p[i] = ys2[i] * ys1[i]

phase = ((p2[1]-p1[1])/period1) * 360 
print(phase)

#hold on
ax.plot(xs, ys2, label="AD2", color="blue")
for i in peaks:
    ax.plot(xs[i], ys2[i], 'x', color="orange")
#ax.plot(p1, ys0[p1], 'x', color="orange")
#ax.plot(xs, ys1, label="AD0")
ax.plot(xs, ys1, label="AD1", color="red")
for i in peaks2:
    ax.plot(xs[i], ys1[i], 'x', color="green")
#ax.plot(xs, p, label="AD2 * AD1", color="gray")
#ax2.plot(xs, ys1)
ax.legend()
#hold off
begin_plot = time.time()
plt.show()
print(time.time() - begin_plot)