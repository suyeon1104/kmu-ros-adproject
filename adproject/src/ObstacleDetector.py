#!/usr/bin/env python
import cv2
import numpy as np
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class ObstacleDetector:
    def __init__(self,topic):
        self.img_shape = (480, 640, 3)
        self.cam_img = np.zeros(shape=self.img_shape, dtype=np.uint8)
        self.bridge = CvBridge()
        self.sub = rospy.Subscriber(topic, Image, self.conv_image)
        warp_range = np.float32([[0, 250], [0, 480], [640, 480], [640, 250]])
        bev_range = np.float32([[0, 0], [260, 480], [380, 480], [640, 0]])
        self.M = cv2.getPerspectiveTransform(warp_range, bev_range)

    def conv_image(self,data):
        self.cam_img = self.bridge.imgmsg_to_cv2(data,'bgr8')

    def getObstacle(self):
        hsv = cv2.cvtColor(self.cam_img, cv2.COLOR_BGR2HSV_FULL)
        hue, sat, val = cv2.split(hsv)
        hue_masked = cv2.bitwise_not(cv2.inRange(hue, 40, 200))
        mrg = cv2.merge([hue_masked, sat, val])
        res = cv2.cvtColor(mrg, cv2.COLOR_HSV2BGR_FULL)

        canny = cv2.Canny(res, 100, 255)
        # canny[370:]=0
        warp = cv2.warpPerspective(canny, self.M, (640, 480))
        warp[370:] = 0

        roi = warp[:155, 207:437]
        cv2.imshow('roi',warp)
        cv2.waitKey(1)
        print(np.count_nonzero(roi))
        if 13000 > np.count_nonzero(roi) > 12500:
            print 'EnD'
            return True
        return False

