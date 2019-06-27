#!/bin/env python3
import sys
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

if len(sys.argv) < 2:
    print("Usage: "+sys.argv[0]+" file")
    exit(1)

filename = sys.argv[1]
print("Reading " + filename)

x0 = np.array([])
x1 = np.array([])
x2 = np.array([])
x3 = np.array([])

app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="Draw dump")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph app')
pg.setConfigOptions(antialias=True)
p0 = win.addPlot(col=0, row=0, title="Plot0")
p1 = win.addPlot(col=0, row=1, title="Plot1")
p2 = win.addPlot(col=0, row=2, title="Plot2")
p3 = win.addPlot(col=0, row=3, title="Plot3")

w0 = p0.plot(pen='r')
w1 = p1.plot(pen='g')
w2 = p2.plot(pen='b')
w3 = p3.plot(pen='y')

state = 0
data = []
counter = 0

with open(filename, "rb") as f:
    s = f.read(1)
    while(s != b''):
        if(s == b'\xAA'):
            state += 1
            if state == 2:
                try:
                    state = 0
                    for i in range(4):
                        h = ord(f.read(1))
                        l = ord(f.read(1))
                        result = 256*h + l
                        ## make signed
                        if result > 32767:
                            result = result - 65536
                        ## sort of filter
                        #if(i != 0 and result < 10000):
                        #    result = 65535
                        data.append(result)

                    csum = f.read(1)

                    counter += 1
                    x0 = np.append(x0, data[0])
                    x1 = np.append(x1, data[1])
                    x2 = np.append(x2, data[2])
                    x3 = np.append(x3, data[3])

                    w0.setData(x0)
                    w1.setData(x1)
                    w2.setData(x2)
                    w3.setData(x3)

                except Exception as e:
                    print("EOF", e)
                data = []
                
        s = f.read(1)

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
