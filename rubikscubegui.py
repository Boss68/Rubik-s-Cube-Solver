import pygame, threading,math, random,time,sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from copy import deepcopy
from PyQt5 import QtCore, QtGui, QtOpenGL,QtWidgets

#pygame.init()
dimensions=(640,480)
#window=pygame.display.set_mode(dimensions,DOUBLEBUF|OPENGL)
running=True
size =3
fullscreen=False
solvetime=0
buttonfontsize=1
#buttontext=pygame.font.SysFont('arial',buttonfontsize)
turnangle=0
rubiksmovequeue=[]
indextoaxisandvalue={0:(2,-1),1:(0,-1),2:(2,1),3:(0,1),4:(1,1),5:(1,-1),6:(3,3)}
finishturn=True
scramble=False
#pygame.display.set_caption(str(size)+'X'+str(size)+'X'+str(size))
threenotation={'F':(2,2),'B':(2,0),'L':(0,0),'R':(0,2),'U':(1,2),'D':(1,0)}
axisandvaluetonotation={(2,2):'F',(2,0):'B',(0,0):'L',(0,2):'R',(1,2):'U',(1,0):'D'}
possiblemoves=['F','B','L','R','U','D']
possibleextensions=['','\'','2']
rotation=''
numtocolor={0:5,1:3,2:4,3:2,4:1,5:0}
'''rotation=input('Rubik\'s rotation? ')
while not((len(rotation)==1 and rotation in threenotation) or (len(rotation)==2 and rotation[0] in threenotation and (rotation[1]=='2' or rotation[1]=='\''))):
   rotation=input('Invalid. Rubik\'s rotation? ')
rubiksmovequeue.append(rotation)'''
allcolors={}
queueremove=False
animspeed=5
solve=False
constants={0:(2,1),1:(0,2),2:(0,1)}
xy=[0,0]
newrotation=''
def maketurn(currentstate,turn):
    global size, allcolors,threenotation,constants
    newcurrentstate=deepcopy(currentstate)
    for a in range(size):
        for b in range(size):
            for c in range(size):
                newcolorlist = None
                if (a, b, c)[threenotation[turn[0]][0]] == threenotation[turn[0]][1]:
                    xy = [(a, b, c)[i] - 1 for i in constants[threenotation[turn[0]][0]]]
                    xyindexes = [constants[threenotation[turn[0]][0]][0], constants[threenotation[turn[0]][0]][1]]
                    newxyz = [0, 0, 0]
                    newxyz[xyindexes[0]] = math.atan2(xy[1], xy[0])
                    newxyz[xyindexes[1]] = math.atan2(xy[1], xy[0])
                    if len(turn) > 1:
                        newxyz[xyindexes[0]] += math.pi / 2 * 1 * ((turn[1] != '\'') * 2 - 1) * (
                                    (turn[1] == '2') + 1) * ((turn[0] != 'F' and turn[0] != 'D' and turn[
                            0] != 'L') * 2 - 1)
                        newxyz[xyindexes[1]] += math.pi / 2 * 1 * ((turn[1] != '\'') * 2 - 1) * (
                                    (turn[1] == '2') + 1) * ((turn[0] != 'F' and turn[0] != 'D' and turn[
                            0] != 'L') * 2 - 1)
                    else:
                        newxyz[xyindexes[0]] += math.pi / 2 * (
                                    (turn[0] != 'F' and turn[0] != 'D' and turn[0] != 'L') * 2 - 1)
                        newxyz[xyindexes[1]] += math.pi / 2 * (
                                    (turn[0] != 'F' and turn[0] != 'D' and turn[0] != 'L') * 2 - 1)
                    newxyz[xyindexes[0]] = math.cos(newxyz[xyindexes[0]]) * math.hypot(xy[0], xy[1]) + 1
                    newxyz[xyindexes[1]] = math.sin(newxyz[xyindexes[1]]) * math.hypot(xy[0], xy[1]) + 1
                    # print(newxyz)
                    for i in range(3):
                        if not (i in constants[threenotation[turn[0]][0]]):
                            newxyz[i] = (a, b, c)[i]
                            # print(i)
                            break
                    newxyz = tuple([int(round(i)) for i in newxyz])
                    # print((a,b,c),newxyz)
                    colorlist = currentstate[(a, b, c)]
                    newcolorlist = [i for i in colorlist]
                    possibleones = []
                    for i in range(len(colorlist)):
                        zero = [0, 1, 2]
                        zero.remove(threenotation[turn[0]][0])
                        if indextoaxisandvalue[i][0] != threenotation[turn[0]][0]:
                            # print(colorlist,newxyz,(a,b,c),indextoaxisandvalue[i])
                            zero.remove(indextoaxisandvalue[i][0])
                            zero = zero[0]
                            xytwo = list(constants[threenotation[turn[0]][0]])
                            xytwotwo = [0, 0]
                            xytwotwo[xytwo.index(indextoaxisandvalue[i][0])] = indextoaxisandvalue[i][1]
                            xytwotwo[xytwo.index(zero)] = 0
                            xytwo = xytwotwo[::]
                            xytwotwo = None
                            # print(xytwo,zero,indextoaxisandvalue[i])
                            newxytwo = [0, 0]
                            changeval = -1 * ((turn[0] != 'F' and turn[0] != 'D' and turn[0] != 'L') * 2 - 1)
                            if len(turn) > 1:
                                changeval = -1 * ((turn[1] != '\'') * 2 - 1) * ((turn[1] == '2') + 1) * (
                                            (turn[0] != 'F' and turn[0] != 'D' and turn[0] != 'L') * 2 - 1)
                            newxytwo = [math.cos(math.atan2(xytwo[1], xytwo[0]) + math.pi / 2 * changeval) * math.hypot(
                                xytwo[0], xytwo[1]),
                                        math.sin(math.atan2(xytwo[1], xytwo[0]) + math.pi / 2 * changeval) * math.hypot(
                                            xytwo[0], xytwo[1])]
                            newxytwo = [int(round(q)) for q in newxytwo]
                            # print(newxytwo)
                            for x in range(len(newxytwo)):
                                if newxytwo[x] != 0:
                                    newxytwo[(x + 1) % 2] = constants[threenotation[turn[0]][0]][x]
                                    if x == 0:
                                        newxytwo = newxytwo[::-1]
                                    break
                            # print(list(indextoaxisandvalue.items()))
                            newcolorindex = [i[1] for i in list(indextoaxisandvalue.items())].index(tuple(newxytwo))
                            newcolorlist[i] = colorlist[newcolorindex]
                    # print(colorlist,newcolorlist)
                    newcurrentstate[newxyz] = newcolorlist
                    # print(currentstate.items()==newcurrentstate.items())

    currentstate = {}
    for i in newcurrentstate:
        currentstate[i] = newcurrentstate[i]
    return currentstate
