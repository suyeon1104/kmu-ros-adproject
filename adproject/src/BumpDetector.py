import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class BumpDetector:
    def __init__(self, topic):
        self.img_shape = (480,640,3)
        self.cam_img = np.zeros(shape=self.img_shape,dtype=np.uint8)
        self.bridge = CvBridge()
        self.sub = rospy.Subscriber(topic,Image,self.conv_image)
        
    def conv_image(self, data):
        self.cam_img = self.bridge.imgmsg_to_cv2(data,'bgr8')
    
    def getBump(self):
        hsv = cv2.cvtColor(self.cam_img,cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv,(20,50,200),(40,255,255))
        canvas = np.zeros(self.cam_img.shape[:2],np.uint8)
        cv2.fillPoly(canvas,[np.int32([[145,264],[90,344],[491,351],[447,270]])],(255))
        masked = np.uint8(np.float32(canvas)*np.float32(thresh)/255)
        if(np.count_nonzero(masked)>2500):
            return True
        return False
       	
