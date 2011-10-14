import os
import yaml
import pygame
import Engine2d as engine
import pygamefrontend
from pygamefrontend import functions

class MapViever:
    """Map Viewer for pygame frontend"""
    def __init__(self):
        SW,SH=pygamefrontend.SW,pygamefrontend.SH
        self.viewW=25
        self.viewH=18
        self.tilesize=pygamefrontend.TILESIZE
        #light
        self.lightsurface=pygame.Surface((SW,SH),pygame.SRCALPHA)
        self.lightoffset=self.tilesize/2 # offset for blit lights circles
        #player image
        self.playerimg=pygamefrontend.imgloader.loadimage("player")
        self.backimg=pygamefrontend.imgloader.loadimage("backimg")
        self.blockimages=pygamefrontend.imgloader.loadimages()

    def render(self, surface, center, mapobject):
        """Render map on the surface. Map will be centered on center position (global)."""
        cx, cy=center

        tilesize=self.tilesize
        #light level
        lightlevel=engine.environment.DAYTIME.getlightlevel()
        #fill mask layer
        self.lightsurface.fill((0,0,0,lightlevel))
        hW=self.viewW/2
        hH=self.viewH/2
        #render tiles
        for yy in range(cy-hH, cy+hH+1):
            locy=hH+cy-yy
            drawposy=locy*tilesize
            for xx in range(cx-hW, cx+hW+1):
                locx=hW+cx-xx

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
                    surface.blit(self.backimg, drawpos)
                    surface.blit(self.blockimages[block.id], drawpos)
                    #draw light emited by block
                    if block.lightradius:
                        radius=block.lightradius
                        functions.drawlight(self.lightsurface,(lx,ly),radius)
                #if not draw background image
                else:
                    surface.blit(self.backimg, drawpos)
                #render player image on center position
                if xx==cx and yy==cy:
                    surface.blit(self.playerimg, drawpos)
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

    def renderatplayer(self,surface,player,mapobject):
        """Render map centered on given player"""
        self.render(surface, player.getposition(), mapobject)
