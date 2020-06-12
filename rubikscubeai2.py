import pygame, threading,math, random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
#my coded NEAT
dimensions=(640,480)
window=pygame.display.set_mode(dimensions,DOUBLEBUF|OPENGL)
running=True
size =3
buttonfontsize=1
buttontext=pygame.font.SysFont('arial',buttonfontsize)
turnangle=0
rubiksmovequeue=[]
indextoaxisandvalue={0:(2,-1),1:(0,-1),2:(2,1),3:(0,1),4:(1,1),5:(1,-1),6:(3,3)}
finishturn=True
scramble=True
pygame.display.set_caption(str(size)+'X'+str(size)+'X'+str(size))
threenotation={'F':(2,2),'B':(2,0),'L':(0,0),'R':(0,2),'U':(1,2),'D':(1,0)}
possiblemoves=['F','B','L','R','U','D']
possibleextensions=['','\'','2']
rotation=''
'''rotation=input('Rubik\'s rotation? ')
while not((len(rotation)==1 and rotation in threenotation) or (len(rotation)==2 and rotation[0] in threenotation and (rotation[1]=='2' or rotation[1]=='\''))):
   rotation=input('Invalid. Rubik\'s rotation? ')
rubiksmovequeue.append(rotation)'''
allcolors={}
queueremove=False
animspeed=10
constants={0:(2,1),1:(0,2),2:(0,1)}
xy=[0,0]
class NeuralNet(object):
    def __init__(self,inputsize,outputsize):
        self.genome=[[(i+1,(i>inputsize)+(i>outputsize)) for i in range(inputsize+outputsize)],[]]
        self.nodes=[0 for i in range(len(self.genome[0]))]
    def runNeuralNet(self,input):
        for i in self.genome[1]:
            None
