import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import ADS1256 as adc
import time
from subprocess import call


x_len = 10
y_range = [0, 1]

fig = plt.figure()
#ax = fig.add_subplot(2, 1, 2)
ax2 = fig.add_subplot(1, 1, 1)
#xs = list(range(0, x_len))
#ys = [0] * x_len
#ax.set_ylim(y_range)

#line, = ax.plot(xs, ys)



#def bin_to_dec(array_of_values)
#    retval = 0
#    if(ADC_Value[0]*5.0/0x7fffff == 1)
#        reval += 1
#    if(ADC_Value[1]*5.0/0x7fffff == 1)
#        reval += 2
#    if(ADC_Value[2]*5.0/0x7fffff == 1)
#        reval += 4
#    if(ADC_Value[3]*5.0/0x7fffff == 1)
#        reval += 8
#    if(ADC_Value[4]*5.0/0x7fffff == 1)
#        reval += 16
#    if(ADC_Value[5]*5.0/0x7fffff == 1)
#        reval += 32
#    if(ADC_Value[6]*5.0/0x7fffff == 1)
#        reval += 64
#    if(ADC_Value[7]*5.0/0x7fffff == 1)
#        reval += 128

#    return retval

power = adc.ADS1256()
power.ADS1256_init()    

def animate(i, ys):

    #ADC_Value = power.ADS1256_GetAll()

    #value = ADC_Value[0]*1.0/0x7fffff #bin_to_dec(ADC_Value)

    #ys.append(ADC_Value[0]*1.0/0x7fffff)#value)
    ys.append(power.ADS1256_GetAll()[0]*1.0/0x7fffff)
    ys = ys[-x_len:]

    line.set_ydata(ys)

    return line,

#ani = animation.FuncAnimation(fig, animate, fargs=(ys,), interval=1, blit=True)
#plt.show()

total_length = 50

#call(["./ads1256_test 100 > data"])

xs = [0] * (total_length)
ys = [0] * (total_length)
ys1 = [0] * (total_length)

numberOfTests = 1
times = [0] * numberOfTests

#for j in range(numberOfTests):
begin = time.time()

for i in range(total_length):
    ys[i] = (power.getValueAtPin(2)*50.0/0x7fffff)
    ys1[i] = (power.getValueAtPin(0)*255.0/0x7fffff)
    xs[i] = (time.time()-begin)

ys[0] = 2.5

end = time.time()

    #times [j] = end - begin

totalTime = end-begin

print(total_length," samples taken over ", totalTime, " seconds")
print(total_length/totalTime, " samples per second")
#print("Average samples per second = ", sum(times)/numberOfTests)

F = open("data", "w")
for i in range (total_length):
    F.write(str(xs[i]) + "\t" + str(ys[i]) + "\t" + str(ys1[i]) + "\n")
F.close()

plt.title("Power")
plt.xlabel("Time")
plt.ylabel("Watts")

ax.plot(xs, ys)
ax2.plot(xs, ys1)
plt.show()