def step1(state):
    #make yellow cross
    currentcube=deepcopy(state)
    virtcube=deepcopy(state)
    order=[(2,4),(3,2),(0,5),(1,3)]
    solve=[]
    currentpiece=[]
    goalpiececoords=[0,0,0]
    realGoal=[0,0,0]
    realValue=[0,0,0,0,0,0]
    actualSolve=[]
    for i in order:
        virtcube = deepcopy(currentcube)
        for x in currentcube:
            if sorted(currentcube[x])==sorted([i[1],1,6,6,6,6]):
                currentpiece=x
                #print(currentcube[x], i[1], x)
                break
        realGoal[1]=2
        realGoal[indextoaxisandvalue[i[0]][0]]=indextoaxisandvalue[i[0]][1]+1
        realGoal[(indextoaxisandvalue[i[0]][0] + 2) % 4]=1
        realValue[4]=1
        realValue[i[0]]=i[1]
        for x in range(6):
            if x!=4 and x!=i[0]:
                realValue[x]=6
        if currentpiece[indextoaxisandvalue[i[0]][0]]!=indextoaxisandvalue[i[0]][1] + 1:
            goalpiececoords[indextoaxisandvalue[i[0]][0]] = indextoaxisandvalue[i[0]][1] + 1
            if (currentpiece[1]==0 or currentpiece[1]==2):
                goalpiececoords[(indextoaxisandvalue[i[0]][0] + 2) % 4] = 1
                if currentpiece[1]==0:
                    #print('down')
                    goalpiececoords[1]=0
                    solve.append(['D',0])
                    while sorted(virtcube[tuple(goalpiececoords)])!=sorted([i[1],1,6,6,6,6]):
                        virtcube=maketurn(virtcube,'D')
                        solve[len(solve)-1][1]+=1
                elif currentpiece[1]==2:
                    #print('up')
                    goalpiececoords[1]=2
                    #goalpiececoords[(indextoaxisandvalue[i[0]][0] + 2) % 4]=currentpiece[(indextoaxisandvalue[i[0]][0] + 2) % 4]
                    for q in range(order.index(i)):
                        solve.append([axisandvaluetonotation[(indextoaxisandvalue[order[q][0]][0],indextoaxisandvalue[order[q][0]][1]+1)],2])
                        virtcube = maketurn(virtcube, axisandvaluetonotation[(indextoaxisandvalue[order[q][0]][0],indextoaxisandvalue[order[q][0]][1]+1)]+'2')
                    solve.append(['U', 0])
                    while sorted(virtcube[tuple(goalpiececoords)])!=sorted([i[1],1,6,6,6,6]):
                        virtcube=maketurn(virtcube,'U')
                        solve[len(solve)-1][1]+=1
                    for q in range(order.index(i)):
                        solve.append([axisandvaluetonotation[(indextoaxisandvalue[order[q][0]][0],indextoaxisandvalue[order[q][0]][1]+1)],2])
                        virtcube = maketurn(virtcube, axisandvaluetonotation[
                            (indextoaxisandvalue[order[q][0]][0], indextoaxisandvalue[order[q][0]][1] + 1)] + '2')
            elif (currentpiece[1]==1):
                #print('side')
                goalpiececoords[1] = 1
                solve.append(['U', 0])
                #print(list(virtcube.items()))
                followingcube = list(virtcube.keys())[[sorted(z[1]) for z in list(virtcube.items())].index(sorted(currentcube[(0, 2, 1)][::]))]
                while followingcube[(indextoaxisandvalue[i[0]][0] + 2) % 4]!=currentpiece[(indextoaxisandvalue[i[0]][0] + 2) % 4]:
                    solve[len(solve)-1][1]+=1
                    virtcube = maketurn(virtcube, 'U')
                    #print(followingcube,currentpiece[(indextoaxisandvalue[i[0]][0] + 2) % 4])
                    followingcube = list(virtcube.keys())[[sorted(z[1]) for z in list(virtcube.items())].index(sorted(currentcube[(0, 2, 1)][::]))]
                solve.append([axisandvaluetonotation[((indextoaxisandvalue[i[0]][0] + 2) % 4,currentpiece[(indextoaxisandvalue[i[0]][0] + 2) % 4])],2])
                virtcube = maketurn(virtcube, axisandvaluetonotation[((indextoaxisandvalue[i[0]][0] + 2) % 4,currentpiece[(indextoaxisandvalue[i[0]][0] + 2) % 4])]+'2')
                solve.append([solve[len(solve)-2][0],4-solve[len(solve)-2][1]])
                for q in range(solve[len(solve)-1][1]):
                    virtcube = maketurn(virtcube, 'U')
            currentcube=deepcopy(virtcube)
        if currentcube[tuple(realGoal)] != realValue:
            for x in currentcube:
                if sorted(currentcube[x]) == sorted([i[1], 1, 6, 6, 6, 6]):
                    currentpiece = x
                    #print(currentcube[x], i[1], x)
                    break
            if currentcube[currentpiece][i[0]]==i[1]:
                #print("solid")
                solve.append([axisandvaluetonotation[(indextoaxisandvalue[i[0]][0], indextoaxisandvalue[i[0]][1] + 1)], 0])
                while virtcube[tuple(realGoal)]!=realValue:
                    solve[len(solve) - 1][1] += 1
                    virtcube = maketurn(virtcube, axisandvaluetonotation[(indextoaxisandvalue[i[0]][0], indextoaxisandvalue[i[0]][1] + 1)])
            elif currentcube[currentpiece][i[0]]==1:
                #print("invert")
                goalpiececoords[1]=1
                goalpiececoords[indextoaxisandvalue[i[0]][0]]=indextoaxisandvalue[i[0]][1] + 1
                if indextoaxisandvalue[i[0]]==(2,1):
                    goalpiececoords[0]=0
                elif indextoaxisandvalue[i[0]]==(2,-1):
                    goalpiececoords[0]=2
                elif indextoaxisandvalue[i[0]]==(0,-1):
                    goalpiececoords[2]=0
                elif indextoaxisandvalue[i[0]]==(0,1):
                    goalpiececoords[2]=2
                solve.append([axisandvaluetonotation[(indextoaxisandvalue[i[0]][0], indextoaxisandvalue[i[0]][1] + 1)],0])
                while sorted(virtcube[tuple(goalpiececoords)])!=sorted(currentcube[currentpiece]):
                    solve[len(solve) - 1][1] += 1
                    virtcube = maketurn(virtcube, axisandvaluetonotation[(indextoaxisandvalue[i[0]][0], indextoaxisandvalue[i[0]][1] + 1)])
                solve.append(['U',1])
                virtcube=maketurn(virtcube,'U')
                if indextoaxisandvalue[i[0]]==(2,1):
                    solve.append(['L', 3])
                    virtcube = maketurn(virtcube, 'L\'')
                elif indextoaxisandvalue[i[0]]==(2,-1):
                    solve.append(['R', 3])
                    virtcube = maketurn(virtcube, 'R\'')
                elif indextoaxisandvalue[i[0]]==(0,-1):
                    solve.append(['B', 3])
                    virtcube = maketurn(virtcube, 'B\'')
                elif indextoaxisandvalue[i[0]]==(0,1):
                    solve.append(['F', 3])
                    virtcube = maketurn(virtcube, 'F\'')
                solve.append(['U',3])
                virtcube=maketurn(virtcube,'U\'')
            currentcube = deepcopy(virtcube)
        #print(solve)
    for i in solve:
        if i[1]==1:
            actualSolve.append(i[0])
        elif i[1]==2:
            actualSolve.append(i[0]+'2')
        elif i[1]==3:
            actualSolve.append(i[0]+'\'')
    #print(actualSolve)
    '''0=behind (white)
        1=left (yellow)
        2=front (blue)
        3=right (green)
        4=top (orange)
        5=bottom (red)
        6=none (black)'''
    return actualSolve,currentcube
