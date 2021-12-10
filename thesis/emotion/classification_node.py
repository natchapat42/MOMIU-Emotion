#!/usr/bin/env python

#-*- coding: utf-8 -*-

import rospy

from message.msg import classification_message

from services.srv import classification_service

def talker():

    pub = rospy.Publisher('classification_data', classification_message , queue_size=5)

    rospy.init_node('talker', anonymous=True)

    rate = rospy.Rate(0.25) # 0.25hz

    # Creat new classification_message object and fill in its contents.

    message = classification_message()

    # Fill in the data infomation

    message.classification_type = "hug"

    message.frequency = 1

    message.intensity = 2

    message.area = 3

    message.duration = 3.5

    while not rospy.is_shutdown():

        pub.publish(message)

        rate.sleep()

    rospy.spin()

if __name__ == '__main__':

    try:

        talker()

    except rospy.ROSInterruptException:
        
        pass