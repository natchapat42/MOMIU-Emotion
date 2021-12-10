import math

import random

# Input from Classification_node

# 1. Type (String) :  เกาคาง , หลับตา , ทักทาย , กอด , ลูบ , ตบ , เเตะ , บีบ , จั๊กจี้ , เขย่า , ยก
# 2. Intensity (Integer)
# 3. Frequency (Integer)
# 4. Area (Integer)
# 5. Duration (Float)

# Input from Emotion_node

# 6. Emotion state (for blending emotion)

happy = [0.4,0.7,0]

angry = [-0.8,-0.6,0]

confuse = [0.5,0.2,0]

sad = [-0.5,-0.3,0]

natural = [0,0,0]

sleepy = [-0.7,0.4,0]

action = [happy , angry , confuse , sad , natural , sleepy]

action_callback = { 0 : "happy" , 1 : "angry" , 2 : "confuse" , 3 : "sad" , 4 : "natural" , 5 : "sleepy" }

# 7. Habits (Initial Value) 

bother = (0.8,0.6,0.3)

polite = (-0.5,-0.2,-0.4)

habits = polite

# No Data = None

# Initial State = Natural

touch_classification = { "เกาคาง" : 1 , "หลับตา" : 2 , "ทักทาย" : 3 , "hug" : 4 , "ลูบ" : 5 , 
                         "ตบ" : 6 , "แตะ" : 7 , "บีบ" : 8 , "จั๊กจี้" : 9 , "เขย่า" : 10 , "ยก" : 11}

# Touch_classification_gain

เกาคาง_gain = [0.12,0.15,0.1]

หลับตา_gain = [0.08,-0.1,-0.1]

ทักทาย_gain = [0.08,0.1,0.1]

กอด_gain = [0.12,0.07,0.2]

ลูบ_gain = [0.03,0.04,0.03]

ตบ_gain = [0.06,-0.05,-0.05]

แตะ_gain = [0.02,0.02,0.04]

บีบ_gain = [0.05,-0.04,-0.04]

จั๊กจี้_gain = [0.12,-0.1,-0.15]

เขย่า_gain = [0,0,0]

ยก_gain = [0,0,0]

####################################################################################

Input = ["แตะ",3,1,2,5]

# Part 1 Emotion

def Emotion(Input):

    Input[0] = touch_classification[Input[0]] # convert string to integer for calculation

    # Emotion = [Arousal,Valence,Stance]

    # Action

    if Input[0] == 1 : #เกาคาง

        arousal = เกาคาง_gain[0] * Input[2] 

        valence = เกาคาง_gain[1] * Input[4]

        stance = เกาคาง_gain[2] * Input[2]

    elif Input[0] == 3 : #ทักทาย

        arousal = ทักทาย_gain[0] * Input[2] 

        valence = ทักทาย_gain[1] * Input[4]

        stance = ทักทาย_gain[2] * Input[2]

    elif Input[0] == 4 : #กอด

        arousal = กอด_gain[0] * (Input[2] + Input[4])

        valence = กอด_gain[1] * (Input[1] + Input[4])

        stance = กอด_gain[2] * ((Input[1] + Input[2] + Input[4]) / 3 )

    elif Input[0] == 5 : #ลูบ

        arousal = ลูบ_gain[0] * ( Input[1] + Input[4] )

        valence = ลูบ_gain[1] * ( Input[2] + Input[4] )

        stance = ลูบ_gain[2] * ((Input[1] + Input[2] + Input[4]) / 3 )
    
    elif Input[0] == 6 : #ตบ

        arousal = ตบ_gain[0] * ( Input[1] + Input[4] )

        valence = ตบ_gain[1] * ( Input[1] + Input[4] )

        stance = ตบ_gain[2] * ((Input[1] + Input[2] + Input[4]) / 3 )

    elif Input[0] == 7 : #เเตะ

        arousal = แตะ_gain[0] * ( Input[1] + Input[4] )

        valence = แตะ_gain[1] * ( Input[1] + Input[4] )

        stance = แตะ_gain[2] * ((Input[1] + Input[2] + Input[4]) / 3 )

    elif Input[0] == 8 : #บีบ

        arousal = บีบ_gain[0] * ( Input[1] + Input[4] )

        valence = บีบ_gain[1] * ( Input[1] + Input[4] )

        stance = บีบ_gain[2] * ((Input[1] + Input[2] + Input[4]) / 3 )
    
    elif Input[0] == 10 : #เขย่า

        print("เขย่า")

    elif Input[0] == 11: #ยก

        print("ยก")
    
    # Reflection

    elif Input[0] == 2 : #หลับตา

        arousal += หลับตา_gain[0] * Input[2] 

        valence += หลับตา_gain[1] 

        stance += หลับตา_gain[2] * Input[2]

    elif Input[0] == 9 and Input[3] == 2 : #จั๊กจี้

        arousal += จั๊กจี้_gain[0] * ( Input[1] + Input[4] )

        valence += จั๊กจี้_gain[1] * Input[2]

        stance += จั๊กจี้_gain[2] * ((Input[1] + Input[2] + Input[4]) / 3 )

    # Check

    # print("arousal= " + str(arousal))

    # print("valence= " + str(valence))

    # print("stance= " + str(stance))

    # Find nearest value

    distance = []

    for i in range(0,6) :

        distance.append(math.sqrt((arousal-action[i][0])**2+(valence-action[i][1])**2)) # Find nearest distance

    nearest = min(distance) # Find min values of nearest distance

    min_index = distance.index(nearest) # Find index of min values

    # print(min_index)

# Part 2 Blending

    print("Current emotion is " + action_callback[min_index]) # convert interger to string

    old_emotion = natural # emotion k - 1

    current_emotion = [arousal,valence,stance] # emotion k

    # Find emotion average between emotion (k-1,k)

    blending_emotion = [(( habits[0] + current_emotion[0] + old_emotion[0] ) / 3 ) , (( habits[1] + current_emotion[1] + old_emotion[1] ) / 3 ) ,(( current_emotion[2] + old_emotion[2] ) / 3 ) ]

    distance_blending = []

    for i in range(0,6) :

        distance_blending.append(math.sqrt((blending_emotion[0]-action[i][0])**2 + (blending_emotion[1]-action[i][1])**2)) # Find nearest distance for blending

    nearest_blending = min(distance_blending) # Find min values of nearest distance

    min_index_blending = distance_blending.index(nearest_blending) # Find index of min values

    print("Blending emotion is " + action_callback[min_index_blending]) # convert interger to string

    ###

    old_emotion = blending_emotion # emotion state k >> emotion state k-1

    print(blending_emotion)

# Part 3 Habits 

    emotion_stance = ( blending_emotion[2] + habits[2] ) / 2

    print(emotion_stance)

    # find intensity in each action

    if emotion_stance < 0.33 :

        emotion_intensity = 1

        duration = random.uniform(0, 1)

    elif emotion_stance > 0.33 and emotion_stance <= 0.67 :

        emotion_intensity = 2

        duration = random.uniform(1, 2.5)

    elif emotion_stance < 0.67 :

        emotion_intensity = 3

        duration = random.uniform(2.5, 4)

# Output

    print(action_callback[min_index_blending]) #

    print('intensity = ' + str(emotion_intensity))

    print('duration = ' + str(duration))

Emotion(Input)



