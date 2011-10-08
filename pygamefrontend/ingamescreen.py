from pygamefrontend import imageloader
import Engine2d as engine
import pygame
import time

"""InGame Screen """
class InGameScreen:
    def __init__(self, gameobject):
        self.gameobj=gameobject
        self.imgloader=imageloader.ImageLoader()
        self.backpackimage=self.imgloader.loadimage("backpackimage")
        self.inventorypos=(560,380)
        self.itemsoffset=(4,6)

    def update(self):
        pass

    def events(self,event):
        mx,my=pygame.mouse.get_pos()


    def redraw(self,screen):
        screen.blit(self.backpackimage, self.inventorypos)
        xx=0
        for item in self.gameobj.player.inventory.slots:
            if item!=None:
                img=self.imgloader.loadimage(item[0])
                nx=xx%4*18+self.inventorypos[0]+self.itemsoffset[0]
                ny=xx/4*18+self.inventorypos[1]+self.itemsoffset[1]
                screen.blit(img,(nx,ny))
                xx+=1
