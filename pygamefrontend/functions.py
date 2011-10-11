import pygame

def drawlight(surface,position,radius,delta=3,color=(255,255,0)):
    c1,c2,c3=color
    alpha=0
    pygame.draw.circle(surface,(c1,c2,c3,alpha),position,radius)
