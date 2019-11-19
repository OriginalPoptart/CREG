import matplotlib.pyplot as plt
import socket
import numpy as np
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

host = '127.0.0.1'
port = 42069

data = [1,1,1]

def f(x):
    return x**2

def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def sendCommand():
    while True:
        command = input("Enter a command: ")
        if command == "PLOT":
            print("You entered: PLOT")
            #s.send(str.encode(command))
            #reply = s.recv(1024)
            #print(reply)
            t = np.arange(-5., 5.2, 0.2)
            plt.title('This is a test Title')
            plt.xlabel('time')
            plt.ylabel('power')
            plt.plot(t, f(t))
            #plt.plot([1,2,3,4], [1,4,9,16])
            plt.tight_layout()
            plt.show()
        elif command == "DATA":
            print("You entered: DATA")
            
            filex = open("testDataX.txt","r")
            filey = open("testDataY.txt","r")
            fileDataX = filex.readlines()
            fileDataY = filey.readlines()
            #step = len(fileData)
            #print(step)
            t = np.arange(0., 100., 1)
            plt.title('This is a test Title')
            plt.xlabel('time')
            plt.ylabel('power')
            #plt.axis([0, 20, 0, 100])
            plt.plot(t, f(t))
            #plt.plot([1,2,3,4], [1,4,9,16])
            plt.tight_layout()
            plt.show()
            #s.send(str.encode(command))
            #reply = s.recv(1024)
            #print(reply)
        elif command == "PIE":
            labels = 'How much I want', 'How much I probably should take', 'How much I actually eat'
            sizes = [30, 15, 55]
            explode = (0.01, 0.01, 0.1)

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode = explode, labels = labels, autopct = '%1.1f%%', shadow = True, startangle = 90)
            ax1.axis('equal')
            plt.tight_layout()
            plt.show()
        elif command == "WHAT":
            xs = [0, 1, 2, 3, 4, 5, 6, 7]
            ys = [1, 0.3, -2.3, 5.1, 7.6, -0.2, -1.8, 4]

            plt.plot(xs, ys)
            plt.show()
        elif command == "MOVE":
            filex = open("testDataX.txt","r")
            fileDataX = filex.readlines()

            #xs = [0, 1, 2, 3, 4, 5, 6, 7]
            #ys = [1, 0.3, -2.3, 5.1, 7.6, -0.2, -1.8, 4]
            
            xs = xs[-5:]
            ys = ys[-5:]

            ax.clear()
            ax.plot(xs, ys)

            # Format plot
            plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.30)
            plt.title('TMP102 Temperature over Time')
            plt.ylabel('Temperature (deg C)')

            # Draw the graph
            plt.show()
        elif command == 'KILL':
            print("You entered: KILL")
            #reply = s.recv(1024)
            #print(reply)
            #s.close()
            break
        else:
            print("Unknown command")

def moveIt(i, xs, ys):
    filex = open("testDataX.txt","r")
    fileDataX = filex.readlines()

#setupsocket()
ani = animation.FuncAnimation(fig, moveIt, fargs = (xs,ys), interval = 1000)
sendCommand()#s)
