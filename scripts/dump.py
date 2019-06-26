#!/usr/bin/env python3

import sys
import serial

if len(sys.argv) < 2:
    print("Usage: "+sys.argv[0]+" tty")
    exit(1)

print("Using "+sys.argv[1])

ser = serial.Serial(
    port = sys.argv[1],
    baudrate = 115200,
    parity = serial.PARITY_EVEN,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 10)

state = 0
data = []
while(1):
    s = ser.read(1)
    if s == bytes([0xAA]):
        state += 1
        if state == 2:
            state = 0
            for i in range(4):
                h = ord(ser.read(1))
                l = ord(ser.read(1))
                data.append(256*h+l)

            csum = ser.read()

            print("---")
            print(len(data), data)
            data = []

