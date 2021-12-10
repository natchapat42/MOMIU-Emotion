#!/usr/bin/python3

import pygame
import pandas as pd
import numpy , sys , time

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from pyfiglet import Figlet

import rospy

from message.msg import pose_message

from PIL import Image as Image

class momiu_emotion:
    
    def __init__(self,R,L,position,face,loop,color):

        self.R = R

        self.L = L

        self.data_pose = position # number of data point

        self.face = face # face

        self.loop = loop

        self.color = color

    def run(self):

        glClearColor(0,0,0,0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)

        # rectangle #

        glPushMatrix()
        
        glColor3f(self.color[0], self.color[1], self.color[2])

        glRotatef(90,1,0,0)

        glRotatef(180,0,0,1)

        glRotatef(180,0,1,0)

        glutSolidCube(5)

        glPopMatrix()

        glutSwapBuffers()


        # Head

        glPushMatrix()
        
        glColor3f(self.color[0], self.color[1], self.color[2])

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
        glColor3f(self.color[0], self.color[1], self.color[2])

        glTranslatef(-6.5,16.5,0)
        glRotatef(-90,1,0,0)

        glutWireCone(4,7,20,20)
        #glutSolidCone(,20,20)
        glPopMatrix()
        glutSwapBuffers()

        # Right Top Ear

        glPushMatrix()
        glColor3f(self.color[0], self.color[1], self.color[2])

        glTranslatef(6.5,16.5,0)
        glRotatef(-90,1,0,0)

        glutWireCone(4,7,20,20)
        #glutSolidCone(,20,20)
        glPopMatrix()
        glutSwapBuffers()

        # Bot Ear

        #self.statics()

        self.dynamics()

        #glutDestroyWindow(win)

    def statics(self):

        # statics show

        for i in range(1,12) :

            glPushMatrix()
            glColor3f(self.color[0], self.color[1], self.color[2])

            glTranslatef(self.R[i-1][1],self.R[i-1][2],self.R[i-1][0])
            glutSolidSphere(4,10,10)

            glPopMatrix()
            glutSwapBuffers()

            glPushMatrix()
            glColor3f(self.color[0], self.color[1], self.color[2])

            glTranslatef(self.L[i-1][1],self.L[i-1][2],self.L[i-1][0])
            glutSolidSphere(4,10,10)

            glPopMatrix()
            glutSwapBuffers() 

    def dynamics(self):

        # Dynamic simulation

        for i in range(0,self.loop):

            for i in range(1,self.data_pose + 2) :

                glPushMatrix()

                glColor3f(self.color[0], self.color[1], self.color[2])

                #print("number " , i)

                #print(momiu.R[50][2])

                if ( momiu.R[12][2] == -3.54 ) and ( momiu.R[50][2] == -5.76 ) :

                    glTranslatef((self.R[i-1][1])-3,self.R[i-1][2]-12.5,self.R[i-1][0])
                    glutSolidSphere(3,10,10)

                    glPopMatrix()
                    glutSwapBuffers()

                    glPushMatrix()
                    glColor3f(self.color[0], self.color[1], self.color[2])

                    glTranslatef((self.L[i-1][1])+3,self.L[i-1][2]-12.5,self.L[i-1][0])
                    glutSolidSphere(3,10,10)

                else :

                    glTranslatef((self.R[i-1][0]/8)-1,((self.R[i-1][2]/13)+15)*-1,(self.R[i-1][1]/9)) # x y z
                    glutSolidSphere(3,10,10)

                    glPopMatrix()
                    glutSwapBuffers()

                    glPushMatrix()
                    glColor3f(self.color[0], self.color[1], self.color[2])

                    glTranslatef((self.L[i-1][0]/8)+1,((self.L[i-1][2]/13)+15)*-1,(self.L[i-1][1]/9))
                    glutSolidSphere(3,10,10)

                #print("sdokhfskljdfjk")

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

                    # Head

                    glPushMatrix()
                    glColor3f(self.color[0], self.color[1], self.color[2])

                    glRotatef(90,1,0,0)

                    glRotatef(180,0,0,1)

                    glRotatef(180,0,1,0)

                    tex = self.read_texture(self.face)
                    qobj = gluNewQuadric()
                    gluQuadricTexture(qobj, GL_TRUE)
                    glEnable(GL_TEXTURE_2D)
                    glBindTexture(GL_TEXTURE_2D, tex)

                    gluSphere(qobj, 20, 100, 10)

                    glDisable(GL_TEXTURE_2D)

                    glPopMatrix()
                    glutSwapBuffers()

                    # Left Top Ear

                    glPushMatrix()
                    glColor3f(self.color[0], self.color[1], self.color[2])

                    glTranslatef(-7.5,16.5,0)
                    glRotatef(-90,1,0,0)

                    #glutWireCone(4,7,20,20)
                    glutSolidCone(4,7,20,20)
                    glPopMatrix()
                    glutSwapBuffers()

                    # Right Top Ear

                    glPushMatrix()
                    glColor3f(self.color[0], self.color[1], self.color[2])

                    glTranslatef(7.5,16.5,0)
                    glRotatef(-90,1,0,0)

                    #glutWireCone(4,7,20,20)
                    glutSolidCone(4,7,20,20)
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

        # for MOMIU face in simulation
        
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

