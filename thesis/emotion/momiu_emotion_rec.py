#!/usr/bin/python3

import pygame
import pandas as pd
import numpy , sys , time

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import rospy

from message.msg import pose_message

from PIL import Image as Image

class momiu_emotion:
    
    def __init__(self,R,L,position,face,loop):

        self.R = R

        self.L = L

        self.data_pose = position # number of data point

        self.face = face # face

        self.loop = loop        

    def sq(self):

        winWidth,winHeight = 100,100

        glColor4f(1.0,1.0,1.0,1.0)
        glEnable(GL_TEXTURE_2D)
        
        glBegin(GL_QUADS) # Begin the sketch
        
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0, 0) # Coordinates for the bottom left point
        
        glTexCoord2f(1.0, 1.0)
        glVertex2f(winWidth, 0) # Coordinates for the bottom right point
        
        glTexCoord2f(1.0, 0.0)
        glVertex2f(winWidth, winHeight) # Coordinates for the top right point
        
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0, winHeight) # Coordinates for the top left point

        glEnd() # Mark the end of drawing
        glDisable(GL_TEXTURE_2D)

    def run(self):
    
        glClearColor(0,0,0,0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)

        # face rectangle #

        '''

        glPushMatrix()
        
        glColor3f(0, 0, 0)

        glRotatef(90,1,0,0)

        glRotatef(180,0,0,1)

        glRotatef(180,0,1,0)

        glTranslatef(0,-20,0) # x y z normally =  x z -y

        glScalef(5,0,3.5)

        glutSolidCube(5)

        glPopMatrix()

        glutSwapBuffers()
    
        '''


        glPushMatrix()

        self.sq()

        glPopMatrix()

        glutSwapBuffers()

        # Head

        glPushMatrix()
        
        glColor3f(1, 1, 1)

        glRotatef(90,1,0,0)

        glRotatef(180,0,0,1)

        glRotatef(180,0,1,0)

        #tex = read_texture('a.jpeg')
        qobj = gluNewQuadric()
        gluQuadricTexture(qobj, GL_TRUE)
        #glEnable(GL_TEXTURE_2D)
        #glBindTexture(GL_TEXTURE_2D, tex)

        gluSphere(qobj, 20, 20, 20)

        #glDisable(GL_TEXTURE_2D)

        glPopMatrix()

        glutSwapBuffers()

        # Left Top Ear

        glPushMatrix()
        glColor3f(0, 1, 1)

        glTranslatef(-6.5,17.5,0)
        glRotatef(-90,1,0,0)

        glutWireCone(4,7,20,20)
        #glutSolidCone(,20,20)
        glPopMatrix()
        glutSwapBuffers()

        # Right Top Ear

        glPushMatrix()
        glColor3f(0, 1, 1)

        glTranslatef(6.5,17.5,0)
        glRotatef(-90,1,0,0)

        glutWireCone(4,7,20,20)
        #glutSolidCone(,20,20)
        glPopMatrix()
        glutSwapBuffers()

        # Bot Ear

        #statics()

        self.dynamics()

        #glutDestroyWindow(win)

    def statics(self):

        for i in range(1,12) :

            glPushMatrix()
            glColor3f(0, 1, 1)

            glTranslatef(self.R[i-1][1],self.R[i-1][2],self.R[i-1][0])
            glutSolidSphere(4,10,10)

            glPopMatrix()
            glutSwapBuffers()

            glPushMatrix()
            glColor3f(0, 1, 1)

            glTranslatef(self.L[i-1][1],self.L[i-1][2],self.L[i-1][0])
            glutSolidSphere(4,10,10)

            glPopMatrix()
            glutSwapBuffers() 

    def dynamics(self):

        for i in range(0,self.loop):

            for i in range(1,self.data_pose + 2) :

                glPushMatrix()
                glColor3f(0, 1, 1)

                print("number " , i)

                print(momiu.R[50][2])

                if ( momiu.R[12][2] == -3.54 ) and ( momiu.R[50][2] == -5.76 ) :

                    glTranslatef((self.R[i-1][1])-3,self.R[i-1][2]-12.5,self.R[i-1][0])
                    glutSolidSphere(3,10,10)

                    glPopMatrix()
                    glutSwapBuffers()

                    glPushMatrix()
                    glColor3f(0, 1, 1)

                    glTranslatef((self.L[i-1][1])+3,self.L[i-1][2]-12.5,self.L[i-1][0])
                    glutSolidSphere(3,10,10)

                else :

                    glTranslatef((self.R[i-1][0]/8)-1,((self.R[i-1][2]/13)+15)*-1,(self.R[i-1][1]/9)) # x y z
                    glutSolidSphere(3,10,10)

                    glPopMatrix()
                    glutSwapBuffers()

                    glPushMatrix()
                    glColor3f(0, 1, 1)

                    glTranslatef((self.L[i-1][0]/8)+1,((self.L[i-1][2]/13)+15)*-1,(self.L[i-1][1]/9))
                    glutSolidSphere(3,10,10)

                print("sdokhfskljdfjk")

                glPopMatrix()
                glutSwapBuffers() 

                if i % 11 == 0 :

                    if i == (self.data_pose + 1) :

                        time.sleep(0.5)

                        break

                    glClearColor(0,0,0,0)
                    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                    glMatrixMode(GL_MODELVIEW)

                    time.sleep(0.05)

                    # face rectangle

                    glPushMatrix()
                    glColor3f(0, 1, 1)

                    glRotatef(90,1,0,0)

                    glRotatef(180,0,0,1)

                    glRotatef(180,0,1,0)

                    glTranslatef(0,-20,0) # x y z normally =  x z -y

                    tex = self.read_texture(self.face)
                    glEnable(GL_TEXTURE_2D)
                    glBindTexture(GL_TEXTURE_2D, tex)

                    #glScalef(5,0,3.5)

                    #glutSolidCube(5)

                    self.sq()

                    #gluSphere(qobj,50,20,20)

                    glDisable(GL_TEXTURE_2D)

                    glPopMatrix()
                    glutSwapBuffers()

                    # head

                    glPushMatrix()
                    
                    glColor3f(0.66, 0.66, 0.66)

                    glRotatef(90,1,0,0)

                    glRotatef(180,0,0,1)

                    glRotatef(180,0,1,0)

                    qobj = gluNewQuadric()
                    gluQuadricTexture(qobj, GL_TRUE)

                    gluSphere(qobj, 20, 20, 20)

                    glPopMatrix()

                    glutSwapBuffers()

                    # Left Top Ear

                    glPushMatrix()
                    glColor3f(0, 1, 1)

                    glTranslatef(-6.5,17.5,0)
                    glRotatef(-90,1,0,0)

                    glutWireCone(4,7,20,20)
                    #glutSolidCone(,20,20)
                    glPopMatrix()
                    glutSwapBuffers()

                    # Right Top Ear

                    glPushMatrix()
                    glColor3f(0, 1, 1)

                    glTranslatef(6.5,17.5,0)
                    glRotatef(-90,1,0,0)

                    glutWireCone(4,7,20,20)
                    #glutSolidCone(,20,20)
                    glPopMatrix()
                    glutSwapBuffers()

    def axis(self):

        # check Axis X

        glPushMatrix()
        glColor3f(1.0, 0.0 , 0.0)
        glRotatef(90,0,1,0)
        glTranslatef(0,0,0)
        #glutWireCylinder(0.1,5,10,10)
        glutSolidCylinder(0.1,5,10,10)
        glPopMatrix()
        glutSwapBuffers()

        # check Axis Y

        glPushMatrix()
        glColor3f(0.0, 1.0 , 0.0)
        glRotatef(-90,1,0,0)
        glTranslatef(0,0,0)
        #glutWireCylinder(0.1,5,10,10)
        glutSolidCylinder(0.1,5,10,10)
        glPopMatrix()
        glutSwapBuffers()

        # check Axis Z

        glPushMatrix()
        glColor3f(0.0, 0.0 , 1.0)
        glRotatef(90,0,0,1)
        glTranslatef(0,0,0)
        #glutWireCylinder(0.1,5,10,10)
        glutSolidCylinder(0.1,5,10,10)
        glPopMatrix()
        glutSwapBuffers()

    def read_texture(self,filename):
        
        img = Image.open(filename)

        img_data = img.tobytes("raw", "RGBX", 0, -1)

        textID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textID) 
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return textID

    def light(self):

        # enable light mode
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        # set light color and ambient

        ambientLight = [0.2, 0.2, 0.2, 1.0 ] # RGB and alpha channels
        diffuseLight = [0.8, 0.8, 0.8, 1.0 ] # RGB and alpha channels
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        
        # set light source position
        # x, y, z, alpha

        position = [ 50, 50.0, 0.0, 1.0 ]
        glLightfv(GL_LIGHT0, GL_POSITION, position)

    def read(self):

        print('xewrwer')