class Generation(object):
    def __init__(self,scrambled,outputsize=18):
        self.gensize=1000
        self.generation=1
        self.outputsize=outputsize
        self.scrambled=scrambled
        self.virtcube={}
        self.startinput={}
        self.writingcubedict={}
        for a in range(size):
            for b in range(size):
                for c in range(size):
                    self.virtcube[(a, b, c)] = [6, 6, 6, 6, 6, 6]
                    if a == 0:
                        self.virtcube[(a, b, c)][1] = 3
                    elif a == size - 1:
                        self.virtcube[(a, b, c)][3] = 2
                    if b == 0:
                        self.virtcube[(a, b, c)][5] = 0
                    elif b == size - 1:
                        self.virtcube[(a, b, c)][4] = 1
                    if c == 0:
                        self.virtcube[(a, b, c)][0] = 5
                    if c == size - 1:
                        self.virtcube[(a, b, c)][2] = 4
        for a in range(size):
            for b in range(size):
                for c in range(size):
                    self.startinput[(a, b, c)] = [6, 6, 6, 6, 6, 6]
                    if a == 0:
                        self.startinput[(a, b, c)][1] = 3
                    elif a == size - 1:
                        self.startinput[(a, b, c)][3] = 2
                    if b == 0:
                        self.startinput[(a, b, c)][5] = 0
                    elif b == size - 1:
                        self.startinput[(a, b, c)][4] = 1
                    if c == 0:
                        self.startinput[(a, b, c)][0] = 5
                    if c == size - 1:
                        self.startinput[(a, b, c)][2] = 4
        for a in range(size):
            for b in range(size):
                for c in range(size):
                    self.writingcubedict[(a, b, c)] = [6, 6, 6, 6, 6, 6]
                    if a == 0:
                        self.writingcubedict[(a, b, c)][1] = 3
                    elif a == size - 1:
                        self.writingcubedict[(a, b, c)][3] = 2
                    if b == 0:
                        self.writingcubedict[(a, b, c)][5] = 0
                    elif b == size - 1:
                        self.writingcubedict[(a, b, c)][4] = 1
                    if c == 0:
                        self.writingcubedict[(a, b, c)][0] = 5
                    if c == size - 1:
                        self.writingcubedict[(a, b, c)][2] = 4
        for rotate in self.scrambled:
            for a in range(size):
                for b in range(size):
                    for c in range(size):
                        self.newcolorlist = None
                        if (a, b, c)[threenotation[rotate[0]][0]] == threenotation[rotate[0]][1]:
                            self.xy = [(a, b, c)[i] - 1 for i in constants[threenotation[rotate[0]][0]]]
                            self.xyindexes = [constants[threenotation[rotate[0]][0]][0],
                                              constants[threenotation[rotate[0]][0]][1]]
                            self.newxyz = [0, 0, 0]
                            self.newxyz[self.xyindexes[0]] = math.atan2(self.xy[1], self.xy[0])
                            self.newxyz[self.xyindexes[1]] = math.atan2(self.xy[1], self.xy[0])
                            if len(rotate) > 1:
                                self.newxyz[self.xyindexes[0]] += math.pi / 2 * 1 * ((rotate[1] != '\'') * 2 - 1) * (
                                            (rotate[1] == '2') + 1) * ((rotate[0] != 'F' and rotate[0] != 'D' and
                                                                        rotate[0] != 'L') * 2 - 1)
                                self.newxyz[self.xyindexes[1]] += math.pi / 2 * 1 * ((rotate[1] != '\'') * 2 - 1) * (
                                            (rotate[1] == '2') + 1) * ((rotate[0] != 'F' and rotate[0] != 'D' and
                                                                        rotate[0] != 'L') * 2 - 1)
                            else:
                                self.newxyz[self.xyindexes[0]] += math.pi / 2 * (
                                            (rotate[0] != 'F' and rotate[0] != 'D' and rotate[0] != 'L') * 2 - 1)
                                self.newxyz[self.xyindexes[1]] += math.pi / 2 * (
                                            (rotate[0] != 'F' and rotate[0] != 'D' and rotate[0] != 'L') * 2 - 1)
                            self.newxyz[self.xyindexes[0]] = math.cos(self.newxyz[self.xyindexes[0]]) * math.hypot(
                                self.xy[0], self.xy[1]) + 1
                            self.newxyz[self.xyindexes[1]] = math.sin(self.newxyz[self.xyindexes[1]]) * math.hypot(
                                self.xy[0], self.xy[1]) + 1
                            # print(self.newxyz)
                            for i in range(3):
                                if not (i in constants[threenotation[rotate[0]][0]]):
                                    self.newxyz[i] = (a, b, c)[i]
                                    # print(i)
                                    break
                            self.newxyz = tuple([int(round(i)) for i in self.newxyz])
                            # print((a,b,c),self.newxyz)
                            self.colorlist = self.startinput[(a, b, c)]
                            self.newcolorlist = [i for i in self.colorlist]
                            self.possibleones = []
                            for i in range(len(self.colorlist)):
                                self.zero = [0, 1, 2]
                                self.zero.remove(threenotation[rotate[0]][0])
                                if indextoaxisandvalue[i][0] != threenotation[rotate[0]][0]:
                                    # print(self.colorlist,self.newxyz,(a,b,c),indextoaxisandvalue[i])
                                    self.zero.remove(indextoaxisandvalue[i][0])
                                    self.zero = self.zero[0]
                                    self.xytwo = list(constants[threenotation[rotate[0]][0]])
                                    self.xytwotwo = [0, 0]
                                    self.xytwotwo[self.xytwo.index(indextoaxisandvalue[i][0])] = indextoaxisandvalue[i][
                                        1]
                                    self.xytwotwo[self.xytwo.index(self.zero)] = 0
                                    self.xytwo = self.xytwotwo[::]
                                    self.xytwotwo = None
                                    # print(self.xytwo,self.zero,indextoaxisandvalue[i])
                                    self.newxytwo = [0, 0]
                                    self.changeval = -1 * (
                                                (rotate[0] != 'F' and rotate[0] != 'D' and rotate[0] != 'L') * 2 - 1)
                                    if len(rotate) > 1:
                                        self.changeval = -1 * ((rotate[1] != '\'') * 2 - 1) * (
                                                    (rotate[1] == '2') + 1) * ((rotate[0] != 'F' and rotate[
                                            0] != 'D' and rotate[0] != 'L') * 2 - 1)
                                    self.newxytwo = [math.cos(math.atan2(self.xytwo[1], self.xytwo[
                                        0]) + math.pi / 2 * self.changeval) * math.hypot(self.xytwo[0], self.xytwo[1]),
                                                     math.sin(math.atan2(self.xytwo[1], self.xytwo[
                                                         0]) + math.pi / 2 * self.changeval) * math.hypot(self.xytwo[0],
                                                                                                          self.xytwo[
                                                                                                              1])]
                                    self.newxytwo = [int(round(q)) for q in self.newxytwo]
                                    # print(self.newxytwo)
                                    for x in range(len(self.newxytwo)):
                                        if self.newxytwo[x] != 0:
                                            self.newxytwo[(x + 1) % 2] = constants[threenotation[rotate[0]][0]][x]
                                            if x == 0:
                                                self.newxytwo = self.newxytwo[::-1]
                                            break
                                    # print(list(indextoaxisandvalue.items()))
                                    self.newcolorindex = [i[1] for i in list(indextoaxisandvalue.items())].index(
                                        tuple(self.newxytwo))
                                    self.newcolorlist[i] = self.colorlist[self.newcolorindex]
                            # print(self.colorlist,self.newcolorlist)
                            self.writingcubedict[self.newxyz] = self.newcolorlist
                            # print(self.startinput.items()==self.writingcubedict.items())

            self.startinput = {}
            for i in self.writingcubedict:
                self.startinput[i] = self.writingcubedict[i]
        self.nnreadinput=[]
        for i in list(self.startinput):
            for x in self.startinput[i]:
                self.nnreadinput.append(x/3-1)
        print([round(i,2) for i in self.nnreadinput])
        self.inputsize=len(self.nnreadinput)
    def rungeneration(self):
        None
