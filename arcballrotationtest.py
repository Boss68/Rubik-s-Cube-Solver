import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

window=pygame.display.set_mode((800,800),pygame.OPENGL)


def drawCube():
    glBegin(GL_QUADS)
