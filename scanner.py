import pygame, cv2, math

capture=cv2.VideoCapture(0)
running=True
dimensions=(len(capture.read()[1][0]),len(capture.read()[1]))
print(dimensions)
window=pygame.display.set_mode(dimensions)
overlay=pygame.Surface((dimensions[1]/4,dimensions[1]/4))
overlay.set_colorkey((0,0,0))
overlay.fill((0,0,0))
pygame.draw.rect(overlay,(255,255,255),pygame.Rect(0,0,dimensions[1]/4,dimensions[1]/4),10)
scanned=pygame.Surface((dimensions[1]/4,dimensions[1]/4))
colorscanned=pygame.Surface((3,3))
allcolors=[(255,255,255),(255,255,0),(255,128,0),(0,255,0),(0,0,255),(255,0,0)]
def closestColor(colorlist,color):
    closest=0
    print(colorlist,color)
    for i in range(len(colorlist)):
        difference=0
        difference=sum([abs(colorlist[i][x]-color[x]) for x in range(3)])
        if difference<sum([abs(colorlist[closest][x]-color[x]) for x in range(3)]):
            closest=i
    #print(closest,color)
    return closest
while running:
    cam=pygame.transform.rotate(pygame.surfarray.make_surface(cv2.cvtColor(capture.read()[1],cv2.COLOR_BGR2RGB)),-90)
    cam=pygame.transform.flip(cam,True,False)
    window.blit(pygame.transform.flip(cam,True,False),(0,0))
    scanned.blit(cam,(0,0),area=((dimensions[0]-dimensions[1]/4)/2,(dimensions[1]-dimensions[1]/4)/2,dimensions[1]/4,dimensions[1]/4))
    window.blit(overlay,((dimensions[0]-dimensions[1]/4)/2,(dimensions[1]-dimensions[1]/4)/2))
    for i in range(3):
        for x in range(3):
            colorscanned.set_at((i,x),(allcolors[closestColor(allcolors,scanned.get_at((int(round(dimensions[1]/12*i+dimensions[1]/24)),int(round(dimensions[1]/12*x+dimensions[1]/24)))))]))
    window.blit(pygame.transform.scale(colorscanned,(int(round(dimensions[1]/4)),int(round(dimensions[1]/4)))),(0,0))
    pygame.display.update()
    window.fill((0,0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            running=False