def getturn():
    global rubiksmovequeue, threenotation,finishturn, queueremove, scramble
    while True:
        if finishturn==True and scramble==False:
            newrotation = input('Rubik\'s rotation? ')
            while not ((len(newrotation) == 1 and newrotation in threenotation) or (
                    len(newrotation) == 2 and newrotation[0] in threenotation and (newrotation[1] == '2' or newrotation[1] == '\''))):
                newrotation = input('Invalid. Rubik\'s rotation? ')
            while queueremove==True:
                None
            rubiksmovequeue.append(newrotation)
        else:
            None
for i in range(50):
    rubiksmovequeue.append(possiblemoves[random.randint(0,5)]+possibleextensions[random.randint(0,2)])
    if len(rubiksmovequeue)>1:
        while rubiksmovequeue[len(rubiksmovequeue)-1][0]==rubiksmovequeue[len(rubiksmovequeue)-2][0]:
            rubiksmovequeue[len(rubiksmovequeue)-1]=possiblemoves[random.randint(0,5)]+possibleextensions[random.randint(0,2)]
print('Scramble: '+str(rubiksmovequeue))
scrambled=rubiksmovequeue[::]
Generation(scrambled)
if scramble==False:
    queuethread=threading.Thread(target=getturn)
    queuethread.setDaemon(True)
    queuethread.start()
for a in range(size):
    for b in range(size):
        for c in range(size):
            allcolors[(a,b,c)]=[6,6,6,6,6,6]
            if a==0:
                allcolors[(a, b, c)][1] = 3
            elif a==size-1:
                allcolors[(a, b, c)][3] = 2
            if b==0:
                allcolors[(a, b, c)][5] = 0
            elif b==size-1:
                allcolors[(a, b, c)][4] = 1
            if c==0:
                allcolors[(a, b, c)][0] = 5
            if c==size-1:
                allcolors[(a, b, c)][2] = 4
