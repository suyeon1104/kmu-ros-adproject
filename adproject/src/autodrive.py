#!/usr/bin/env python

import rospy, time
import serial
import numpy as np

#from linedetector import LineDetector
from MotorControl import MotorControl
from BumpDetector import BumpDetector
from NightDetector import NightDetector
from ObstacleDetector import ObstacleDetector

from std_msgs.msg import String

class AutoDrive:

    def __init__(self):
        rospy.init_node('xycar_driver')
        self.line_detector = 0#LineDetector('/usb_cam/image_raw')
        self.bump_detector = BumpDetector('/usb_cam/image_raw')
        self.night_detector = NightDetector('/usb_cam/image_raw')
        self.led_control_pub = rospy.Publisher('/led_controller',String,queue_size=1)
        self.obstacle_detector = ObstacleDetector('/usb_cam/image_raw')
        self.motor = MotorControl(14)
        self.trig = True

    def trace(self):
        #insert Autodrive Logic
        if self.bump_detector.getBump():
            print 'BUMP!'
            self.led_control_pub.publish(String("B1"))
            for i in range(40):
                self.motor.drive(100,120)
                time.sleep(0.1)
            self.led_control_pub.publish(String("B0"))
        else:
            print 'NO' 
            self.motor.drive(100,140)

    def stop(self):
        print 'stop'
        self.sendLed('E19,9')
        for i in range(5):
            self.motor.drive(100,0)
            time.sleep(0.1)
        self.motor.drive(90,90)
        
    def moveLeft(self):
        self.led_control_pub.publish(String('R19,9'))
        for i in range(20):
            self.motor.drive(100,150)
            time.sleep(0.1)
        for i in range(5):
            self.motor.drive(125,150)
            time.sleep(0.1)
        for i in range(7):
            self.motor.drive(105,150)
            time.sleep(0.1)
        self.led_control_pub.publish(String('R0'))
        for i in range(7):
            self.motor.drive(70,150)
            time.sleep(0.1)
        for i in range(10):
            self.motor.drive(100,150)
            time.sleep(0.1)
            
    def night_detect(self):
        if self.night_detector.isNight():
            self.sendLed('F1')
        else:
            self.sendLed('F0')

    def sendLed(self,l):
        self.led_control_pub.publish(String(l))

    def exit(self):
        print('finished')

if __name__ == '__main__':
    car = AutoDrive()
    time.sleep(10)
    rate = rospy.Rate(10)
    print('READY')
    car.moveLeft()
    while not rospy.is_shutdown():
        car.trace()
        car.night_detect()
        time.sleep(0.1)
        #if ti > 40:#car.obstacle_detector.getObstacle():
        #    car.stop()
        #    break;
    rospy.on_shutdown(car.exit)
