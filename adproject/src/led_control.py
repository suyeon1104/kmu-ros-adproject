#!/usr/bin/env python
'''
  Usage: python led_control.py COM5
  Usage: python led_control.py /dev/ttyUSB1
  F1  => F1
  F0  => F0
  B1  => B1
  B0  => B0
  L30,30 => L<ontime><offtime>
  L30,65 => L<ontime><offtime>
  R30,30 => R<ontime><offtime>
  O   => O
  E130,30 => E1<ontime><offtime>
  E0  => E0
  I   => I
'''

import sys
import serial
import time
import rospy
from std_msgs.msg import String

ser = serial.Serial('/dev/ttyUSB2')
print("   ser.baudrage:", ser.baudrate)

message = ''
rospy.init_node('LED CONTROLLER')

def callback(data):
    global message
    message = data.data

sub = rospy.Subscriber('/led_controller',String,callback)

line = ''
while True:
    while line == message:
        time.sleep(0.1)
    line = message
    line = line.rstrip()
    if line == b'I' or line == b'F1' or line == b'F0' or line == b'B1' or line == b'B0' or line == b'O' or line == b'E0' or line == b'L0' or line == b'R0':
        ser.write(line)
        ser.flush()
        print("->:", line)
    elif line[0:1] == b'L':
        args = line[1:].split(b',')
        on_time = int(args[0])
        off_time = int(args[1])
        output = line[0:1] + chr(on_time).encode() + chr(off_time).encode()
        ser.write(output)
        ser.flush()
        print("->:", output)
    elif line[0:1] == b'R':
        args = line[1:].split(b',')
        on_time = int(args[0])
        off_time = int(args[1])
        output = line[0:1] + chr(on_time).encode() + chr(off_time).encode()
        ser.write(output)
        ser.flush()
        print("->:", output)
    elif line[0:2] == b'E1':
        args = line[2:].split(b',')
        on_time = int(args[0])
        off_time = int(args[1])
        output = line[0:2] + chr(on_time).encode() + chr(off_time).encode()
        ser.write(output)
        ser.flush()
        print("->:", output)
    else:
        print("invalid command:", line)
    time.sleep(0.1)
