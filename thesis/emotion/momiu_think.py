#!/usr/bin/python3

import pygame
import pandas as pd
import numpy , sys , time

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image as Image

R = pd.read_csv('right_think.csv',header=None)

L = pd.read_csv('left_think.csv',header=None)

def run():

    glClearColor(0,0,0,0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    # Head

    glPushMatrix()
    
    glColor3f(1.0, 0.5, 0.0)

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
    glColor3f(1.0, 0.5, 0.0)

    glTranslatef(-7.5,17.5,0)
    glRotatef(-90,1,0,0)

    glutWireCone(4,7,20,20)
    #glutSolidCone(,20,20)
    glPopMatrix()
    glutSwapBuffers()

    # Right Top Ear

    glPushMatrix()
    glColor3f(1.0, 0.5, 0.0)

    glTranslatef(7.5,17.5,0)
    glRotatef(-90,1,0,0)

    glutWireCone(4,7,20,20)
    #glutSolidCone(,20,20)
    glPopMatrix()
    glutSwapBuffers()

    # Bot Ear

    #statics()

    dynamics()

    axis()

def statics():

    global R

    global L

    for i in range(1,12) :

        glPushMatrix()
        glColor3f(1.0, 0.5, 0.0)

        glTranslatef(R[i-1][1],R[i-1][2],R[i-1][0])
        glutSolidSphere(4,10,10)

        glPopMatrix()
        glutSwapBuffers()

        glPushMatrix()
        glColor3f(1.0, 0.5, 0.0)

        glTranslatef(L[i-1][1],L[i-1][2],L[i-1][0])
        glutSolidSphere(4,10,10)

        glPopMatrix()
        glutSwapBuffers() 

def dynamics():

    global R

    global L

    for i in range(1,56) :

        glPushMatrix()
        glColor3f(1.0, 0.5, 0.0)

        glTranslatef(R[i-1][0]/8,((R[i-1][2]/13))*-1,(R[i-1][1]/9)) # x y z
        glutSolidSphere(4,10,10)

        glPopMatrix()
        glutSwapBuffers()

        glPushMatrix()
        glColor3f(1.0, 0.5, 0.0)

        glTranslatef(L[i-1][0]/8,(L[i-1][2]/13)*-1,(L[i-1][1]/9))
        glutSolidSphere(4,10,10)

        glPopMatrix()
        glutSwapBuffers() 

        if i % 11 == 0 :

            if i == 55 :

                break

            glClearColor(0,0,0,0)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)

            time.sleep(0.05)

            # Head

            glPushMatrix()
            glColor3f(1.0, 0.5, 0.0)

            glRotatef(90,1,0,0)

            glRotatef(180,0,0,1)

            glRotatef(180,0,1,0)

            tex = read_texture('a.jpeg')
            qobj = gluNewQuadric()
            gluQuadricTexture(qobj, GL_TRUE)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, tex)

            gluSphere(qobj, 20, 20, 20)

            glDisable(GL_TEXTURE_2D)

            glPopMatrix()
            glutSwapBuffers()

            # Left Top Ear

            glPushMatrix()
            glColor3f(1.0, 0.5, 0.0)

            glTranslatef(-7.5,17.5,0)
            glRotatef(-90,1,0,0)

            #glutWireCone(4,7,20,20)
            glutSolidCone(4,7,20,20)
            glPopMatrix()
            glutSwapBuffers()

            # Right Top Ear

            glPushMatrix()
            glColor3f(1.0, 0.5, 0.0)

            glTranslatef(7.5,17.5,0)
            glRotatef(-90,1,0,0)

            #glutWireCone(4,7,20,20)
            glutSolidCone(4,7,20,20)
            glPopMatrix()
            glutSwapBuffers()

def axis():

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

def read_texture(filename):
    
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

def light():

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

def main():
    
    # Screen

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800,800)
    glutInitWindowPosition(1200,0)
    glutCreateWindow('MOMIU')

    light()

    glMatrixMode(GL_PROJECTION)
    
    glLoadIdentity()

    gluPerspective(30,1,1,1000)

    glTranslate(0,0,-200)

    # Display

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    
    glutDisplayFunc(run)
    
    # push and pop the current matrix stack
    
    glutMainLoop()

if __name__ == "__main__":
    
    main()

    