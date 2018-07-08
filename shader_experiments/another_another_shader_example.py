# Pygame/PyopenGL example by Bastiaan Zapf, Apr 2009
#
# Draw a range of cubes, light them prettily
#
# Employed techniques: 
#
# - Vertex and Fragment shaders
# - Lightsource variables
# - Display Lists


from OpenGL.GL import *
from OpenGL.GLU import *
import random
from math import * # trigonometry

import pygame # just to get a display

import Image
import sys
import time

# get an OpenGL surface

pygame.init() 
pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

def jpg_file_write(name, number, data):
    im = Image.frombuffer("RGBA", (800,600), data, "raw", "RGBA", 0, 0)
    fnumber = "%05d" % number
    im.save(name + fnumber + ".jpg")


glEnable(GL_DEPTH_TEST)

# Create and Compile a shader
# but fail with a meaningful message if something goes wrong

def createAndCompileShader(type,source):
    shader=glCreateShader(type)
    glShaderSource(shader,source)
    glCompileShader(shader)

    # get "compile status" - glCompileShader will not fail with 
    # an exception in case of syntax errors

    result=glGetShaderiv(shader,GL_COMPILE_STATUS)

    if (result!=1): # shader didn't compile
        raise Exception("Couldn't compile shader\nShader compilation Log:\n"+glGetShaderInfoLog(shader))
    return shader

# Create and Compile fragment and vertex shaders
# Transfer data from fragment to vertex shader

vertex_shader=createAndCompileShader(GL_VERTEX_SHADER,"""
varying vec3 v;
varying vec3 N;

void main(void)
{

   v = gl_ModelViewMatrix * gl_Vertex;
   N = gl_NormalMatrix * gl_Normal;

   gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

}
""");

fragment_shader=createAndCompileShader(GL_FRAGMENT_SHADER,"""
varying vec3 N;
varying vec3 v;

void main(void)
{
   vec3 L = gl_LightSource[0].position.xyz-v;

   // "Lambert's law"? (see notes)
   // Rather: faces will appear dimmer when struck in an acute angle
   // distance attenuation

   float Idiff = max(dot(normalize(L),N),0.0)*pow(length(L),-2.0); 

   gl_FragColor = vec4(0.5,0,0.5,1.0)+ // purple
                  vec4(1.0,1.0,1.0,1.0)*Idiff; // diffuse reflection
}
""");

# build shader program

program=glCreateProgram()
glAttachShader(program,vertex_shader)
glAttachShader(program,fragment_shader)
glLinkProgram(program)

# try to activate/enable shader program
# handle errors wisely

try:
    glUseProgram(program)   
except OpenGL.error.GLError:
    print glGetProgramInfoLog(program)
    raise

done = False

t=0 

# load a cube into a display list

glNewList(1,GL_COMPILE)

glBegin(GL_QUADS)

glColor3f(1,1,1)

glNormal3f(0,0,-1)
glVertex3f( -1, -1, -1)
glVertex3f(  1, -1, -1)
glVertex3f(  1,  1, -1)
glVertex3f( -1,  1, -1)

glNormal3f(0,0,1)
glVertex3f( -1, -1,  1)
glVertex3f(  1, -1,  1)
glVertex3f(  1,  1,  1)
glVertex3f( -1,  1,  1)

glNormal3f(0,-1,0) 
glVertex3f( -1, -1, -1)
glVertex3f(  1, -1, -1)
glVertex3f(  1, -1,  1)
glVertex3f( -1, -1,  1)

glNormal3f(0,1,0) 
glVertex3f( -1,  1, -1)
glVertex3f(  1,  1, -1)
glVertex3f(  1,  1,  1)
glVertex3f( -1,  1,  1)

glNormal3f(-1,0,0)     
glVertex3f( -1, -1, -1)
glVertex3f( -1,  1, -1)
glVertex3f( -1,  1,  1)
glVertex3f( -1, -1,  1)                      

glNormal3f(1,0,0)        
glVertex3f(  1, -1, -1)
glVertex3f(  1,  1, -1)
glVertex3f(  1,  1,  1)
glVertex3f(  1, -1,  1)

glEnd()
glEndList()

while not done:

    t=t+1

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90,1,0.01,1000)
    gluLookAt(sin(t/260.0)*4,cos(t/260.0)*4,cos(t/687.0)*3,0,0,0,0,1,0)
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)

    # calculate light source position

    ld=[sin(t/16.0)*4.0,sin(t/20.0)*4.0,cos(t/16.0)*4.0]

    # pass data to fragment shader

    glLightfv(GL_LIGHT0,GL_POSITION,[ld[0],ld[1],ld[2]]);
    
    # fallback

    glColor3f(1,1,1)

    glLoadIdentity()
    # render a pretty range of cubes

    for i in range(-5,5):
        for j in range(-5,5):
            for k in range(-5,5):
                glPushMatrix()
                
                glTranslate(i,j,k)
                glScale(0.1,0.1,0.1)
                glCallList(1)
                glPopMatrix()

    pygame.display.flip()
