import pygame

class MapViever:
    def __init__(self):
        self.viewW=20
        self.viewH=15
        self.tilesize=32

    def render(self, surface, center, imageloader, mapobject):
        """Render map on the surface. Map will be centered on center position (global)."""
        img=pygame.Surface((640, 480))
        img.fill((0, 0, 0))
        cx, cy=center

        tilesize=self.tilesize

        for yy in range(cy-self.viewH/2, cy+self.viewH/2+1):
            for xx in range(cx-self.viewW/2, cx+self.viewW/2+1):
                locx=(self.viewW/2)+cx-xx
                locy=(self.viewH/2)+cy-yy
                #render player image on center position
                if xx==cx and yy==cy:
                    playerimg=imageloader.loadimage("player")
                    img.blit(playerimg, (locx*tilesize, locy*tilesize),(0,0,tilesize,tilesize))
                    continue
                block=mapobject.getblock((xx, yy))
                if not block:continue # skip empty places
                if block.id==0:continue # skip block with id 0 (air)
                blockimg=imageloader.loadimage(block.id)
                img.blit(blockimg, (locx*tilesize, locy*tilesize),(0,0,tilesize,tilesize))
        #blit
        surface.blit(img, (0, 0))

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