def step2(state):
    #put in yellow corners
    global numtocolor,indextoaxisandvalue
    '''0=behind (white)
        1=left (yellow)
        2=front (blue)
        3=right (green)
        4=top (orange)
        5=bottom (red)
        6=none (black)'''
    solve=[]
    currentstate=deepcopy(state)
    virtcube=deepcopy(currentstate)
    actualSolve=[]
    order=[(0,2,2),(2,2,2),(2,2,0),(0,2,0)]
    rightside={(1,2):2,(3,2):3,(3,0):0,(1,0):1}
    for i in order:
        currentfaces=(list([x[1] for x in indextoaxisandvalue.items()]).index((0,i[0]-1)),list([x[1] for x in indextoaxisandvalue.items()]).index((2,i[2]-1)))
        currentpiece=[numtocolor[x] for x in currentfaces]
        currentpiece.append(1)
        currentcoords=()
        for x in range(3):
            currentpiece.append(6)
        for x in currentstate:
            if sorted(currentstate[x])==sorted(currentpiece):
                currentcoords=x
                break
        actualpos=(list([x[1] for x in indextoaxisandvalue.items()]).index((0, currentcoords[0] - 1)),list([x[1] for x in indextoaxisandvalue.items()]).index((2, currentcoords[2] - 1)))
        #print(sorted(currentpiece),currentcoords,currentfaces)
        if currentcoords!=i or currentstate[currentcoords][4]!=1:
            if currentcoords[1]==2:
                downturn=axisandvaluetonotation[(indextoaxisandvalue[rightside[actualpos]][0],indextoaxisandvalue[rightside[actualpos]][1]+1)]
                #print('top',downturn)
                solve.append([downturn,3])
                virtcube=maketurn(virtcube,downturn+'\'')
                solve.append(['D',3])
                virtcube = maketurn(virtcube, 'D\'')
                solve.append([downturn,1])
                virtcube = maketurn(virtcube,downturn)
                for x in virtcube:
                    if sorted(virtcube[x]) == sorted(currentpiece):
                        currentcoords = x
                        break
                actualpos = (list([x[1] for x in indextoaxisandvalue.items()]).index((0, currentcoords[0] - 1)),list([x[1] for x in indextoaxisandvalue.items()]).index((2, currentcoords[2] - 1)))
            if currentcoords[1]==0:
                downturn = axisandvaluetonotation[(indextoaxisandvalue[rightside[actualpos]][0], indextoaxisandvalue[rightside[actualpos]][1] + 1)]
                #print(downturn,currentcoords)
                #print('bottom')
                solve.append(['D',0])
                while (currentcoords[0],currentcoords[2])!=(i[0],i[2]):
                    solve[len(solve)-1][1]+=1
                    virtcube = maketurn(virtcube, 'D')
                    for x in virtcube:
                        if sorted(virtcube[x]) == sorted(currentpiece):
                            currentcoords = x
                actualpos = (list([x[1] for x in indextoaxisandvalue.items()]).index((0, currentcoords[0] - 1)),
                             list([x[1] for x in indextoaxisandvalue.items()]).index((2, currentcoords[2] - 1)))
                downturn = axisandvaluetonotation[
                    (indextoaxisandvalue[rightside[actualpos]][0], indextoaxisandvalue[rightside[actualpos]][1] + 1)]
                #print(str(currentcoords)+" under right piece: "+str(i))
                if virtcube[currentcoords][rightside[actualpos]]==1:
                    solve.append([downturn, 3])
                    virtcube = maketurn(virtcube, downturn + '\'')
                    solve.append(['D', 3])
                    virtcube = maketurn(virtcube, 'D\'')
                    solve.append([downturn, 1])
                    virtcube = maketurn(virtcube, downturn)
                elif virtcube[currentcoords][rightside[actualpos]]!=1 and virtcube[currentcoords][5]==1:
                    solve.append([downturn, 3])
                    virtcube = maketurn(virtcube, downturn + '\'')
                    solve.append(['D',2])
                    virtcube = maketurn(virtcube, 'D2')
                    solve.append([downturn, 1])
                    virtcube = maketurn(virtcube, downturn)
                    solve.append(['D',1])
                    virtcube = maketurn(virtcube, 'D')
                    solve.append([downturn, 3])
                    virtcube = maketurn(virtcube, downturn + '\'')
                    solve.append(['D', 3])
                    virtcube = maketurn(virtcube, 'D\'')
                    solve.append([downturn, 1])
                    virtcube = maketurn(virtcube, downturn)
                else:
                    solve.append(['D', 3])
                    virtcube = maketurn(virtcube, 'D\'')
                    solve.append([downturn, 3])
                    virtcube = maketurn(virtcube, downturn + '\'')
                    solve.append(['D', 1])
                    virtcube = maketurn(virtcube, 'D')
                    solve.append([downturn, 1])
                    virtcube = maketurn(virtcube, downturn)
            currentstate=deepcopy(virtcube)
    for i in solve:
        if i[1] == 1:
            actualSolve.append(i[0])
        elif i[1] == 2:
            actualSolve.append(i[0] + '2')
        elif i[1] == 3:
            actualSolve.append(i[0] + '\'')
    #print('----')
    return actualSolve,currentstate
