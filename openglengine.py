import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

vertices=((1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,-1),(1,-1,1),(1,1,1),(-1,-1,1),(-1,1,1))
edges=((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))
faces=((0,1,2,3),(3,2,7,6),(6,7,5,4),(4,5,1,0),(1,5,7,2),(4,0,3,6))
colors=((1,0,0),(0,0,1),(1,1,0),(0,1,0),(1,1,1),(1,0,1))
ground_vertices=((-10,-1.1,20),(10,-1.1,20),(-10,-1.1,-300),(10,-1.1,-300))
def ground():
    glBegin(GL_QUADS)
    for vertex in ground_vertices:
        glColor3fv((0.5,0.5,0.5))
        glVertex3fv(vertex)
    glEnd()
def set_vertices(max_distance):
    x_value_change=random.randrange(-10,10)
    #y_value_change=random.randrange(-10,10)
    z_value_change=random.randrange(-1*max_distance,-20)
    new_vertices=[]
    for vert in vertices:
        new_vert=[]
        new_x=vert[0]+x_value_change
        #new_y = vert[1] + y_value_change
        new_y=vert[1]
        new_z = vert[2] + z_value_change

        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)
        new_vertices.append(new_vert)
    return new_vertices

def Cube(cube_verts):
    glBegin(GL_QUADS)
    for face in faces:
        x=random.randint(0,5)
        for vertex in face:
            glColor3fv(colors[x])
            glVertex3fv(cube_verts[vertex])
    glEnd()




    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
            #glColor3fv((0, 0, 0))
    glEnd()
def main():
    speed=0.05
    pygame.init()
    display=(1280,720)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45,display[0]/display[1], 0.1,50)
    glTranslatef(random.randrange(-5,5),0,-40)
    glRotatef(0,0,0,0)
    #object_passed=False
    max_distance=100
    cube_dict={}
    for x in range(20):
        cube_dict[x]=set_vertices(max_distance)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        if pygame.key.get_pressed()[pygame.K_a]:
            glTranslatef(speed, 0, 0)
        elif pygame.key.get_pressed()[pygame.K_d]:
            glTranslatef(-speed, 0, 0)
        if pygame.key.get_pressed()[pygame.K_w]:
            glTranslatef(0, -speed, 0)
        elif pygame.key.get_pressed()[pygame.K_s]:
            glTranslatef(0, speed, 0)

        #glRotatef(0.1,0,1,0)

        x=glGetDoublev(GL_MODELVIEW_MATRIX)
        camera_x = x[3][0]
        camera_y = x[3][1]
        camera_z = x[3][2]
        #print(camera_x,camera_y,camera_z)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glTranslatef(0, 0, 0.5)
        ground()
        for each_cube in cube_dict:
            Cube(cube_dict[each_cube])
        pygame.display.flip()
        pygame.time.wait(10)
main()