#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import math

import rospy

import numpy as np

from message.msg import touch_message

from message.msg import classification_message

pub = rospy.Publisher('touch_classification', classification_message , queue_size=5)

message = classification_message()

message.classification_type = 'squeeze'

message.frequency = 1

message.intensity = 1

message.area = 1

message.duration = 3

# Input from Touch node

# 1. position : list of int

def listener1():
    
    rospy.init_node('touch', anonymous=True)

    #rospy.Subscriber("imu1", Imu , callback)

    pub.publish(message)
        
    rospy.spin()

if __name__ == '__main__':

    listener1()

# Float MultiArray

'''
if __name__ =="__main__":
    rospy.init_node("publisher")
    pub = rospy.Publisher('sent_matrix', Float32MultiArray, queue_size=1)
    r = rospy.Rate(0.5)
    # let's build a 3x3 matrix:
    mat = Float32MultiArray()
    mat.layout.dim.append(MultiArrayDimension())
    mat.layout.dim.append(MultiArrayDimension())
    mat.layout.dim[0].label = "height"
    mat.layout.dim[1].label = "width"
    mat.layout.dim[0].size = 3
    mat.layout.dim[1].size = 3
    mat.layout.dim[0].stride = 3*3
    mat.layout.dim[1].stride = 3
    mat.layout.data_offset = 0
    mat.data = [0]*9

    # save a few dimensions:
    dstride0 = mat.layout.dim[0].stride
    dstride1 = mat.layout.dim[1].stride
    offset = mat.layout.data_offset
    while not rospy.is_shutdown():
        tmpmat = np.zeros((3,3))
        for i in range(3):
            for j in range(3):
                num = random.randrange(0,10)
                mat.data[offset + i + dstride1*j] = num
                tmpmat[i,j] = num
        pub.publish(mat)
        rospy.loginfo("I'm sending:")
        print tmpmat,"\r\n"
        r.sleep()
'''