def step3(state):
    '''0=behind (white)
                1=left (yellow)
                2=front (blue)
                3=right (green)
                4=top (orange)
                5=bottom (red)
                6=none (black)

                idk why i made it like this'''
    #solve middle layer
    currentstate=deepcopy(state)
    order=[(2,3),(2,1),(1,0),(0,3)]
    leftright={2:(1,3),3:(2,0),0:(3,1),1:(0,2)}
    edgeleftright=[(1,2),(2,3),(3,0),(0,1)]
    currentpiece=()
    virtcube=deepcopy(currentstate)
    solve=[]
    actualSolve=[]
    currentdirection=0
    otherdirection=0
    for i in order:
        for x in currentstate:
            if sorted(currentstate[x])==sorted([numtocolor[i[0]],numtocolor[i[1]],6,6,6,6]):
                currentpiece=x
        if currentpiece[1]==1 and len([i for i in currentstate[currentpiece] if i!=6 and numtocolor[currentstate[currentpiece].index(i)]==i])<2:
            #print('middle',currentpiece)
            betweenfaces=tuple([currentstate[currentpiece].index(x) for x in currentstate[currentpiece] if x!=6])
            whitepiece=(False,6)
            solve.append(['D',0])
            while whitepiece[0]==False:
                solve[len(solve) - 1][1] += 1
                virtcube = maketurn(virtcube, 'D')
                for q in betweenfaces:
                    whitecoords = [1, 0, 1]
                    whitecoords[indextoaxisandvalue[q][0]]=indextoaxisandvalue[q][1]+1
                    if 0 in virtcube[tuple(whitecoords)]:
                        whitepiece=(True,q)
                        break
            currentdirection = [virtcube[tuple(whitecoords)].index(x) for x in virtcube[tuple(whitecoords)] if
                                virtcube[tuple(whitecoords)].index(x) != 5 and x != 6][0]
            otherdirection = [currentstate[currentpiece].index(x) for x in currentstate[currentpiece] if
                              currentstate[currentpiece].index(x) != currentdirection and x != 6][0]
            currentdirection = axisandvaluetonotation[
                (indextoaxisandvalue[currentdirection][0], indextoaxisandvalue[currentdirection][1] + 1)]
            otherdirection = axisandvaluetonotation[
                (indextoaxisandvalue[otherdirection][0], indextoaxisandvalue[otherdirection][1] + 1)]
            #print(currentdirection,otherdirection)
            if edgeleftright[[sorted(x) for x in edgeleftright].index(sorted(betweenfaces))].index(whitepiece[1])==1:
                #print('right')
                solve.append(['D', 1])
                virtcube = maketurn(virtcube, 'D')
                solve.append([otherdirection, 1])
                virtcube = maketurn(virtcube, otherdirection)
                solve.append(['D', 3])
                virtcube = maketurn(virtcube, 'D\'')
                solve.append([otherdirection, 3])
                virtcube = maketurn(virtcube, otherdirection + "\'")
                solve.append(['D', 3])
                virtcube = maketurn(virtcube, "D\'")
                solve.append([currentdirection, 3])
                virtcube = maketurn(virtcube, currentdirection + "\'")
                solve.append(['D', 1])
                virtcube = maketurn(virtcube, 'D')
                solve.append([currentdirection, 1])
                virtcube = maketurn(virtcube, currentdirection)
            else:
                #print('left')
                solve.append(['D', 3])
                virtcube = maketurn(virtcube, 'D\'')
                solve.append([otherdirection, 3])
                virtcube = maketurn(virtcube, otherdirection + "\'")
                solve.append(['D', 1])
                virtcube = maketurn(virtcube, 'D')
                solve.append([otherdirection, 1])
                virtcube = maketurn(virtcube, otherdirection)
                solve.append(['D', 1])
                virtcube = maketurn(virtcube, "D")
                solve.append([currentdirection, 1])
                virtcube = maketurn(virtcube, currentdirection)
                solve.append(['D', 3])
                virtcube = maketurn(virtcube, 'D\'')
                solve.append([currentdirection, 3])
                virtcube = maketurn(virtcube, currentdirection + '\'')
        currentstate=deepcopy(virtcube)
        for x in currentstate:
            if sorted(currentstate[x])==sorted([numtocolor[i[0]],numtocolor[i[1]],6,6,6,6]):
                currentpiece=x
        if currentpiece[1]==0:
            #print('top',currentpiece)
            othercolor=[x for x in currentstate[currentpiece] if x!=6 and currentstate[currentpiece].index(x)!=5][0]
            #print(othercolor)
            solve.append(['D',0])
            while numtocolor[virtcube[currentpiece].index(othercolor)]!=othercolor:
                solve[len(solve)-1][1]+=1
                virtcube=maketurn(virtcube,'D')
                for x in virtcube:
                    if sorted(virtcube[x]) == sorted([numtocolor[i[0]], numtocolor[i[1]], 6, 6, 6, 6]):
                        currentpiece = x

            if [numtocolor[x] for x in leftright[virtcube[currentpiece].index(othercolor)]].index(virtcube[currentpiece][5])==0:
                #print('right')
                otherdirection=axisandvaluetonotation[(indextoaxisandvalue[leftright[virtcube[currentpiece].index(othercolor)][0]][0],indextoaxisandvalue[leftright[virtcube[currentpiece].index(othercolor)][0]][1]+1)]
                currentdirection = axisandvaluetonotation[(
                indextoaxisandvalue[virtcube[currentpiece].index(othercolor)][0],
                indextoaxisandvalue[virtcube[currentpiece].index(othercolor)][1] + 1)]
                solve.append(['D',1])
                virtcube=maketurn(virtcube,'D')
                solve.append([otherdirection, 1])
                virtcube = maketurn(virtcube, otherdirection)
                solve.append(['D', 3])
                virtcube = maketurn(virtcube, 'D\'')
                solve.append([otherdirection,3])
                virtcube = maketurn(virtcube, otherdirection+"\'")
                solve.append(['D', 3])
                virtcube = maketurn(virtcube, "D\'")
                solve.append([currentdirection, 3])
                virtcube = maketurn(virtcube, currentdirection+"\'")
                solve.append(['D', 1])
                virtcube = maketurn(virtcube, 'D')
                solve.append([currentdirection, 1])
                virtcube = maketurn(virtcube, currentdirection)
            elif [numtocolor[x] for x in leftright[virtcube[currentpiece].index(othercolor)]].index(virtcube[currentpiece][5])==1:
                #right
                #print('left')
                otherdirection = axisandvaluetonotation[(indextoaxisandvalue[leftright[virtcube[currentpiece].index(othercolor)][1]][0],indextoaxisandvalue[leftright[virtcube[currentpiece].index(othercolor)][1]][1] + 1)]
                currentdirection = axisandvaluetonotation[(indextoaxisandvalue[virtcube[currentpiece].index(othercolor)][0],indextoaxisandvalue[virtcube[currentpiece].index(othercolor)][1]+1)]
                solve.append(['D', 3])
                virtcube = maketurn(virtcube, 'D\'')
                solve.append([otherdirection, 3])
                virtcube = maketurn(virtcube, otherdirection+"\'")
                solve.append(['D', 1])
                virtcube = maketurn(virtcube, 'D')
                solve.append([otherdirection, 1])
                virtcube = maketurn(virtcube, otherdirection)
                solve.append(['D', 1])
                virtcube = maketurn(virtcube, "D")
                solve.append([currentdirection, 1])
                virtcube = maketurn(virtcube, currentdirection)
                solve.append(['D', 3])
                virtcube = maketurn(virtcube, 'D\'')
                solve.append([currentdirection, 3])
                virtcube = maketurn(virtcube, currentdirection+'\'')
        '''elif currentpiece[1]==2:
            #print('what',currentpiece)
        elif currentpiece[1]==1 and len([i for i in currentstate[currentpiece] if i!=6 and numtocolor[currentstate[currentpiece].index(i)]==i])==2:
            #print('solved piece', currentpiece)'''
        currentstate=deepcopy(virtcube)
        #print('next piece---', solve)
    for i in solve:
        if i[1] == 1:
            actualSolve.append(i[0])
        elif i[1] == 2:
            actualSolve.append(i[0] + '2')
        elif i[1] == 3:
            actualSolve.append(i[0] + '\'')
    return actualSolve,currentstate
