import os
import yaml
import pygame
import Engine2d as engine
import pygamefrontend
from pygamefrontend import functions

SW,SH=pygamefrontend.SW,pygamefrontend.SH

class MapViever:
    """Map Viewer for pygame frontend"""
    def __init__(self):
        #View Width and height (in tiles)
        self.viewW=25
        self.viewH=18
        self.center=(self.viewW/2,self.viewH/2) # centered position
        #tilesize
        self.tilesize=pygamefrontend.TILESIZE
        #light
        self.lightsurface=pygame.Surface((SW,SH),pygame.SRCALPHA)
        #player image
        self.playerimg=pygamefrontend.imgloader.loadimage("player")
        self.backimg=pygamefrontend.imgloader.loadimage("backimg")
        self.blockimages=pygamefrontend.imgloader.loadimages()
        #player position
        self.playerx=(self.viewW/2)*self.tilesize
        self.playery=(self.viewH/2)*self.tilesize

    def calculate_drawpos(self,tiledposition,centered=(0,0)):
        """Calculate where object at tiledpositions (centered at center)
        should be drawn on the screen"""
        locx=self.center[0]+centered[0]-tiledposition[0]
        locy=self.center[1]+centered[1]-tiledposition[1]
        return (locx*self.tilesize,locy*self.tilesize)

    def render(self, surface, center, mapobject):
        """Render map on the surface. Map will be centered on center position (global)."""
        cx, cy=center

        tilesize=self.tilesize
        #light level
        lightlevel=engine.environment.DAYTIME.getlightlevel()
        #fill mask layer
        self.lightsurface.fill((0,0,0,lightlevel))
        #render tiles
        for yy in range(cy-self.center[1], cy+self.center[1]+1):
            for xx in range(cx-self.center[0], cx+self.center[0]+1):
                drawblock=True
                #get block and blit it
                block=mapobject.getblock((xx, yy))
                #check for air and empty blocks
                if not block:drawblock=False # skip empty places
                elif block.id==0:drawblock=False # skip block with id 0

                drawpos=self.calculate_drawpos((xx,yy),(cx,cy))

                #draw block only if there is one
                if drawblock:
                    surface.blit(self.backimg, drawpos)
                    surface.blit(self.blockimages[block.id], drawpos)
                    #draw light emited by block
                    if block.lightradius:
                        radius=block.lightradius
                        functions.drawlight(self.lightsurface,drawpos,radius)
                #if not draw background image
                else:
                    surface.blit(self.backimg, drawpos)

        #draw light emited by player
        #functions.drawlight(self.lightsurface,(lx,ly),4)
        #blit light mask
        surface.blit(self.lightsurface,(0,0))

    def drawplayer(self,surface):
        """Draw player centered at screen"""
        #render player image on center position
        surface.blit(self.playerimg, (self.playerx, self.playery))

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
        self.drawplayer(surface)
