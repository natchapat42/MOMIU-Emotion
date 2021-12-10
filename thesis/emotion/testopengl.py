import numpy as np


import sys
import OpenGL.GL as gl
import OpenGL.GLUT as glut


winWidth,winHeight = 500,500

def sq():
    gl.glColor4f(1.0,1.0,1.0,1.0)
    gl.glEnable(gl.GL_TEXTURE_2D)
    
    gl.glBegin(gl.GL_QUADS) # Begin the sketch
    
    gl.glTexCoord2f(0.0, 1.0)

    gl.glVertex2f(0, 0) # Coordinates for the bottom left point
    
    gl.glTexCoord2f(1.0, 1.0)
    gl.glVertex2f(winWidth, 0) # Coordinates for the bottom right point
    
    gl.glTexCoord2f(1.0, 0.0)
    gl.glVertex2f(winWidth, winHeight) # Coordinates for the top right point
    
    gl.glTexCoord2f(0.0, 0.0)
    gl.glVertex2f(0, winHeight) # Coordinates for the top left point
    gl.glEnd() # Mark the end of drawing
    gl.glDisable(gl.GL_TEXTURE_2D)
    
def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT) # Remove everything from screen (i.e. displays all white)
    
    gl.glMatrixMode (gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    sq()
    glut.glutSwapBuffers()

def reshape(width,height):
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    
def keyboard( key, x, y ):
    if key == b'\x1b':
        sys.exit( )

glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow('Hello world!')
glut.glutReshapeWindow(winWidth,winHeight)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)

glut.glutMainLoop()