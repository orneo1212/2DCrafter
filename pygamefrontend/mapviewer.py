import pygame

class MapViever:

    def render(self, surface, center, imageloader, mapobject,layer=0):
        """Render map on the surface. Map will be centered on center position (global)."""
        img=pygame.Surface((640, 480))
        img.fill((128,0,0))
        cx,cy=center

        for yy in range(cy-7,cy+7+1): # size 15
            for xx in range(cx-10,cx+10): # size 20
                locx=(20/2)+1+cx+xx
                locy=(15/2)+1+cy+yy
                block=mapobject.getblock((cx,cy,layer))
                if not block:continue # skip empty places
                if block.id==0:continue # skip block with id 0 (air)
                blockimg=imageloader.loadimage(block.id)
                img.blit(blockimg,(locx*32,locy*32))
        #blit
        surface.blit(img,(0,0))