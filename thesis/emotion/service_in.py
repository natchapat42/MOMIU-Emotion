#!/usr/bin/env python

from __future__ import print_function

from services.srv import classification_service

import rospy

def handle_add_two_ints(req):

    print("Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))

def add_two_ints_server():

    rospy.init_node('add_two_ints_server')

    s = rospy.Service('add_two_ints', classification_service, handle_add_two_ints) #topic / message / callback

    print("Ready to add two ints.")

    rospy.spin()

if __name__ == "__main__":

    add_two_ints_server()