def keyboard(key, x, y):

    print(key)

    if key == b'\x1b':

        sys.exit()

    elif key == b'r':

        momiu.L = pd.read_csv('left_tickle.csv',header=None)

        momiu.R = pd.read_csv('right_tickle.csv',header=None)

        momiu.face = 'natural.jpg'
        
        momiu.data_pose = 54

        glutPostRedisplay()

def main(data):

    print(data)

    # Screen

    print('fuckkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')

    print(momiu.R)

    print(momiu.R[3][2])

    if data.pose == 'hello' :

        momiu.R = pd.read_csv('right_hello.csv',header=None)

        momiu.L = pd.read_csv('left_hello.csv',header=None)

        #momiu.face = data.face #momiu.face = 'natural.jpg'

        momiu.data_pose = 54

        #print(momiu.R[12][2])

        #print(momiu.R[50][2])

    elif data.pose == 'happy':
    
        momiu.R = pd.read_csv('right_happy.csv',header=None)

        momiu.L = pd.read_csv('left_happy.csv',header=None)

        #momiu.face = data.face #momiu.face = 'happy1.jpg'

        momiu.data_pose = 109

    elif data.pose == 'sad':
    
        momiu.R = pd.read_csv('right_sad.csv',header=None)

        momiu.L = pd.read_csv('left_sad.csv',header=None)

        #momiu.face = data.face #momiu.face = 'sad2.jpg'

        momiu.data_pose = 54

    elif data.pose == 'natural':
    
        momiu.R = pd.read_csv('right_tickle.csv',header=None)

        momiu.L = pd.read_csv('left_tickle.csv',header=None)

        #momiu.face = data.face #momiu.face = 'natural.jpg'

        momiu.data_pose = 54

    elif data.pose == 'tickle':
    
        momiu.R = pd.read_csv('right_tickle.csv',header=None)

        momiu.L = pd.read_csv('left_tickle.csv',header=None)

        #momiu.face = data.face #momiu.face = 'happy2.jpg'

        momiu.data_pose = 54

    elif data.pose == 'angry':
    
        momiu.R = pd.read_csv('right_angry.csv',header=None)

        momiu.L = pd.read_csv('left_angry.csv',header=None)

        #momiu.face = data.face #momiu.face = 'angry2.jpg'

        momiu.data_pose = 54

    #elif data.pose == 'angry':
    
        #momiu.R = pd.read_csv('right_angry.csv',header=None)

        #momiu.L = pd.read_csv('left_angry.csv',header=None)

        #momiu.face = data.face #momiu.face = 'angry2.jpg'

        #momiu.data_pose = 54'''

    elif data.pose == 'close_eye': 

        print('close_eye')

    else : 

        momiu.R = pd.read_csv('right_think.csv',header=None)

        momiu.L = pd.read_csv('left_think.csv',header=None)

        #momiu.face = data.face #momiu.face = 'confuse.jpg'

        momiu.data_pose = 54

    momiu.face = data.face

    momiu.loop = data.loop

    glutPostRedisplay()

    print('yyyyyyyyy')

if __name__ == "__main__":

    #main()

    #print(data)

    rospy.init_node('momiu_emotion', anonymous=True)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800,800)
    glutInitWindowPosition(1200,0)
    win = glutCreateWindow('MOMIU')

    RRR = pd.read_csv('right_tickle.csv',header=None)

    LLL = pd.read_csv('left_tickle.csv',header=None)

    # Right / left / pose_number / face / loop

    momiu = momiu_emotion(RRR,LLL,54,'ฟฟฟ.jpg',1)

    print(RRR)

    momiu.light()

    glMatrixMode(GL_PROJECTION)
    
    glLoadIdentity()

    gluPerspective(30,1,1,1000)

    glTranslate(0,0,-200)

    # # Display

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    
    glutDisplayFunc(momiu.run)

    print("564564564")

    #glutIdleFunc(momiu.read)
    
    # # push and pop the current matrix stack

    glutKeyboardFunc(keyboard)

    rospy.Subscriber("pose", pose_message , main)

    glutMainLoop()

    rospy.spin()

 

    