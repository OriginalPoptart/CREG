import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import ADC_Code/ADS1256 as adc

x_len = 100
y_range = [-10, 265]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, x_len))
ys = [0] * x_len
ax.set_ylim(y_range)

line, = ax.plot(xs, ys)

plt.title("Power and Shit")
plt.xlabel("Time")
plt.ylabel("Watts")

def bin_to_dec(array_of_values)
    retval = 0
    if(ADC_Value[0]*5.0/0x7fffff == 1)
        reval += 1
    if(ADC_Value[1]*5.0/0x7fffff == 1)
        reval += 2
    if(ADC_Value[2]*5.0/0x7fffff == 1)
        reval += 4
    if(ADC_Value[3]*5.0/0x7fffff == 1)
        reval += 8
    if(ADC_Value[4]*5.0/0x7fffff == 1)
        reval += 16
    if(ADC_Value[5]*5.0/0x7fffff == 1)
        reval += 32
    if(ADC_Value[6]*5.0/0x7fffff == 1)
        reval += 64
    if(ADC_Value[7]*5.0/0x7fffff == 1)
        reval += 128

    return retval
    

def animate(i, ys)

    power = adc.ADS1256()
    power.ADS1256_init()

    ADC_Value = power.ADS1256_GetAll()

    value = bin_to_dec(ADC_Value)

    ys.append(value)

    ys = ys[-x_len:]

    line.set_ydata(ys)

    return line,

ani = animation.FuncAnimation(fig, animate, fargs=(ys,), interval=50, blit=True)
plt.show()
