import pygame

class MapViever:

    def render(self, surface, center, imageloader, mapobject):
        """Render map on the surface. Map will be centered on center position (global)."""
        img=pygame.Surface((640, 480))
        img.fill((0, 0, 0))
        cx, cy, cz=center

        for yy in range(cy-7, cy+7+1): # size 15
            for xx in range(cx-10, cx+10+1): # size 20
                locx=(20/2)+cx-xx
                locy=(15/2)+cy-yy
                block=mapobject.getblock((xx, yy, cz))
                if not block:continue # skip empty places
                if block.id==0:continue # skip block with id 0 (air)
                blockimg=imageloader.loadimage(block.id)
                img.blit(blockimg, (locx*32, locy*32))
        #blit
        surface.blit(img, (0, 0))