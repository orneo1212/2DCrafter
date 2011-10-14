import os
import yaml
import pygame
import Engine2d as engine
from pygamefrontend import functions

TILESIZE=32

class MapViever:
    def __init__(self):
        self.viewW=20
        self.viewH=15
        self.tilesize=TILESIZE
        #light
        self.lightsurface=pygame.Surface((640,480),pygame.SRCALPHA)
        self.lightoffset=TILESIZE/2 # offset for blit lights circles

    def render(self, surface, center, imageloader, mapobject):
        """Render map on the surface. Map will be centered on center position (global)."""
        cx, cy=center

        tilesize=self.tilesize
        #light level
        lightlevel=engine.environment.DAYTIME.getlightlevel()
        #fill mask layer
        self.lightsurface.fill((0,0,0,lightlevel))
        #render tiles
        for yy in range(cy-self.viewH/2, cy+self.viewH/2+1):
            locy=(self.viewH/2)+cy-yy
            drawposy=locy*tilesize
            for xx in range(cx-self.viewW/2, cx+self.viewW/2+1):
                locx=(self.viewW/2)+cx-xx

                drawblock=True

                #get block and blit it
                block=mapobject.getblock((xx, yy))
                #check for air and empty blocks
                if not block:drawblock=False # skip empty places
                elif block.id==0:drawblock=False # skip block with id 0

                drawposx=locx*tilesize

                drawpos=(drawposx,drawposy)
                #light position
                lx,ly=drawposx+self.lightoffset,\
                    drawposy+self.lightoffset

                #draw block only if there is one
                if drawblock:
                    blockimg=imageloader.loadimage(block.id)
                    surface.blit(blockimg, drawpos)
                    #draw light emited by block
                    if block.lightradius:
                        radius=block.lightradius
                        functions.drawlight(self.lightsurface,(lx,ly),radius)
                #if not draw background image
                else:
                    backimg=imageloader.loadimage("backimg")
                    surface.blit(backimg, drawpos)
                #render player image on center position
                if xx==cx and yy==cy:
                    playerimg=imageloader.loadimage("player")
                    surface.blit(playerimg, drawpos)
                    #draw light emited by player
                    #functions.drawlight(self.lightsurface,(lx,ly),4)
        #blit light mask
        surface.blit(self.lightsurface,(0,0))

    def getglobalfromscreen(self,centerpos,screenpos):
        """get global position (in tiles) from screenpos,
        where view is centered at position centerposition.
        positions should be given as tuple (x,y)"""
        screentilex=screenpos[0]/self.tilesize
        screentiley=screenpos[1]/self.tilesize
        gx=self.viewW/2+centerpos[0]-screentilex
        gy=self.viewH/2+centerpos[1]-screentiley
        return [gx,gy]

    def renderatplayer(self,surface,player,imageloader,mapobject):
        """Render map centered on given player"""
        self.render(surface, player.getposition(), imageloader, mapobject)
