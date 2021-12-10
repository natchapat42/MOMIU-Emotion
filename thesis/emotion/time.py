#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import rospy

import math

import random

from message.msg import *

#from message.msg import IR_message

#from message.msg import touch_message

#from message.msg import classification_message

import os

import sys

from subprocess import call

############################################3


def listener1():
    
    rospy.init_node('touch', anonymous=True)

    now = rospy.get_rostime()

    rospy.loginfo("Current time %i %i", now.secs, now.nsecs)

    one = rospy.get_time()

    seconds = 222
    print(seconds)

    epoch = rospy.Time() # secs=nsecs=0
    print(epoch)
    t = rospy.Time(10) # t.secs=10
    t = rospy.Time(12345, 6789)

    print(t)

    d = rospy.Duration.from_sec(60.1)  # One minute and one tenth of a second
    seconds = d.to_sec() #floating point
    nanoseconds = d.to_nsec()

    print(d)
    print(seconds)
    print(nanoseconds)

    rospy.sleep(15)

    two = rospy.get_time()

    three = two - one

    print(three)   

    

if __name__ == '__main__':

        listener1()


        