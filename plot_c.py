import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import ADS1256 as adc
import time
from subprocess import call


x_len = 10
y_range = [0, 1]

fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

total_length = 100
destination_file = "data"
#command = str("./ads1256_test " + str(total_length) + " > " + destination_file)
#call(["./ads1256_test 100 > data"])

xs = [0] * (total_length)
ys = [0] * (total_length)
ys1 = [0] * (total_length)

numberOfTests = 1

#begin = time.time()
call(["./ads1256_test", str(total_length)])
#end = time.time()

#totalTime = end-begin

#print(total_length," samples taken over ", totalTime, " seconds")
#print(total_length/totalTime, " samples per second")

i = 0
file = open("data", "r")
for line in file:
    #print(line)
    data = line.split()
    xs[i] = float(data[0])
    ys[i] = float(data[1])
    ys1[i] = float(data[2])
    i += 1
    #print(xs[i], ", ", ys[i], ", ", ys1[i])

plt.title("Power")
plt.xlabel("Time")
plt.ylabel("Watts")

ax.plot(xs, ys)
ax2.plot(xs, ys1)
plt.show()