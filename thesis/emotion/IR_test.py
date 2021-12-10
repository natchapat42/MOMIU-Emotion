#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Setting

import math

import rospy

import numpy as np

from std_msgs.msg import Bool

from std_msgs.msg import Float32

from message.msg import *

from message.msg import classification_message

pub = rospy.Publisher('IR_classification', classification_message , queue_size=5)

message = classification_message()

frequency_close_eye = 0

frequency_say_hi = 0

frequency_chin = 0

duration_chin = 0

duration_face = 0

first = 0

one = 0

# Input from IR node

# 1. Chin : boolean

# 2. Face : range (float)

class IR_sensors:

    def __init__(self,one,first,duration_chin,duration_face,frequency_chin,frequency_say_hi,frequency_close_eye):

        self.one = one

        self.first = first

        self.duration_chin = duration_chin

        self.duration_face = duration_face

        self.frequency_chin = frequency_chin

        self.frequency_say_hi = frequency_say_hi

        self.frequency_close_eye = frequency_close_eye

def chin(data):

    # For Duration 

    print(data)

    if IR.duration_chin == 0 :

        IR.one = rospy.get_time()

    else :

        IR.one = IR.one

    # For classification

    if data.data == True :

        message.classification_type = "chin"

        IR.frequency_chin += 1

        # Reset frequency

        if IR.frequency_chin > 200 :

            IR.frequency_chin = 1

        message.frequency = IR.frequency_chin

        message.area = 1

        # duration

        seconds = rospy.get_time()

        IR.duration_chin += seconds - IR.one

    else :

        message.classification_type = "hug"

        message.frequency = 0

        message.intensity = 0

        message.area = 0

        IR.duration_chin = 0

    message.duration = IR.duration_chin

    pub.publish(message)

def face(data):

    print(data)

    # For duration

    if IR.duration_face == 0 :

        IR.first = rospy.get_time()

    else :

        IR.first = IR.first 

    # For Classification

    if data.data <= 200  :

        # Close _eye

        message.classification_type = "close_eye"

        IR.frequency_close_eye += 1

        if IR.frequency_close_eye >= 200 :
    
            IR.frequency_close_eye = 1

        message.frequency = IR.frequency_close_eye

        # duration

        seconds = rospy.get_time()

        IR.duration_face += seconds - IR.first

    elif  data.data > 700 :

        # Say_hi

        message.classification_type = "say_hi"

        IR.frequency_say_hi += 1

        # Reset frequency

        if IR.frequency_say_hi >= 200 :
        
            IR.frequency_say_hi = 1

        message.frequency = frequency_say_hi

        # duration

        seconds = rospy.get_time()

        IR.duration_face += seconds - first

    else :

        message.classification_type = "hug"

        message.frequency = 0

        message.intensity = 0

        message.area = 0

        duration = 0

    message.duration = IR.duration_face

    message.area = 0

    pub.publish(message)

def listener1():
    
    rospy.init_node('IR', anonymous=True)

    rospy.Subscriber("IR_face", Float32 , face) # range

    rospy.Subscriber("IR_chin", Bool , chin) # 0 , 1
        
    rospy.spin()

if __name__ == '__main__':

    IR = IR_sensors(one,first,duration_chin,duration_face,frequency_chin,frequency_say_hi,frequency_close_eye)
    
    listener1()


# duration from ros time

# node ที่รับค่ามาจาก IR sensors


