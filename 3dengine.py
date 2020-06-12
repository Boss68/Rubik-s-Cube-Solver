import pygame, math



#UHHHHHH NO DONT TRY THIS ANYMORE. USE rubikscubeopengl.py
pygame.init()
WIDTH=800
HEIGHT=800
WINDOW=pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)
pygame.display.set_caption('3D Engine')
cubeparams=[[(-1,-1,1),(1,-1,1),(1,-1,-1),(-1,-1,-1),(-1,1,-1),(-1,1,1),(1,1,1),(1,1,-1)],[(0,1),(0,3),(0,5),(1,2),(1,6),(2,3),(2,7),(3,4),(4,5),(4,7),(5,6),(6,7)]]
class Camera(object):
    def __init__(self,x,y,z,dirx,diry,speed):
        self.start=(x,y,z)
        self.posfont=pygame.font.SysFont('arial',20)
        self.speed=speed
        self.dirx=dirx
        self.diry=diry
    def update(self):
        global mousemovement,WIDTH,HEIGHT
        #print(math.degrees(math.atan2(*mousemovement)),math.hypot(*mousemovement))
        self.dirx+=mousemovement[0]/(WIDTH/2)*90
        self.diry+=mousemovement[1]/(HEIGHT/2)*90
        #print(self.dirx,self.diry)
        #WINDOW.blit(self.posfont.render(str((self.dirx,self.diry)),True,(0,0,0)),(0,0))
cam=Camera(0,2,-5,90,0,0.1)
class Shape(object):
    def __init__(self,verts,edges):
        global cam
        self.verts=verts
        self.edges=edges
        self.relx=[-cam.start[0]+i[0] for i in self.verts]
        self.rely=[-cam.start[1]+i[1] for i in self.verts]
        self.relz=[-cam.start[2]+i[2] for i in self.verts]
        self.dirchange=[]
    def update(self):
        global cam, mousemovement,WIDTH,HEIGHT
        self.drawpoints = []
        for i in range(len(self.verts)):
            #self.relx[i] -= math.cos(math.atan2(self.verts[i][2], self.verts[i][0]) - cam.dirx) * math.hypot(self.verts[i][0], self.verts[i][2])
            #self.relz[i] -=math.sin(math.atan2(self.verts[i][2], self.verts[i][0]) - cam.dirx) * math.hypot(self.verts[i][0],self.verts[i][2])
            #self.dirchange=[math.cos(math.atan2(self.verts[i][2],self.verts[i][0])-cam.dirx)*math.hypot(-cam.start[0]+self.verts[i][0],-cam.start[2]+self.verts[i][2]),math.sin(math.atan2(self.verts[i][2], self.verts[i][0]) - cam.dirx) * math.hypot(-cam.start[0]+self.verts[i][0],-cam.start[2]+self.verts[i][2])]
            self.angle=math.atan2(-cam.start[2]+self.verts[i][2],-cam.start[0]+self.verts[i][0])-math.radians(cam.dirx)
            self.dirchange=[self.relx[i]*math.cos(self.angle)-self.relz[i]*math.sin(self.angle),self.relx[i]*math.sin(self.angle)+self.relz[i]*math.cos(self.angle)]
            if pygame.key.get_pressed()[pygame.K_w]:
                self.relz[i]-=cam.speed
            elif pygame.key.get_pressed()[pygame.K_s]:
                self.relz[i]+=cam.speed
            if pygame.key.get_pressed()[pygame.K_a]:
                self.relx[i]+=cam.speed
            elif pygame.key.get_pressed()[pygame.K_d]:
                self.relx[i]-=cam.speed
            if self.relz[i]>0:
                self.drawpoints.append((int(round((self.relx[i]+self.dirchange[0])*(WIDTH/2)/(self.relz[i]+self.dirchange[1])))+int(round(WIDTH/2)),int(round(-self.rely[i]*(HEIGHT/2)/(self.relz[i]+self.dirchange[1])))+int(round(HEIGHT/2))))
            #WINDOW.blit(cam.posfont.render(str((self.relx[i]+self.dirchange[0], self.rely[i], self.relz[i]+self.dirchange[1]))+str((self.relx[i], self.rely[i], self.relz[i])), True, (0, 0, 0)),(0, 20 * i))
            WINDOW.blit(cam.posfont.render(str(math.hypot(self.verts[i][0],self.verts[i][2]))+' '+str(math.hypot(-cam.start[0]+self.verts[i][0],-cam.start[2]+self.verts[i][2])), True, (0, 0, 0)),(0, 20 * i))
        #print(self.drawpoints)
        for i in self.drawpoints:
            if i[0]>=0 and i[0]<=WIDTH and i[1]>=0 and i[1]<=HEIGHT:
                pygame.draw.circle(WINDOW,(0,0,0),i,2)
        for i in self.edges:
            if len(self.drawpoints)>i[0] and len(self.drawpoints)>i[1]:
                if self.drawpoints[i[0]][0] >= 0 and self.drawpoints[i[0]][0] <= WIDTH and self.drawpoints[i[0]][1] >= 0 and self.drawpoints[i[0]][1] <= HEIGHT:
                    if self.drawpoints[i[1]][0] >= 0 and self.drawpoints[i[1]][0] <= WIDTH and self.drawpoints[i[1]][1] >= 0 and self.drawpoints[i[1]][1] <= HEIGHT:
                        pygame.draw.line(WINDOW,(0,0,0),self.drawpoints[i[0]],self.drawpoints[i[1]])
running=True
cube=Shape(*cubeparams)
frame=0
mousemovement=(0,0)
while running:
    if frame>=60:
        mousemovement=pygame.mouse.get_rel()
    pygame.mouse.set_pos(int(round(WIDTH / 2)), int(round(HEIGHT / 2)))
    cam.update()
    cube.update()
    if frame>=60:
        mousemovement=pygame.mouse.get_rel()
    pygame.display.update()
    WINDOW.fill((255,255,255))
    frame+=1
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            pygame.quit()
            running=False
        elif i.type==pygame.KEYDOWN:
            if i.key==pygame.K_ESCAPE:
                pygame.quit()
                running=False