def step4(state):
    currentstate=deepcopy(state)
    virtstate=deepcopy(currentstate)
    solve=[]
    actualSolve=[]
    topcolors=[]
    leftright=[('L','F'),('F','R'),('R','B'),('B','L')]
    opposites=[('F','B'),('L','R')]
    while len(topcolors)!=4:
        topcolors=[]
        for i in currentstate:
            if i[1]==0:
                #print(i,currentstate[i][5],[axisandvaluetonotation[(x,i[x])] for x in range(len(i)) if x!=1 and i[x]!=1])
                if currentstate[i][5]==0 and len([axisandvaluetonotation[(x,i[x])] for x in range(len(i)) if x!=1 and i[x]!=1])==1:
                    topcolors.append([axisandvaluetonotation[(x,i[x])] for x in range(len(i)) if x!=1 and i[x]!=1][0])
        #print(topcolors)
        if len(topcolors)==2:
            if sorted(topcolors)==['L','R'] or sorted(topcolors)==['B','F']:
                #print('line')
                for i in leftright:
                    if topcolors[0] in i:
                        if i.index(topcolors[0])==1:
                            otherdirection=topcolors[0]
                            currentdirection=i[(i.index(topcolors[0])+1)%2]
                            break
                solve.append([currentdirection, 3])
                virtstate = maketurn(virtstate, currentdirection + '\'')
                solve.append(['D', 3])
                virtstate = maketurn(virtstate, 'D\'')
                solve.append([otherdirection, 3])
                virtstate = maketurn(virtstate, otherdirection + '\'')
                solve.append(['D', 1])
                virtstate = maketurn(virtstate, 'D')
                solve.append([otherdirection, 1])
                virtstate = maketurn(virtstate, otherdirection)
                solve.append([currentdirection, 1])
                virtstate = maketurn(virtstate, currentdirection)
            else:
                #print('L')
                currentdirection=leftright[[sorted(i) for i in leftright].index(sorted(topcolors))][1]
                for i in leftright:
                    if currentdirection in i and sorted(i)!=sorted(topcolors):
                        otherdirection=i[(i.index(currentdirection)+1)%2]
                        break
                for i in opposites:
                    if currentdirection in i:
                        currentdirection=i[(i.index(currentdirection)+1)%2]
                        break
                #print(currentdirection,otherdirection)
                solve.append([currentdirection,1])
                virtstate=maketurn(virtstate,currentdirection)
                solve.append(['D',1])
                virtstate = maketurn(virtstate, 'D')
                solve.append([otherdirection, 1])
                virtstate = maketurn(virtstate, otherdirection)
                solve.append(['D', 3])
                virtstate = maketurn(virtstate, 'D\'')
                solve.append([otherdirection, 3])
                virtstate = maketurn(virtstate, otherdirection+'\'')
                solve.append([currentdirection, 3])
                virtstate = maketurn(virtstate, currentdirection+'\'')
        elif len(topcolors)==0:
            #print('center dot')
            currentdirection=leftright[0][1]
            otherdirection=leftright[0][0]
            solve.append([currentdirection, 1])
            virtstate = maketurn(virtstate, currentdirection)
            solve.append(['D', 1])
            virtstate = maketurn(virtstate, 'D')
            solve.append([otherdirection, 1])
            virtstate = maketurn(virtstate, otherdirection)
            solve.append(['D', 3])
            virtstate = maketurn(virtstate, 'D\'')
            solve.append([otherdirection, 3])
            virtstate = maketurn(virtstate, otherdirection + '\'')
            solve.append([currentdirection, 3])
            virtstate = maketurn(virtstate, currentdirection + '\'')
        currentstate=deepcopy(virtstate)
    for i in solve:
        if i[1] == 1:
            actualSolve.append(i[0])
        elif i[1] == 2:
            actualSolve.append(i[0] + '2')
        elif i[1] == 3:
            actualSolve.append(i[0] + '\'')
    return actualSolve,currentstate
