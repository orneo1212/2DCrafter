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
        #day night cycle
        self.daylength=10*60 # day+night length in secs
        self.daytime=0.0 # time in secs
        self.lightlevel=255 # light level 0-255
        #time to change from day to night
        #sunset sunrise take 10% of time
        self.daydelta=255.0/(self.daylength*0.1)

    def updatedattime(self):
        """Update daytime cycle should be called in each sec"""
        self.daytime+=1

        #time tu sunrise or sunset
        dd=(self.daylength*0.1)

        #sunrise
        if self.daytime<=dd:
            self.lightlevel=255-self.daydelta*self.daytime
        #day
        if self.daytime>=dd and self.daytime<self.daylength/2:
            self.lightlevel=0
        #sunset
        if self.daytime>=self.daylength/2:
            lightdelta=self.daytime-self.daylength/2
            self.lightlevel=self.daydelta*lightdelta
        #night
        if self.daytime>=self.daylength/2+dd:
            self.lightlevel=255

        #limit
        if self.daytime>self.daylength:self.daytime=0
        if self.daytime<0:self.daytime=self.daylength

    def render(self, surface, center, imageloader, mapobject):
        """Render map on the surface. Map will be centered on center position (global)."""
        cx, cy=center

        tilesize=self.tilesize
        #avoid wrong daytime
        self.lightlevel=max(0,self.lightlevel)
        self.lightlevel=min(self.lightlevel,255)
        #fill mask layer
        self.lightsurface.fill((0,0,0,self.lightlevel))
        #render tiles
        for yy in range(cy-self.viewH/2, cy+self.viewH/2+1):
            for xx in range(cx-self.viewW/2, cx+self.viewW/2+1):
                locx=(self.viewW/2)+cx-xx
                locy=(self.viewH/2)+cy-yy

                drawblock=True

                #get block and blit it
                block=mapobject.getblock((xx, yy))
                #check for air and empty blocks
                if not block:drawblock=False # skip empty places
                elif block.id==0:drawblock=False # skip block with id 0

                drawposx=locx*tilesize
                drawposy=locy*tilesize
                drawpos=(drawposx,drawposy)
                #light position
                lx,ly=drawposx+self.lightoffset,\
                    drawposy+self.lightoffset

                drawoffset=(0,0,tilesize,tilesize)
                #draw block only if there is one
                if drawblock:
                    blockimg=imageloader.loadimage(block.id)
                    surface.blit(blockimg, drawpos, drawoffset)
                    #draw light emited by block
                    if block.lightradius:
                        radius=block.lightradius*self.tilesize
                        functions.drawlight(self.lightsurface,(lx,ly),radius)
                #if not draw background image
                else:
                    backimg=imageloader.loadimage("backimg")
                    surface.blit(backimg, drawpos, drawoffset)
                #render player image on center position
                if xx==cx and yy==cy:
                    playerimg=imageloader.loadimage("player")
                    surface.blit(playerimg, drawpos, drawoffset)
                    #draw light emited by player
                    functions.drawlight(self.lightsurface,(lx,ly),32)
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

    def savemapdata(self,mapobject):
        """Save map data to file"""
        worldpath=os.path.join(engine.mainpath, mapobject.mapname)
        mapfile=os.path.join(worldpath,"world.yaml")
        try:
            datafile=open(mapfile,"w")
        except:return
        args={}
        args["daytime"]=self.daytime
        args["mapseed"]=engine.seed
        yaml.dump(args,datafile)

    def loadmapdata(self,mapobject):
        """Load map data from file"""
        worldpath=os.path.join(engine.mainpath, mapobject.mapname)
        mapfile=os.path.join(worldpath,"world.yaml")
        try:
            data=yaml.load(open(mapfile))
        except:return
        self.daytime=data["daytime"]
        engine.seed=data["mapseed"]
