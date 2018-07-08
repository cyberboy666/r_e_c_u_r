#! /usr/bin/env python
# -*- coding: utf-8 -*-
import common2d, sys
import OpenGL.GLUT as glut
import OpenGL.GL as gl

_myProg = None

def displayFunc():
	global _myProg
	common2d.display(_myProg)
	glut.glutSwapBuffers()

def set_global_program(program):
	global _myProg
	_myProg = program

def reshape(width,height):
	gl.glViewport(0, 0, width, height)

def keyboard( key, x, y ):
	if key == '\033':
		sys.exit( )

if __name__=="__main__":
	# GLUT init
	# --------------------------------------
	glut.glutInit()
	glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
	glut.glutCreateWindow('Hello world!')
	glut.glutReshapeWindow(640,480)
	glut.glutReshapeFunc(reshape)
	glut.glutDisplayFunc(displayFunc)
	glut.glutKeyboardFunc(keyboard)

	program = common2d.init_shader_program()
	set_global_program(program)

	# Make program the default program
	gl.glUseProgram(program)

	# Enter mainloop
	# --------------------------------------
	glut.glutMainLoop()

if __name__ == '__main__': 
	main()