newallcolors={}
for a in range(size):
    for b in range(size):
        for c in range(size):
            newallcolors[(a,b,c)]=[6,6,6,6,6,6]
            if a==0:
                newallcolors[(a, b, c)][1] = 3
            elif a==size-1:
                newallcolors[(a, b, c)][3] = 2
            if b==0:
                newallcolors[(a, b, c)][5] = 0
            elif b==size-1:
                newallcolors[(a, b, c)][4] = 1
            if c==0:
                newallcolors[(a, b, c)][0] = 5
            if c==size-1:
                newallcolors[(a, b, c)][2] = 4
#print(newallcolors)
pygame.time.wait(1000)
def background():
    glBegin(GL_QUADS)
    verts = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))
    verts=[[x*900 for x in i] for i in verts]
    faces = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))
    glColor3fv((0.5,0.5,0.5))
    for face in faces:
        for vert in face:
            glVertex3fv(verts[vert])
    glEnd()
'''def similar(iter,value,index):
    allsame=True
    for i in iter:
        if i[index]!=value:
            allsame=False
            break
    return allsame'''
def RubiksCube():
    global size, turnangle, allcolors, finishturn
    glEnable(GL_DEPTH_TEST)
    change=-(size-1)
    changey=-(size-1)
    changez=-(size-1)
    verts = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, 1), (1, 1, 1), (-1,-1, 1), (-1, 1, 1))
    edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))
    faces = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))
    facecolors=[(1,1,1),(1,1,0),(0,0,1),(0,1,0),(1,0.5,0),(1,0,0),(0,0,0)]
    '''0=behind (white)
    1=left (yellow)
    2=front (blue)
    3=right (green)
    4=top (orange)
    5=bottom (red)
    6=none (black)'''
    #print(goalsituation)
    #allcolors={(0,0,0):[3,5,6,6,6,1],(1,0,0):[3,6,6,6,6,1],(2,0,0):[3,6,6,4,6,1],()}
    if finishturn==True and len(rubiksmovequeue)!=0:
        for a in range(size):
            for b in range(size):
                for c in range(size):
                    newcolorlist=None
                    if (a,b,c)[threenotation[rotation[0]][0]]==threenotation[rotation[0]][1]:
                        xy=[(a,b,c)[i]-1 for i in constants[threenotation[rotation[0]][0]]]
                        xyindexes=[constants[threenotation[rotation[0]][0]][0],constants[threenotation[rotation[0]][0]][1]]
                        newxyz=[0,0,0]
                        newxyz[xyindexes[0]]=math.atan2(xy[1],xy[0])
                        newxyz[xyindexes[1]] = math.atan2(xy[1], xy[0])
                        if len(rotation)>1:
                            newxyz[xyindexes[0]]+=math.pi/2*1*((rotation[1] != '\'')*2-1)*((rotation[1] == '2') + 1)*((rotation[0]!='F' and rotation[0]!='D' and rotation[0]!='L')*2-1)
                            newxyz[xyindexes[1]]+=math.pi/2*1*((rotation[1] != '\'')*2-1)*((rotation[1] == '2') + 1)*((rotation[0]!='F' and rotation[0]!='D' and rotation[0]!='L')*2-1)
                        else:
                            newxyz[xyindexes[0]] += math.pi / 2*((rotation[0]!='F' and rotation[0]!='D' and rotation[0]!='L')*2-1)
                            newxyz[xyindexes[1]] += math.pi / 2*((rotation[0]!='F' and rotation[0]!='D' and rotation[0]!='L')*2-1)
                        newxyz[xyindexes[0]]=math.cos(newxyz[xyindexes[0]])*math.hypot(xy[0],xy[1])+1
                        newxyz[xyindexes[1]]=math.sin(newxyz[xyindexes[1]])*math.hypot(xy[0],xy[1])+1
                        #print(newxyz)
                        for i in range(3):
                            if not(i in constants[threenotation[rotation[0]][0]]):
                                newxyz[i]=(a,b,c)[i]
                                #print(i)
                                break
                        newxyz=tuple([int(round(i))for i in newxyz])
                        #print((a,b,c),newxyz)
                        colorlist=allcolors[(a,b,c)]
                        newcolorlist=[i for i in colorlist]
                        possibleones=[]
                        for i in range(len(colorlist)):
                            zero=[0,1,2]
                            zero.remove(threenotation[rotation[0]][0])
                            if indextoaxisandvalue[i][0]!=threenotation[rotation[0]][0]:
                                #print(colorlist,newxyz,(a,b,c),indextoaxisandvalue[i])
                                zero.remove(indextoaxisandvalue[i][0])
                                zero=zero[0]
                                xytwo=list(constants[threenotation[rotation[0]][0]])
                                xytwotwo=[0,0]
                                xytwotwo[xytwo.index(indextoaxisandvalue[i][0])]=indextoaxisandvalue[i][1]
                                xytwotwo[xytwo.index(zero)]=0
                                xytwo=xytwotwo[::]
                                xytwotwo=None
                                #print(xytwo,zero,indextoaxisandvalue[i])
                                newxytwo=[0,0]
                                changeval=-1*((rotation[0]!='F' and rotation[0]!='D' and rotation[0]!='L')*2-1)
                                if len(rotation)>1:
                                    changeval=-1*((rotation[1] != '\'')*2-1)*((rotation[1] == '2')+ 1)*((rotation[0]!='F' and rotation[0]!='D' and rotation[0]!='L')*2-1)
                                newxytwo=[math.cos(math.atan2(xytwo[1],xytwo[0])+math.pi/2*changeval)*math.hypot(xytwo[0],xytwo[1]),math.sin(math.atan2(xytwo[1],xytwo[0])+math.pi/2*changeval)*math.hypot(xytwo[0],xytwo[1])]
                                newxytwo=[int(round(q)) for q in newxytwo]
                                #print(newxytwo)
                                for x in range(len(newxytwo)):
                                    if newxytwo[x]!=0:
                                        newxytwo[(x+1)%2]=constants[threenotation[rotation[0]][0]][x]
                                        if x==0:
                                            newxytwo=newxytwo[::-1]
                                        break
                                #print(list(indextoaxisandvalue.items()))
                                newcolorindex=[i[1] for i in list(indextoaxisandvalue.items())].index(tuple(newxytwo))
                                newcolorlist[i]=colorlist[newcolorindex]
                        #print(colorlist,newcolorlist)
                        newallcolors[newxyz]=newcolorlist
                        #print(allcolors.items()==newallcolors.items())

        allcolors={}
        for i in newallcolors:
            allcolors[i]=newallcolors[i]
    glLineWidth(1)
    for y in range(size):
        for z in range(size):
            newverts = [(f[0] + change, f[1] + changey, f[2]+changez) for f in verts]
            for q in range(size):
                if len(rotation)>0:
                    if rotation[0] in threenotation:
                        if (q,z,y)[threenotation[rotation[0]][0]]==threenotation[rotation[0]][1]:
                            glPushMatrix()
                            if len(rotation)>1:
                                args = [turnangle * ((rotation[1] == '2') + 1), 0, 0, 0]
                                if rotation[0]=='R' or rotation[0]=='U' or rotation[0]=='F':
                                    args[threenotation[rotation[0]][0] + 1] = -1 * ((rotation[1] != '\'') * 2 - 1)
                                else:
                                    args[threenotation[rotation[0]][0] + 1] = 1 * ((rotation[1] != '\'') * 2 - 1)
                                glRotatef(*args)
                            else:
                                args = [turnangle, 0, 0, 0]
                                if rotation[0]=='R' or rotation[0]=='U' or rotation[0]=='F':
                                    args[threenotation[rotation[0]][0]+1]=-1
                                else:
                                    args[threenotation[rotation[0]][0] + 1] = 1
                                glRotatef(*args)
                            #print((q,z,y))
                glBegin(GL_QUADS)
                for face in faces:
                    '''for i in facecolors:
                        if similar([newverts[x] for x in face],i[0]+change*(i[1]==0)+changey*(i[1]==1)+changez*(i[1]==2),i[1]):
                            finalcolor=facecolors[i]
                            #print(finalcolor)
                            break'''
                    if (q,z,y) in allcolors:
                        finalcolor=facecolors[allcolors[(q,z,y)][faces.index(face)]]
                        #print(finalcolor)
                    else:
                        finalcolor=(0,0,0)
                    glColor3fv(finalcolor)
                    for vert in face:
                        glVertex3fv(newverts[vert])
                glEnd()
                glLineWidth(3)
                glBegin(GL_LINES)
                for edge in edges:
                    for vert in edge:
                        glColor3fv((0,0,0))
                        glVertex3fv(newverts[vert])
                glEnd()
                change+=2
                newverts = [(f[0] + change, f[1]+changey, f[2]+changez) for f in verts]
                if len(rotation)>0:
                    if rotation[0] in threenotation:
                        if (q,z,y)[threenotation[rotation[0]][0]]==threenotation[rotation[0]][1]:
                            glPopMatrix()
            change=-(size-1)
            changey+=2
        changey=-(size-1)
        changez+=2
    glDisable(GL_DEPTH_TEST)
