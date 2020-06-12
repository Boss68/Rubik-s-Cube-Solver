import pygame

Fbutton=pygame.image.load('F.bmp')
Fbutton=pygame.transform.scale(Fbutton,(640,480))
print(pygame.image.tostring(Fbutton,'RGB',False))