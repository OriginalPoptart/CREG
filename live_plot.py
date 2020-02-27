import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import ADS1256 as adc
import time
from subprocess import call


x_len = 150
y_range = [0, 1]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
#ax2 = fig.add_subplot(2, 1, 1)
xs = list(range(0, x_len))
ys = [0] * x_len
ax.set_ylim(y_range)

line, = ax.plot(xs, ys)

power = adc.ADS1256()
power.ADS1256_init()    

def animate(i, ys):

    ys.append(power.getValueAtPin(0)*1.0/0x7fffff)
    ys = ys[-x_len:]

    line.set_ydata(ys)

    return line,

ani = animation.FuncAnimation(fig, animate, fargs=(ys,), interval=0, blit=True)
plt.show()