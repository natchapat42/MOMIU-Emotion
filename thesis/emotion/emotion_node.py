#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from pickle import decode_long

import rospy

import math

import random

from message.msg import *

from pyfiglet import Figlet

import momiu_happy , momiu_think , momiu_sad , momiu_hello , momiu_angry , momiu_tickle

import numpy as np

from scipy.spatial import distance

from momiu_happy import *

from momiu_think import *

from momiu_sad import *

from momiu_hello import *

from momiu_angry import *

from momiu_tickle import *

#from message.msg import IR_message

#from message.msg import touch_message

#from message.msg import classification_message

import os

import subprocess

from subprocess import call

from subprocess import Popen

####################################################################################################################

import pygame
import pandas as pd
import numpy , sys , time

from pygame.locals import *

from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image as Image

pub = rospy.Publisher('pose', pose_message , queue_size=5)

message = pose_message()

################################################################################################################### All input from raw_data node (Imu , touch , IR)

# Input from Classification_node

# 1. Type (String) :  chin , close_eye , say_hi , hug , pat , slap , touch , squeeze , tickle , shake , lift
# 2. Intensity (Integer)
# 3. Frequency (Integer)
# 4. Area (Integer)
# 5. Duration (Float)

# Input from Emotion_node

# 6. Emotion state (for blending emotion)

#################################################################################################################### Initial Value

happy = [0.4,0.6,0]

angry = [0.8,-0.6,0]

surprise = [-0.15,0.3,0]

sad = [-0.5,-0.3,0]

natural = [0,0,0]

action = [happy , angry , surprise , sad , natural]

action_callback = { 0 : "happy" , 1 : "angry" , 2 : "surprise" , 3 : "sad" , 4 : "natural" }

# 7. Habits (Initial Value) 

bother = (0.8,0.6,0.3)

polite = (-0.5,-0.2,-0.4)

# happy / angry / surprise / sad / natural 

bother_emotional_stack = [2,2,3,3,1] 

#polite_emotional_stack = [4,4,3,4,1]

polite_emotional_stack = [1,1,1,1,1] # test clip

# chin / close_eye / say_hi  / hug / pat / slap / touch / squeeze / tickle / shake / lift

bother_classification_stack = [3,3,1,2,4,2,2,3,2,2] 

#polite_classification_stack = [1,3,1,1,4,4,5,4,3,3]

polite_classification_stack = [1,1,1,1,1,1,1,1,1,1] # test clip

habits = bother

classification_stack = polite_classification_stack 

classification_current_stack = [0,0,0,0,0] # if stack is full in each classification , then generate action 1 time

emotional_stack = polite_emotional_stack # if stack is full in each emotion , then action emotion 1 time

# No Data = None

# Initial State = Natural

physical_classification = { "chin" : 0 , "close_eye" : 1 , "say_hi" : 2 , "hug" : 3 , "pat" : 4 , 
                            "slap" : 5 , "touch" : 6 , "squeeze" : 7 , "shake" : 8 , "lift" : 9}

                            # เกาคาง / หลับตา / สวัสดี / กอด / ลูบ / ตบ / จับ / บีบ / 'จั๊กจี้' / เขย่า / ยก

# Touch_classification_gain

# 3 = 0.10
# 2 = 0.5
# 1 = 0.2 

chin_gain = [0.06,0.09,0.08] # +++

close_eye_gain = [-0.06,-0.02,-0.02] # - 

say_hi_gain = [-0.02,0.05,-0.03] # +

hug_gain = [0.1,0.07,0.1] # +++

pat_gain = [-0.03,0.03,-0.05] # +

slap_gain = [0.15,-0.12,0.07] # ---

touch_gain = [-0.1,0.02,-0.04] # +

squeeze_gain = [-0.05,-0.04,0.04] # -- 

tickle_gain = [0.05,-0.1,0.04] # --

shake_gain = [0.06,-0.07,0.07] # --

lift_gain = [0.03,0.03,-0.05] # +

old_emotion = [0,0,0]

### For frequency

frequency = [0,0,0,0,0,0,0,0,0,0] 

diff_frequency = [0,0,0,0,0,0,0,0,0,0]

#######################

arousal = 0

valence = 0

stance = 0

### Check Input / else

Input_test = [3,0,0,0,0] 

old_input = []

## For clip

loop_emotion = 1

###################################################################################################################################

