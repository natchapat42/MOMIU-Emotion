#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import math

import rospy

import numpy as np

from message.msg import IR_message

from message.msg import classification_message

pub = rospy.Publisher('IR_classification', classification_message , queue_size=5)

message = classification_message()

message.classification_type = 'hug'

message.frequency = 0

message.intensity = 0

message.area = 0

message.duration = 0

frequency_close_eye = 0

frequency_say_hi = 0

frequency_chin = 0

# Input from IR node

# 1. status : boolean

# 2. range : float

def callback(data):

    global frequency_close_eye

    global frequency_say_hi

    global frequency_chin

    position = data.position

    #position = 0 = face / position = 1 = chin

    distance = data.range

    if position == 0 :

        if distance <= 1000 :

            message.classification_type == "close_eye"

            frequency_close_eye += 1

            message.frequency = frequency_close_eye

        else :

            message.classification_type == "say_hi"

            frequency_say_hi += 1

            message.frequency = frequency_say_hi

    elif position == 1 :

        message.classification_type = "chin"

        frequency_chin += 1

        message.frequency = frequency_chin

    else: 

        message.classification_type = "hug"

        message.frequency = 0

    pub.publish(message)

def listener1():
    
    rospy.init_node('TEST', anonymous=True)

    #rospy.Subscriber("imu1", Imu , callback)

    pub.publish(message)
        
    rospy.spin()

if __name__ == '__main__':

    listener1()
