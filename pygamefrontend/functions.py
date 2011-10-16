import math
import pygame
import Engine2d as engine
import pygamefrontend

lightoffset=pygamefrontend.TILESIZE/2 # offset for blit lights circles

def drawlight(surface,position,radius,delta=3,color=(128,128,0)):
    c1,c2,c3=color
    alpha=16
    lightcircle=engine.Config["circlelight"]
    position=(position[0]+lightoffset, position[1]+lightoffset)
    #draw square light
    if not lightcircle:
        for y in range(-radius-1,radius+1):
            for x in range(-radius-1,radius+1):
                dist=math.sqrt(x**2+y**2)
                if dist>radius:continue
                px=(position[0]-16)+x*32
                py=(position[1]-16)+y*32
                #draw each square
                pygame.draw.rect(surface,(c1,c2,c3,alpha),\
                    (px,py,32,32))
    else:
        #draw circle lights
        pygame.draw.circle(surface,(c1,c2,c3,alpha),position,radius*\
            pygamefrontend.TILESIZE)