def maximum(arousal,valence,stance):

    if arousal >= 1 :

        arousal = 1

    elif arousal <= -1 :

        arousal = -1

    else :

        arousal = arousal

    #print(arousal)

    if valence >= 1 :
    
        valence = 1

    elif valence <= -1 :
    
        valence = -1

    else :

        valence = valence

    #print(valence)

    if stance >= 1 :
    
        stance = 1

    elif stance <= -1 :
    
        stance = -1

    else :

        stance = stance

    #print(stance)

    return(arousal , valence , stance)

def process(Input,arousal,valence,stance):

    global old_emotion

    global old_input

    global diff_frequency

    global loop_emotion 

    # Check

    #print("check")

    #print("arousal= " + str(arousal))

    #print("valence= " + str(valence))

    #print("stance= " + str(stance))

    # Find nearest value

    distance = []

    for i in range(0,5) :

        distance.append(math.sqrt(((arousal-action[i][0])**2)+((valence-action[i][1])**2))) # Find nearest distance

    nearest = min(distance) # Find min values of nearest distance

    min_index = distance.index(nearest) # Find index of min values

    # print(min_index)

# Part 2 Blending

    #print("Current emotion is " + action_callback[min_index]) # convert interger to string

    current_emotion = [arousal,valence,stance] # emotion k

    # Find emotion average between emotion (k-1,k)

    blending_emotion = [(( (habits[0]*0.6) + (current_emotion[0]*0.25) + (old_emotion[0]*0.15) )) , (( (habits[1]*0.2) + (current_emotion[1]*0.6) + (old_emotion[1]*0.2) )) ,(( habits[2] + current_emotion[2] + old_emotion[2] ) / 3 ) ]

    distance_blending = []

    #print(blending_emotion)

    for i in range(0,5) :

        distance_blending.append(math.sqrt(((blending_emotion[0]-action[i][0])**2)+((blending_emotion[1]-action[i][1])**2)))

        ############################################

    #print(distance_blending)

    nearest_blending = min(distance_blending) # Find min values of nearest distance

    min_index_blending = distance_blending.index(nearest_blending) # Find index of min values

    #print(min_index_blending)

    #print("Blending emotion is " + action_callback[min_index_blending]) # convert interger to string

    #print(blending_emotion)

    classification_current_stack[min_index_blending] += 1

    #print(classification_current_stack)

    ###

    #print(old_emotion)

    old_emotion = blending_emotion # emotion state k >> emotion state k-1

    #print(blending_emotion)    

    #maximum(arousal,valence,stance)

    arousal = old_emotion[0]

    valence = old_emotion[1]

    stance = old_emotion[2]

    if arousal >= 1 :
    
        arousal = 1

    elif arousal <= -1 :

        arousal = -1

    else :

        arousal = arousal

    #print(arousal)

    if valence >= 1 :
    
        valence = 1

    elif valence <= -1 :
    
        valence = -1

    else :

        valence = valence

    #print(valence)

    if stance >= 1 :
    
        stance = 1

    elif stance <= -1 :
    
        stance = -1

    else :
    
        stance = stance

    #print("arousal is " + str(arousal))

    #print("valence is " + str(valence))

    #print("stance is " + str(stance))

