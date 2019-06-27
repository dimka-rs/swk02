#!/bin/env python3
import sys 

if len(sys.argv) < 2:
    print("Usage: "+sys.argv[0]+" file")
    exit(1)

filename = sys.argv[1]
print("Reading " + filename)

state = 0
data = []

with open(filename, "rb") as f:
    s = f.read(1)
    while(s != b''):
        if(s == b'\xAA'):
            state += 1
            if state == 2:
                state = 0
                for i in range(4):
                    l = ord(f.read(1))
                    h = ord(f.read(1))
                    data.append(256*h+l)

                csum = f.read(1)

                if (data[0] == 1777):
                    print("%d\t%d\t%d\t%d\t| %d" % (data[0], data[1], data[2], data[3], ord(csum)))
                data = []
                
        s = f.read(1)