def step5(state):
    '''0=behind (white)
            1=left (yellow)
            2=front (blue)
            3=right (green)
            4=top (orange)
            5=bottom (red)
            6=none (black)

            idk why i made it like this'''
    #white corner step
    currentstate=deepcopy(state)
    virtstate=deepcopy(currentstate)
    solve = []
    numwhite=0
    while numwhite<4:
        numwhite=0
        facecheckingorder=['F','L','B','R']
        opposites=[('F','B'),('L','R')]
        piececheck=[0,0,0]
        actualSolve=[]
        currentdirection=''
        notationtoindex={'B':0,'L':1,'F':2,'R':3,'U':4,'D':5}
        for i in [x for x in currentstate if x[1]==0 and x[0]!=1 and x[2]!=1]:
            if currentstate[i][5]==0:
                numwhite+=1
        if numwhite==1:
            rightstate = {'F': [1, 2], 'L': [1,2], 'B': [0, 1], 'R': [0,1]}
            for i in facecheckingorder:
                rightorient=[]
                for x in range(3):
                    piececheck[(threenotation[i][0]+2)%4]=x
                    piececheck[1]=0
                    piececheck[threenotation[i][0]]=threenotation[i][1]
                    if currentstate[tuple(piececheck)][5]==0:
                        rightorient.append(x)
                if len(rightorient)==2 and rightorient==rightstate[i]:
                    currentdirection=facecheckingorder[(facecheckingorder.index(i)+1)%4]
                    break
        elif numwhite==0:
            rightstate={'F':0,'L':0,'B':2,'R':2}
            for i in facecheckingorder:
                piececheck[(threenotation[i][0]+2)%4]=rightstate[i]
                piececheck[1]=0
                piececheck[threenotation[i][0]] = threenotation[i][1]
                if currentstate[tuple(piececheck)][notationtoindex[i]]==0:
                    for x in opposites:
                        if i in x:
                            currentdirection=x[(x.index(i)+1)%2]
                            break
                    break
        elif numwhite==2:
            rightstate = {'F': 2, 'L': 2, 'B': 0, 'R': 0}
            for i in facecheckingorder:
                piececheck[(threenotation[i][0]+2)%4]=rightstate[i]
                piececheck[1]=0
                piececheck[threenotation[i][0]] = threenotation[i][1]
                if currentstate[tuple(piececheck)][notationtoindex[i]]==0:
                    currentdirection=facecheckingorder[(facecheckingorder.index(i)+1)%4]
                    break
        if numwhite!=4:
            #print(currentdirection, numwhite)
            solve.append([currentdirection,1])
            virtstate=maketurn(virtstate,currentdirection)
            solve.append(['D',1])
            virtstate=maketurn(virtstate,'D')
            solve.append([currentdirection,3])
            virtstate = maketurn(virtstate, currentdirection+'\'')
            solve.append(['D', 1])
            virtstate = maketurn(virtstate, 'D')
            solve.append([currentdirection, 1])
            virtstate = maketurn(virtstate, currentdirection)
            solve.append(['D', 2])
            virtstate = maketurn(virtstate, 'D2')
            solve.append([currentdirection, 3])
            virtstate = maketurn(virtstate, currentdirection + '\'')
            currentstate=deepcopy(virtstate)
    for i in solve:
        if i[1] == 1:
            actualSolve.append(i[0])
        elif i[1] == 2:
            actualSolve.append(i[0] + '2')
        elif i[1] == 3:
            actualSolve.append(i[0] + '\'')
    return actualSolve, currentstate
def step6(state):
    currentstate=deepcopy(state)
    virtstate=deepcopy(currentstate)
    correct=0
    correctpieces=[]
    solve=[]
    actualSolve=[]
    order=[(2,0,2),(0,0,2),(0,0,0),(2,0,0)]
    opposites=[('F','B'),('L','R')]
    clock=['F','L','B','R']
    while correct<4:
        correct = 0
        correctpieces = []
        for i in order:
            if len([x for x in currentstate[i] if x != 6 and numtocolor[currentstate[i].index(x)] == x]) == 3:
                correct += 1
                correctpieces.append(i)
        solve.append(['D', 0])
        while correct<2:
            solve[len(solve)-1][1]+=1
            virtstate=maketurn(virtstate,'D')
            correct=0
            correctpieces=[]
            for i in order:
                if len([x for x in virtstate[i] if x!=6 and numtocolor[virtstate[i].index(x)]==x])==3:
                    correct+=1
                    correctpieces.append(i)
        if correct==2:
            if correctpieces[0][0]==correctpieces[1][0]:
                for i in opposites:
                    if axisandvaluetonotation[(0,correctpieces[0][0])] in i:
                        currentdirection=i[(i.index(axisandvaluetonotation[(0,correctpieces[0][0])])+1)%2]
                        backdirection=axisandvaluetonotation[(0,correctpieces[0][0])]
                        rightdirection=clock[(clock.index(currentdirection)+1)%4]
            elif correctpieces[0][2]==correctpieces[1][2]:
                #print(axisandvaluetonotation[(2, correctpieces[0][2])])
                for i in opposites:
                    if axisandvaluetonotation[(2, correctpieces[0][2])] in i:
                        currentdirection=i[(i.index(axisandvaluetonotation[(2, correctpieces[0][2])])+1)%2]
                        backdirection=axisandvaluetonotation[(2, correctpieces[0][2])]
                        rightdirection = clock[(clock.index(currentdirection) + 1) % 4]

            else:
                for i in opposites:
                    if axisandvaluetonotation[(0,correctpieces[0][0])] in i:
                        currentdirection=i[(i.index(axisandvaluetonotation[(0,correctpieces[0][0])])+1)%2]
                        backdirection=axisandvaluetonotation[(0,correctpieces[0][0])]
                        rightdirection=clock[(clock.index(currentdirection)+1)%4]
            solve.append([rightdirection,3])
            virtstate=maketurn(virtstate,rightdirection+'\'')
            solve.append([currentdirection,1])
            virtstate=maketurn(virtstate,currentdirection)
            solve.append([rightdirection, 3])
            virtstate = maketurn(virtstate, rightdirection+'\'')
            solve.append([backdirection,2])
            virtstate=maketurn(virtstate,backdirection+'2')
            solve.append([rightdirection, 1])
            virtstate = maketurn(virtstate, rightdirection)
            solve.append([currentdirection, 3])
            virtstate = maketurn(virtstate, currentdirection+'\'')
            solve.append([rightdirection, 3])
            virtstate = maketurn(virtstate, rightdirection + '\'')
            solve.append([backdirection, 2])
            virtstate = maketurn(virtstate, backdirection + '2')
            solve.append([rightdirection, 2])
            virtstate = maketurn(virtstate, rightdirection + '2')
            solve.append(['D',3])
            virtstate=maketurn(virtstate,'D\'')
            #print(currentdirection,backdirection,rightdirection)
        currentstate=deepcopy(virtstate)
        #print(correct,correctpieces)
    for i in solve:
        if i[1] == 1:
            actualSolve.append(i[0])
        elif i[1] == 2:
            actualSolve.append(i[0] + '2')
        elif i[1] == 3:
            actualSolve.append(i[0] + '\'')
    return actualSolve,currentstate