# Part 3 Habits 

    # find intensity / duration in each action

    # Real

    if stance < 0.2 :
    
        message.intensity = 1

        message.loop = random.randint(1, 1)

        #print(message.intensity)

    elif 0.2 <= stance <= 0.6 :

        message.intensity = 2

        message.loop = random.randint(1, 2)

        #print(message.intensity)

    elif 0.6 < stance :

        message.intensity = 3

        message.loop = random.randint(2, 3)

        #print(message.intensity)

    else :
    
        print("I don't know what happennnnnnnnnnnnnn!!")
    
    # Simulation

    # happy / angry / surprise / sad / natural 

    if (classification_current_stack[0] % emotional_stack[0] == 0) and (classification_current_stack[0] != 0) : 

        #print("happy")

        message.pose = 'happy'

        level = message.intensity

        message.face = ('happy%d.jpg' % level)

        print("So , Emotion of MOMIU Robot is >> happy level%d <<" % level)

        print("-------------------------\n")

        #print(message.face)

        classification_current_stack[0] = 0
    
    elif (classification_current_stack[1] % emotional_stack[1] == 0) and (classification_current_stack[1] != 0)  : 

        #print("angry")

        message.pose = 'angry'

        level = message.intensity

        message.face = ('angry%d.jpg' % level)

        #print(message.face)

        print("So , Emotion of MOMIU Robot is >> angry level%d <<" % level)

        print("-------------------------\n")

        classification_current_stack[1] = 0

    elif (classification_current_stack[2] % emotional_stack[2] == 0) and (classification_current_stack[2] != 0)  : 

        #print("surprise")

        message.pose = 'surprise'

        message.face = 'surprise.jpg'

        print("So , Emotion of MOMIU Robot is >> surprise <<")

        print("-------------------------\n")

        classification_current_stack[2] = 0

    elif (classification_current_stack[3] % emotional_stack[3] == 0) and (classification_current_stack[3] != 0)  : 

        #print("sad")

        message.pose = 'sad'

        level = message.intensity

        message.face = ('sad%d.jpg' % level)

        print("So , Emotion of MOMIU Robot is >> Sad level%d <<" % level)

        print("-------------------------\n")

        #print(message.face)

        classification_current_stack[3] = 0

    elif (classification_current_stack[4] % emotional_stack[4] == 0 and (classification_current_stack[4] != 0) ) : 

        #print("natural")

        message.pose = 'natural' # still not have "natural simulation" >> so use think instead

        message.face = 'natural.jpg'

        classification_current_stack[4] = 0

        print("So , Emotion of MOMIU Robot is >> Natural <<")

        print("-------------------------\n")

    else :

        #p = Popen(['python', 'momiu_happy.py'])

        #p.kill()

        #print("Fuckkkkkkkkk")

        message.pose = 'confuse'

        message.face = 'confuse.jpg'

        print("I don't know what are you doing... ?")

        print("So , Emotion of MOMIU Robot is >> Confuse <<")

    old_input = Input

    pub.publish(message)

    print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    print("arousal is " + str(arousal))

    print("valence is " + str(valence))

    print("stance is " + str(stance))

    print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    #p.terminate()

