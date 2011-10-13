import math
import pygame
import pygamefrontend

def drawlight(surface,position,radius,delta=3,color=(128,128,0)):
    c1,c2,c3=color
    alpha=16
    lightcircle=pygamefrontend.imgloader.config["circlelight"]
    if not lightcircle:
        for y in range(-radius-1,radius+1):
            for x in range(-radius-1,radius+1):
                dist=math.sqrt(x**2+y**2)
                if dist>radius:continue
                pp=((position[0]-16)+x*32, (position[1]-16)+y*32, 32, 32)
                pygame.draw.rect(surface,(c1,c2,c3,alpha),pp,0)
    else:
        #draw circle lights
        pygame.draw.circle(surface,(c1,c2,c3,alpha),position,radius*16)