def keyboard(key, x, y):

    # check function

    #print(key)

    if key == b'\x1b':

        sys.exit()

    elif key == b'r':

        momiu.L = pd.read_csv('left_tickle.csv',header=None)

        momiu.R = pd.read_csv('right_tickle.csv',header=None)

        momiu.face = 'natural.jpg'
        
        momiu.data_pose = 54

        glutPostRedisplay()

def main(data):

    #print(momiu.R)

    #print(momiu.R[3][2])

    # Set Simulation depend on input 

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

        momiu.color = (0.96,0.95,0.55)

    elif data.pose == 'sad':
    
        momiu.R = pd.read_csv('right_sad.csv',header=None)

        momiu.L = pd.read_csv('left_sad.csv',header=None)

        #momiu.face = data.face #momiu.face = 'sad2.jpg'

        momiu.data_pose = 54

        momiu.color = (0.23,0.34,0.78)

    elif data.pose == 'natural':
    
        momiu.R = pd.read_csv('right_tickle.csv',header=None)

        momiu.L = pd.read_csv('left_tickle.csv',header=None)

        #momiu.face = data.face #momiu.face = 'natural.jpg'

        momiu.data_pose = 54

        momiu.color = (1,1,1)

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

        momiu.color = (1,0.54,0.54)

    elif data.pose == 'surprise':
    
        momiu.R = pd.read_csv('right_tickle.csv',header=None)

        momiu.L = pd.read_csv('left_tickle.csv',header=None)

        momiu.face = data.face 

        momiu.data_pose = 54

        momiu.color = (1,0.78,0.54)

    elif data.pose == 'close_eye': 

        print('close_eye')

        momiu.R = momiu.R

        momiu.L = momiu.L

        momiu.face = momiu.face

        momiu.data_pose = momiu.data_pose

        momiu.color = momiu.color

    else : 

        momiu.R = pd.read_csv('right_think.csv',header=None)

        momiu.L = pd.read_csv('left_think.csv',header=None)

        momiu.face = 'confuse.jpg'

        momiu.data_pose = 54

        momiu.color = (0.82,0.58,0.82)

    momiu.face = data.face

    momiu.loop = data.loop

    glutPostRedisplay() # Play run() function again ; but change parameter

if __name__ == "__main__":

    # Set up

    rospy.init_node('momiu_emotion', anonymous=True)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800,800)
    glutInitWindowPosition(1200,0)
    win = glutCreateWindow('MOMIU')

    RRR = pd.read_csv('right_tickle.csv',header=None)

    LLL = pd.read_csv('left_tickle.csv',header=None)

    momiu = momiu_emotion(RRR,LLL,54,'natural.jpg',1,(1,1,1))

    momiu.light()

    glMatrixMode(GL_PROJECTION)
    
    glLoadIdentity()

    gluPerspective(30,1,1,1000)

    glTranslate(0,0,-200)

    # # Display

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    # Run Simulation
    
    glutDisplayFunc(momiu.run)
    
    # # push and pop the current matrix stack

    # Check function from key board

    glutKeyboardFunc(keyboard)

    rospy.Subscriber("pose", pose_message , main)

    glutMainLoop()

    rospy.spin()

 

    