def Emotion(data):

    global arousal

    global valence 

    global stance 

    global old_emotion

    global old_input

    global diff_frequency

    global loop_emotion

    #p = subprocess.Popen(['python', 'momiu_angry.py'])

    #exec(open('momiu_happy.py').read())

    Input = [data.classification_type,data.frequency,data.intensity,data.area,data.duration] #list of data

    Input[0] = physical_classification[Input[0]] # convert string to integer for calculation

    print('-------------------------------------------------------')

    print(old_emotion)

    if  (Input == Input_test) and (old_input != Input_test) and (old_input != []):

    # Part 1 Current emotion

        # IMU ( type , frequency , intensity , area(Frame) , duration )

        if (old_input[0] == 8) and ( (old_input[1] // 200 ) % classification_stack[8] == 0 ) : #shake --- # 10 ครั้งนับ 1

            print("Loop : %d\n" % loop_emotion)

            print("Physical Action Input is Shake\n")

            diff_frequency[8] = old_input[1] - frequency[8]

            frequency[8] = old_input[1]

            #print(frequency)

            #print(diff_frequency)

            arousal += shake_gain[0] * ((diff_frequency[8]*0.25) + (old_input[2]*0.5) + (old_input[4]*0.25)) # frequency / intensity / duration

            valence += shake_gain[1] * ((diff_frequency[8]*0.4) + (old_input[2]*0.4) + (old_input[4]*0.2)) 

            stance += shake_gain[2] * ((diff_frequency[8]*0.33) + (old_input[2]*0.33) + (old_input[4]*0.33)) 

        elif (old_input[0] == 9) and ( (old_input[1] // 200) % classification_stack[9] == 0 ): #lift +

            print("Loop : %d\n" % loop_emotion)

            print("Physical Action Input is lift\n")

            diff_frequency[9] = old_input[1] - frequency[9]

            frequency[9] = old_input[1]

            arousal += lift_gain[0] * ((diff_frequency[9]*0.25) + (old_input[2]*0.5) + (old_input[4]*0.25)) # frequency / intensity / duration

            valence += lift_gain[1] * ((diff_frequency[9]*0.4) + (old_input[2]*0.4) + (old_input[4]*0.2)) 

            stance += lift_gain[2] * ((diff_frequency[9]*0.33) + (old_input[2]*0.33) + (old_input[4]*0.33)) 

        # IR ( type , frequency , intensity , area(position) , duration )

        # area 0 : face / area 1 : chin

        elif (old_input[0] == 0) and ( (old_input[1] // 200 ) % classification_stack[0] == 0 ) and (old_input[3] == 1) : #chin +++

            print("Loop : %d\n" % loop_emotion)

            print("Physical Action Input is Chin\n")

            diff_frequency[0] = old_input[1] - frequency[0]

            frequency[0] = old_input[1]

            arousal += chin_gain[0] * (diff_frequency[0]*0.5 + old_input[4]*0.5) 

            valence += chin_gain[1] * (diff_frequency[0]*0.2 + old_input[4]*0.8) 
 
            stance += chin_gain[2] * old_input[4]

        elif (old_input[0] == 2) and ( (old_input[1] // 200 ) %  classification_stack[2] == 0 and (old_input[3] == 0)): #say_hi +

            print("Loop : %d\n" % loop_emotion)

            print("Physical Action Input is Say Hi\n")

            diff_frequency[2] = old_input[1] - frequency[2]

            frequency[2] = old_input[1]

            arousal += say_hi_gain[0] * (diff_frequency[2]*0.5 + old_input[4]*0.5) 

            valence += say_hi_gain[1] * (diff_frequency[2]*0.2 + old_input[4]*0.8)

            stance += say_hi_gain[2] * old_input[4]

            message.pose = 'hello'

            message.intensity = 2

            message.loop = 3

            pub.publish(message)

            time.sleep(2)

        # Reflection 

        elif (old_input[0] == 1) and ( (old_input[1] // 100 ) % classification_stack[1] == 0 and (old_input[3] == 0)) : #close_eye -

            print("Loop : %d\n" % loop_emotion)

            print("Physical Action Input is Close eye\n")

            diff_frequency[1] = old_input[1] - frequency[1]

            frequency[1] = old_input[1]

            arousal += close_eye_gain[0] * (diff_frequency[1]*0.5 + old_input[4]*0.5) 

            valence += close_eye_gain[1] * (diff_frequency[1]*0.2 + old_input[4]*0.8) 

            stance += close_eye_gain[2] * old_input[4]

            message.pose = 'close_eye'

            message.intensity = 1

            message.loop = 1

            # face publich last value

            pub.publish(message)

            time.sleep(2)

        # Touch ( type , frequency , intensity , area(position) , duration )

        # area : 0 ( normally ) / area 1 : head 

        elif (old_input[0] == 3) and ( (old_input[1] // 10) % classification_stack[3] == 0 ) : #hug +++

            print("Loop : %d\n" % loop_emotion)

            print("Physical Action Input is Hug\n")

            diff_frequency[3] = old_input[1] - frequency[3]

            frequency[3] = old_input[1]

            arousal += hug_gain[0] * (old_input[3] + (diff_frequency[3]*0.2 + old_input[2]*0.6 + old_input[4]*0.2))

            valence += hug_gain[1] * (old_input[3] + (diff_frequency[3]*0.4 + old_input[2]*0.4 + old_input[4]*0.2))

            stance += hug_gain[2] * (old_input[3] + (diff_frequency[3]*0.2 + old_input[2]*0.2 + old_input[4]*0.6))

        elif (old_input[0] == 4) and ( (old_input[1] // 10 ) % classification_stack[4] == 0 ) : #pat +

            # specific have area 2 seperate from area 0

            if old_input[3] == 2 :

                print("Loop : %d\n" % loop_emotion)

                print("Physical Action Input is Tickle\n")

                diff_frequency[8] = old_input[1] - frequency[8]

                frequency[8] = old_input[1]

                arousal += tickle_gain[0] * (old_input[3] + (diff_frequency[8]*0.2 + old_input[2]*0.6 + old_input[4]*0.2))

                valence += tickle_gain[1] * (old_input[3] + (diff_frequency[8]*0.4 + old_input[2]*0.4 + old_input[4]*0.2))

                stance += tickle_gain[2] * (old_input[3] + (diff_frequency[8]*0.2 + old_input[2]*0.2 + old_input[4]*0.6))

                message.pose = 'tickle'

                message.intensity = 1

                message.loop = 2

                #message.face = 'happy1.jpg'

                pub.publish(message)

                time.sleep(2)

            else : 

                print("Loop : %d\n" % loop_emotion)

                print("Physical Action Input is Pat\n")

                diff_frequency[4] = old_input[1] - frequency[4]

                frequency[4] = old_input[1]

                arousal += pat_gain[0] * (old_input[3] + (diff_frequency[4]*0.2 + old_input[2]*0.6 + old_input[4]*0.2))

                valence += pat_gain[1] * (old_input[3] + (diff_frequency[4]*0.4 + old_input[2]*0.4 + old_input[4]*0.2))

                stance += pat_gain[2] * (old_input[3] + (diff_frequency[4]*0.2 + old_input[2]*0.2 + old_input[4]*0.6))
            
        elif (old_input[0] == 5) and ( (old_input[1] // 10) % classification_stack[5] == 0 ) : #slap ---

            print("Loop : %d\n" % loop_emotion)

            print("Physical Action Input is Slap\n")

            diff_frequency[5] = old_input[1] - frequency[5]

            frequency[5] = old_input[1]

            arousal += slap_gain[0] * (old_input[3] + (diff_frequency[5]*0.2 + old_input[2]*0.6 + old_input[4]*0.2))

            valence += slap_gain[1] * (old_input[3] + (diff_frequency[5]*0.4 + old_input[2]*0.4 + old_input[4]*0.2))

            stance += slap_gain[2] * (old_input[3] + (diff_frequency[5]*0.2 + old_input[2]*0.2 + old_input[4]*0.6))

        elif (old_input[0] == 6) and ( (old_input[1] // 10) % classification_stack[6] == 0 ) : #touch +

            if old_input[3] == 2 :

                print("Loop : %d\n" % loop_emotion)

                print("Physical Action Input is Tickle\n")

                diff_frequency[8] = old_input[1] - frequency[8]

                frequency[8] = old_input[1]

                arousal += tickle_gain[0] * (old_input[3] + (diff_frequency[8]*0.2 + old_input[2]*0.6 + old_input[4]*0.2))

                valence += tickle_gain[1] * (old_input[3] + (diff_frequency[8]*0.4 + old_input[2]*0.4 + old_input[4]*0.2))

                stance += tickle_gain[2] * (old_input[3] + (diff_frequency[8]*0.2 + old_input[2]*0.2 + old_input[4]*0.6))

                message.pose = 'tickle'

                message.intensity = 1

                message.loop = 2

                #message.face = 'happy1.jpg'

                pub.publish(message)

                time.sleep(2)

            else :

                print("Loop : %d\n" % loop_emotion)

                print("Physical Action Input is Touch\n")

                diff_frequency[6] = old_input[1] - frequency[6]

                frequency[6] = old_input[1]

                arousal += touch_gain[0] * (old_input[3] + (diff_frequency[6]*0.2 + old_input[2]*0.6 + old_input[4]*0.2))

                valence += touch_gain[1] * (old_input[3] + (diff_frequency[6]*0.4 + old_input[2]*0.4 + old_input[4]*0.2))

                stance += touch_gain[2] * (old_input[3] + (diff_frequency[6]*0.2 + old_input[2]*0.2 + old_input[4]*0.6))

        elif (old_input[0] == 7) and ( (old_input[1] // 10) % classification_stack[7] == 0 ) : #squeeze --

            print("Loop : %d\n" % loop_emotion)

            print("Physical Action Input is Squeeze\n")

            diff_frequency[7] = old_input[1] - frequency[7]

            frequency[7] = old_input[1]

            arousal += squeeze_gain[0] * (old_input[3] + (diff_frequency[7]*0.2 + old_input[2]*0.6 + old_input[4]*0.2))

            valence += squeeze_gain[1] * (old_input[3] + (diff_frequency[7]*0.4 + old_input[2]*0.4 + old_input[4]*0.2))

            stance += squeeze_gain[2] * (old_input[3] + (diff_frequency[7]*0.2 + old_input[2]*0.2 + old_input[4]*0.6))

        # Reflection

        else:
            
            print("Processing...\n")

        loop_emotion += 1
        
        #maximum(arousal,valence,stance)

        if arousal >= 1 :
    
            arousal = 1

        elif arousal <= -1 :

            arousal = -1

        else :

            arousal = arousal

        #print(arousal)

        if valence >= 1 :
        
            valence = 1

        elif valence <= -1 :
        
            valence = -1

        else :

            valence = valence

        #print(valence)

        if stance >= 1 :
        
            stance = 1

        elif stance <= -1 :
        
            stance = -1

        else :

            stance = stance

        #print(valence)

        process(Input,arousal,valence,stance)
        
    else : 

        #print('No entry!')

        #print(old_input)

        #print(Input)

        old_input = Input

        #print(old_input)

        #p.terminate()

def listener():

    rospy.init_node('From_Classificattion_DATA', anonymous=True)

    rospy.Subscriber("IMU_classification", classification_message , Emotion)

    rospy.Subscriber("IR_classification", classification_message , Emotion)

    rospy.Subscriber("touch_classification", classification_message , Emotion)

    rospy.spin()

if __name__ == '__main__':

    f = Figlet(font='standard')

    print(f.renderText("-------------"))

    print(f.renderText("HABIT OF MOMIU."))

    print(f.renderText("-------------"))

    listener()


