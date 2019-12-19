import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import numpy as np
import cv2

class NightDetector:
    def __init__(self,topic):
        self.img_size = (480,640,3)
        self.img = np.zeros(self.img_size,np.uint8)
        self.bridge = CvBridge()
        self.sub = rospy.Subscriber(topic,Image,self.conv_image)

    def conv_image(self,data):
        self.img = self.bridge.imgmsg_to_cv2(data,'bgr8')

    def isNight(self):
        gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        roi = gray[100:380,140:500]
        if np.mean(roi) < 100:
            return True
        return False
