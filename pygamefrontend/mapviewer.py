import pygame

TILESIZE=16

class MapViever:
    def __init__(self):
        self.viewW=40
        self.viewH=30
        self.tilesize=TILESIZE
        #light
        self.lightsurface=pygame.Surface((640,480),pygame.SRCALPHA)
        #day night cycle
        self.daytimestep=255.0/600 # day length in secs
        self.daytime=0.0 # 0 day 255 night

    def updatedattime(self):
        """Update daytime cycle should be called in each sec"""
        self.daytime+=self.daytimestep
        if self.daytime>=255 or self.daytime<=0:
            self.daytimestep=-self.daytimestep

    def render(self, surface, center, imageloader, mapobject):
        """Render map on the surface. Map will be centered on center position (global)."""
        cx, cy=center

        tilesize=self.tilesize
        #avoid wrong daytime
        self.daytime=max(0,self.daytime)
        self.daytime=min(self.daytime,255)
        #fill mask layer
        self.lightsurface.fill((0,0,0,self.daytime))
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

                drawoffset=(0,0,tilesize,tilesize)
                #draw block only if there is one
                if drawblock:
                    blockimg=imageloader.loadimage(block.id)
                    surface.blit(blockimg, drawpos, drawoffset)
                    #draw light emited by block
                    if block.lightradius:
                        radius=block.lightradius*self.tilesize
                        pygame.draw.circle(self.lightsurface,
                        (255,255,255,0),(drawposx+8,drawposy+8),
                        radius,0)
                #if not draw background image
                else:
                    backimg=imageloader.loadimage("backimg")
                    surface.blit(backimg, drawpos, drawoffset)
                #render player image on center position
                if xx==cx and yy==cy:
                    playerimg=imageloader.loadimage("player")
                    surface.blit(playerimg, drawpos, drawoffset)
                    #draw light emited by player
                    pygame.draw.circle(self.lightsurface,
                        (255,255,255,0),(drawposx+8,drawposy+8),
                        32,0)
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
