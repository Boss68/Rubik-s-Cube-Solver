import pygame

pygame.init()
makebuttons=['F','F\'','B','B\'','L','L\'','R','R\'','U','U\'','D','D\'','Scramble','Solve','Step 1','Step 2','Step 3','Step 4','Step 5','Step 6','Step 7']
size=100
buttonfont=pygame.font.SysFont('arial',size,True)
window=pygame.display.set_mode((640,480))
window.fill((255,255,0))
buttonpositions=[(19,170),(60,170),(19,220),(60,220),(19,270),(60,270),(19,320),(60,320),(19,370),(60,370),(19,420),(60,420),(445,430),(520,430),(460,207),(540,207),(460,257),(540,257),(460,307),(540,307),(500,357)]
while buttonfont.size('I')[1]>28:
    size-=1
    buttonfont = pygame.font.SysFont('arial', size, True)
for i in makebuttons:
    button=pygame.Surface((buttonfont.size(i)[0],30))
    button.fill((255,255,255))
    #mockscreen=pygame.Surface((640,480))
    #mockscreen=pygame.Surface.convert(mockscreen)
    #mockscreen.set_colorkey((255,0,0))
    #mockscreen.fill((255,0,0))
    pygame.draw.rect(button,(0,0,0),pygame.Rect(0,0,button.get_width(),button.get_height()),2)
    button.blit(buttonfont.render(i,True,(0,0,0)),(0,0))
    #mockscreen.blit(button,buttonpositions[makebuttons.index(i)])
    #window.blit(mockscreen,(0,0))
    #pygame.image.save(window,'bruh.png')
    pygame.image.save(button,'%s.png'%(i))
def tuplehex(hexa):
    string=str(hexa)[2:]
    while len(string)<6:
        string=string+'0'
    return (int(string[0:2],16),int(string[2:4],16),int(string[4:6],16))
#print([[tuplehex(hex(int(x))) for x in list(i)] for i in pygame.surfarray.array2d(pygame.image.load('F.bmp'))])