gluPerspective(45, dimensions[0] / dimensions[1], 0.1, 2000*3/size)
glTranslatef(0,-2,-30)
#glScalef(1/scale,1/scale,1/scale)
glRotatef(0,0,0,0)
glScalef(3/size,3/size,3/size)
up=True
rotatekey=[0,0,0]
finishturn=False
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            #print(event.button)
            if event.button==4:
                glTranslatef(0,0,-5)
            if event.button==5:
                glTranslatef(0,0,5)
        if event.type==pygame.KEYDOWN:
            if event.key==K_ESCAPE:
                pygame.quit()
                running=False
    if running==True:
        #print(pygame.mouse.get_pos())
        queueremove=True
        '''if finishturn==False:
            print(rotation,finishturn)'''
        if len(rubiksmovequeue)!=0:
            rotation=rubiksmovequeue[0]
            finishturn=False
            turnangle+=animspeed
            if turnangle>=90:
                turnangle = 0
                finishturn=True
        '''if up==True:
            if turnangle<90:
                turnangle+=5
            else:
                up=False
        elif up==False:
            if turnangle>0:
                turnangle-=5
            else:
                up=True'''
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        background()
        glPushMatrix()
        if pygame.key.get_pressed()[pygame.K_w]:
            rotatekey[0]-=3
        elif pygame.key.get_pressed()[pygame.K_s]:
            rotatekey[0]+=3
        if pygame.key.get_pressed()[pygame.K_a]:
            rotatekey[1]-=3
        elif pygame.key.get_pressed()[pygame.K_d]:
            rotatekey[1]+=3
        glRotate(abs(rotatekey[0]),((abs(rotatekey[0])-rotatekey[0])!=2*abs(rotatekey[0]))*2-1,0,0)
        glRotate(abs(rotatekey[1]),0,((abs(rotatekey[1])-rotatekey[1])!=2*abs(rotatekey[1]))*2-1,0)
        RubiksCube()
        if finishturn==True and len(rubiksmovequeue)>0:
            del rubiksmovequeue[0]
        if len(rubiksmovequeue)==0 and scramble==True:
            scramble=False
            queuethread = threading.Thread(target=getturn)
            queuethread.setDaemon(True)
            queuethread.start()
            #print(allcolors)
        queueremove=False
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)
