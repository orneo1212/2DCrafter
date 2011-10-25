import os
import pygame
import Engine
import pygamefrontend
from pygamefrontend import functions

SW, SH=pygamefrontend.SW, pygamefrontend.SH

class MapRender:
    """Map Viewer for pygame frontend"""
    def __init__(self):
        #View Width and height (in tiles)
        self.viewW=25
        self.viewH=18
        self.center=(self.viewW/2, self.viewH/2) # centered position
        #tilesize
        self.tilesize=pygamefrontend.TILESIZE
        #light
        self.lightsurface=pygame.Surface((SW, SH), pygame.SRCALPHA)
        #player image
        self.playerimg=pygamefrontend.imgloader.loadimage("player")
        #Sprites
        self.playersprite=pygamefrontend.animation.AnimatedSprite(self.playerimg)
        self.playersprite.start_animation()
        self.playersprite.set_delay(250)
        #images
        self.backimg=pygamefrontend.imgloader.loadimage("backimg")
        self.blockimages=pygamefrontend.imgloader.loadimages()
        #player position
        self.playerx=(self.viewW/2)*self.tilesize
        self.playery=(self.viewH/2)*self.tilesize
        #Map move offset
        self.mmox=0
        self.mmoy=0

    def calculate_drawpos(self, tiledposition, centered=(0, 0), offset=(0, 0)):
        """Calculate where object at tiledpositions (centered at center)
        should be drawn on the screen"""
        nx=tiledposition[0]-centered[0]
        ny=tiledposition[1]-centered[1]
        xx = (nx-ny)*32+400-32
        yy = (nx+ny)*16+300-16
        return (xx+offset[0], yy+offset[1])

    def render(self, surface, center, mapobject):
        """Render map on the surface. Map will be centered on center position (global)."""
        cx, cy=int(center[0]), int(center[1])

        tilesize=self.tilesize
        #light level
        if mapobject.index>0:
            lightlevel=255-16
        else:
            lightlevel=Engine.environment.DAYTIME.getlightlevel()
        #fill mask layer
        self.lightsurface.fill((0, 0, 0, lightlevel))
        #calculate map move offset (smooth move)
        #self.mmox=int((center[0]-cx)*tilesize)
        #self.mmoy=int((center[1]-cy)*tilesize)
        #render tiles in each layer
        for layer in [0,1]: # layers 0=blocks 1=items
            for yy in xrange(cy-self.center[1]-1, cy+self.center[1]+2):
                for xx in xrange(cx-self.center[0]-1, cx+self.center[0]+2):
                    #get block
                    block=mapobject.getblock((xx, yy), layer)
                    #calc position to blit
                    drawpos=self.calculate_drawpos((xx, yy), (cx, cy), \
                                       (self.mmox, self.mmoy))
                    #draw block
                    self.draw_block(surface, block, layer, drawpos)
        #draw light emited by player
        #functions.drawlight(self.lightsurface,(lx,ly),4)
        #blit light mask
        surface.blit(self.lightsurface, (0, 0))

    def draw_block(self, surface, block, layer, drawpos):
        """Draw block by given tile position"""
        drawblock=True

        #check for air and empty blocks
        if not block:drawblock=False # skip empty places
        elif block.id==0:drawblock=False # skip block with id 0

        #draw block only if there is one
        if drawblock:
            surface.blit(self.blockimages[block.id], drawpos)
            #draw light emited by block
            if block.lightradius:
                radius=block.lightradius
                functions.drawlight(self.lightsurface, drawpos, radius)
        #if not draw background image
        elif layer==False:
            surface.blit(self.backimg, drawpos)

    def drawplayer(self, surface):
        """Draw player centered at screen"""
        #render player image on center position\
        self.playersprite.update()
        playerframe=self.playersprite.get_current_frame()
        surface.blit(playerframe, (self.playerx, self.playery))

    def getglobalfromscreen(self, centerpos, screenpos):
        """get global position (in tiles) from screenpos,
        where view is centered at position centerposition (in tiles).
        positions should be given as tuple (x,y)"""
        nx=(screenpos[0]+self.mmox)-400
        ny=(screenpos[1]+self.mmoy)-300+8
        screentilex=(ny+nx/2)/32
        screentiley=(ny-nx/2)/32
        gx=screentilex+centerpos[0]
        gy=screentiley+centerpos[1]
        #print gx,gy,centerpos, screentilex,screentiley
        return [gx, gy]

    def renderatplayer(self, surface, player, mapobject):
        """Render map centered on given player"""
        self.render(surface, player.position, mapobject)
        self.drawplayer(surface)
