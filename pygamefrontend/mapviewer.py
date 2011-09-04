import pygame

class MapViever:

    def render(self, surface, center, imageloader, mapobject):
        """Render map on the surface. Map will be centered on center position (global)."""
        img=pygame.Surface((640, 480))
        img.fill((0, 0, 0))
        cx, cy=center

        tilesize=32
        viewx=20
        viewy=15
        for yy in range(cy-viewy/2, cy+viewy/2+1): # size 15
            for xx in range(cx-viewx/2, cx+viewx/2+1): # size 20
                locx=(viewx/2)+cx-xx
                locy=(viewy/2)+cy-yy
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

    def renderatplayer(self,surface,player,imageloader,mapobject):
        """Render map centered on given player"""
        self.render(surface, player.getposition(), imageloader, mapobject)
