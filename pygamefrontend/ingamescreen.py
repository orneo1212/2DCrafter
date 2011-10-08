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
        self.invsize=(4*18,5*18)

    def update(self):
        pass

    def events(self,event):

        #left mouse button
        if pygame.mouse.get_pressed()[0]==1:
            #select block
            mx,my=pygame.mouse.get_pos()
            slotpos=self.getslotunderpoint((mx,my))
            if slotpos!=None:
                    slot=self.gameobj.player.inventory.slots[slotpos]
                    if slot!=None:
                        self.gameobj.currenttile=slot[0]

    def getinvpos(self):
        """get position of the top left corner of area to display
        inventory items"""
        nx=self.inventorypos[0]+self.itemsoffset[0]
        ny=self.inventorypos[1]+self.itemsoffset[1]
        return (nx,ny)

    def getslotunderpoint(self,(mx,my)):
        """Return None if the point (mx, my) is not in
        inventory area, otherwise return index of slot"""
        nx,ny=self.getinvpos()
        if mx>nx and mx<nx+self.invsize[0]:
            if my>ny and my<ny+self.invsize[1]:
                px=(mx-nx)/18
                py=(my-ny)/18
                return px+4*py
        return None

    def redraw(self,screen):
        screen.blit(self.backpackimage, self.inventorypos)
        xx=0
        for item in self.gameobj.player.inventory.slots:
            if item!=None:
                img=self.imgloader.loadimage(item[0])
                nx=xx%4*18+self.getinvpos()[0]
                ny=xx/4*18+self.getinvpos()[1]
                screen.blit(img,(nx,ny))
                xx+=1