def step7(state):
    '''0=behind (white)
        1=left (yellow)
        2=front (blue)
        3=right (green)
        4=top (orange)
        5=bottom (red)
        6=none (black)'''
    currentstate=deepcopy(state)
    virtstate=deepcopy(currentstate)
    solve=[]
    actualSolve=[]
    order=[(1,0,2),(2,0,1),(1,0,0),(0,0,1)]
    clockwiseindexes=[2,3,0,1]
    while True:
        solid = (False, 6)
        for i in order:
            checkingcolor=[x for x in currentstate[i] if x!=6 and x!=0][0]
            if numtocolor[currentstate[i].index(checkingcolor)]==checkingcolor:
                if solid==(False,6):
                    solid=(True,currentstate[i].index(checkingcolor))
                else:
                    #print('solved')
                    for i in solve:
                        if i[1] == 1:
                            actualSolve.append(i[0])
                        elif i[1] == 2:
                            actualSolve.append(i[0] + '2')
                        elif i[1] == 3:
                            actualSolve.append(i[0] + '\'')
                    return actualSolve,currentstate
        if solid[0]==True:
            #print(solid)
            frontdirection=axisandvaluetonotation[(indextoaxisandvalue[clockwiseindexes[(clockwiseindexes.index(solid[1])+2)%4]][0],indextoaxisandvalue[clockwiseindexes[(clockwiseindexes.index(solid[1])+2)%4]][1]+1)]
            leftdirection = axisandvaluetonotation[(indextoaxisandvalue[clockwiseindexes[(clockwiseindexes.index(solid[1]) + 3) % 4]][0],indextoaxisandvalue[clockwiseindexes[(clockwiseindexes.index(solid[1]) + 3) % 4]][1] + 1)]
            rightdirection = axisandvaluetonotation[(indextoaxisandvalue[clockwiseindexes[(clockwiseindexes.index(solid[1]) + 1) % 4]][0],indextoaxisandvalue[clockwiseindexes[(clockwiseindexes.index(solid[1]) + 1) % 4]][1] + 1)]
            solve.append([frontdirection,2])
            virtstate=maketurn(virtstate,frontdirection+'2')
            if currentstate[order[(clockwiseindexes.index(solid[1])-1)%4]][clockwiseindexes[(clockwiseindexes.index(solid[1])-1)%4]]==numtocolor[clockwiseindexes[(clockwiseindexes.index(solid[1])-2)%4]]:
                #print('counter-clockwise')
                solve.append(['D', 3])
                virtstate = maketurn(virtstate, 'D\'')
            else:
                solve.append(['D', 1])
                virtstate = maketurn(virtstate, 'D')
                #print('clockwise')
            solve.append([leftdirection,1])
            virtstate=maketurn(virtstate,leftdirection)
            solve.append([rightdirection,3])
            virtstate=maketurn(virtstate,rightdirection+'\'')
            solve.append([frontdirection, 2])
            virtstate = maketurn(virtstate, frontdirection + '2')
            solve.append([leftdirection, 3])
            virtstate = maketurn(virtstate, leftdirection)
            solve.append([rightdirection, 1])
            virtstate = maketurn(virtstate, rightdirection + '\'')
            if currentstate[order[(clockwiseindexes.index(solid[1])-1)%4]][clockwiseindexes[(clockwiseindexes.index(solid[1])-1)%4]]==numtocolor[clockwiseindexes[(clockwiseindexes.index(solid[1])-2)%4]]:
                #print('counter-clockwise')
                solve.append(['D', 3])
                virtstate = maketurn(virtstate, 'D\'')
            else:
                solve.append(['D', 1])
                virtstate = maketurn(virtstate, 'D')
                #print('clockwise')
            solve.append([frontdirection, 2])
            virtstate = maketurn(virtstate, frontdirection + '2')
        else:
            solve.append(['F',2])
            virtstate=maketurn(virtstate,'F2')
            solve.append(['D',1])
            virtstate=maketurn(virtstate,'D')
            solve.append(['R',1])
            virtstate=maketurn(virtstate,'R')
            solve.append(['L',3])
            virtstate=maketurn(virtstate,'L\'')
            solve.append(['F', 2])
            virtstate = maketurn(virtstate, 'F2')
            solve.append(['R', 3])
            virtstate = maketurn(virtstate, 'R\'')
            solve.append(['L', 1])
            virtstate = maketurn(virtstate, 'L')
            solve.append(['D', 1])
            virtstate = maketurn(virtstate, 'D')
            solve.append(['F', 2])
            virtstate = maketurn(virtstate, 'F2')
            #print('no solid')
        currentstate=deepcopy(virtstate)
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
#print(newallcolors)
#pygame.time.wait(1000)
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
def RubiksCube():
    global size, turnangle, allcolors, finishturn, rotation,threenotation,constants
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
        allcolors=maketurn(allcolors,rotation)
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
def getturn():
    global rubiksmovequeue, threenotation,finishturn, queueremove, scramble,allcolors, animspeed, solve,solvetime,newrotation,newrubiksmovequeue
    keywords=['solve','scramble','step1','step2','step3','step4','step5','step6','step7']
    stepfunction={'step1':step1,'step2':step2,'step3':step3,'step4':step4,'step5':step5,'step6':step6,'step7':step7}
    while True:
        newrotation = input('Rubik\'s rotation? ')
        while not (((len(newrotation) == 1 and newrotation in threenotation) or (
                len(newrotation) == 2 and newrotation[0] in threenotation and (newrotation[1] == '2' or newrotation[1] == '\''))) or newrotation in keywords):
            newrotation = input('Invalid. Rubik\'s rotation? ')
        while queueremove==True:
            None
        if not(newrotation in keywords):
            while queueremove == True:
                None
            rubiksmovequeue.append(newrotation)
        elif newrotation=='solve':
            while queueremove == True:
                None
            #print(rubiksmovequeue,rotation)
            #rubiksmovequeue=step3(allcolors)[0]
            newrubiksmovequeue=[]
            for i in step1(allcolors)[0]:
                newrubiksmovequeue.append(i)
            for i in step2(step1(allcolors)[1])[0]:
                newrubiksmovequeue.append(i)
            for i in step3(step2(step1(allcolors)[1])[1])[0]:
                newrubiksmovequeue.append(i)
            for i in step4(step3(step2(step1(allcolors)[1])[1])[1])[0]:
                newrubiksmovequeue.append(i)
            for i in step5(step4(step3(step2(step1(allcolors)[1])[1])[1])[1])[0]:
                newrubiksmovequeue.append(i)
            for i in step6(step5(step4(step3(step2(step1(allcolors)[1])[1])[1])[1])[1])[0]:
                newrubiksmovequeue.append(i)
            for i in step7(step6(step5(step4(step3(step2(step1(allcolors)[1])[1])[1])[1])[1])[1])[0]:
                newrubiksmovequeue.append(i)
            while queueremove==True:
                None
            animspeed=90
            if len(newrubiksmovequeue)>0:
                while queueremove == True:
                    None
                finishturn=False
                while queueremove == True:
                    None
                solvetime = time.time()
                solve = True
            else:
                finishturn=True
                animspeed=5
            rubiksmovequeue=newrubiksmovequeue[::]
            while queueremove==True:
                None
            print("Solve (%s moves): "%(len(rubiksmovequeue))+str(rubiksmovequeue))
            while queueremove == True:
                None
        elif newrotation=='scramble':
            rubiksmovequeue=[]
            for i in range(20):
                rubiksmovequeue.append(
                    possiblemoves[random.randint(0, 5)] + possibleextensions[random.randint(0, 2)])
                if len(rubiksmovequeue) > 1:
                    while rubiksmovequeue[len(rubiksmovequeue) - 1][0] == rubiksmovequeue[len(rubiksmovequeue) - 2][0]:
                        rubiksmovequeue[len(rubiksmovequeue) - 1] = possiblemoves[random.randint(0, 5)] + possibleextensions[random.randint(0, 2)]
            print("Scramble: "+str(rubiksmovequeue))
            while queueremove == True:
                None
        else:
            while queueremove == True:
                None
            newrubiksmovequeue=stepfunction[newrotation](allcolors)[0]
            while queueremove == True:
                None
            rubiksmovequeue=newrubiksmovequeue[::]
#queuethread = threading.Thread(target=getturn)
#queuethread.setDaemon(True)
#queuethread.start()
#gluPerspective(45, dimensions[0] / dimensions[1], 0.1, 2000*3/size)
#glTranslatef(0,-2,-30)
#glScalef(1/scale,1/scale,1/scale)
#glRotatef(0,0,0,0)
#glScalef(3/size,3/size,3/size)
up=True
rotatekey=[0,0,0]
'''while running:
    #print(finishturn,rubiksmovequeue)
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
            if event.key==K_SPACE:
                rubiksmovequeue.append(
                    possiblemoves[random.randint(0, 5)] + possibleextensions[random.randint(0, 2)])
    if running==True:
        queueremove=True
        ''''''if finishturn==False:
            print(rotation,finishturn)''''''
        if len(rubiksmovequeue)!=0:
            rotation=rubiksmovequeue[0]
            finishturn=False
            turnangle+=animspeed
            if turnangle>=90:
                turnangle = 0
                finishturn=True
        ''''''if up==True:
            if turnangle<90:
                turnangle+=5
            else:
                up=False
        elif up==False:
            if turnangle>0:
                turnangle-=5
            else:
                up=True''''''
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
        #print(finishturn,len(rubiksmovequeue))
        if finishturn==True and len(rubiksmovequeue)==0:
            if solve==True:
                print('\nSolve took %f seconds'%(time.time()-solvetime))
                animspeed=5
                solve=False
        queueremove=False
        glPopMatrix()
        pygame.display.flip()'''

class glWindow(QtWidgets.QOpenGLWidget):
    def __init__(self,parent=None):
        self.initializeGL()
        self.paintGL()
    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        gluPerspective(45, dimensions[0] / dimensions[1], 0.1, 2000*3/size)
        glRotatef(0,0,0,0)
        glScalef(3/size,3/size,3/size)
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        background()
        RubiksCube()


if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    window=QtWidgets.QWidget()
    window.setWindowTitle('PyQt Rubiks Cube')
    window.setFixedSize(dimensions[0],dimensions[1])
    b = QtWidgets.QPushButton(window)
    b.setText("F")
    b.move(500, 40)
    b2 = QtWidgets.QPushButton(window)
    b2.setText("F\'")
    b3 = QtWidgets.QPushButton(window)
    b3.setText("B")
    gl=glWindow(window)
    gl.move(0,0)
    gl.setFixedSize(dimensions[0]/1.3, dimensions[1])
    #background()
    #window.setGeometry(0,0, dimensions[0], dimensions[1])
    window.show()
    sys.exit(app.exec_())