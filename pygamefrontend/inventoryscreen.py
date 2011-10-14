from pygamefrontend import imageloader, mapviewer
import Engine2d as engine
import pygame
import time
import pygamefrontend

"""Inventory screen (show content of Inventory object)"""
class InventoryScreen:
    def __init__(self):
        self.imgloader=imageloader.ImageLoader("data/images.yaml")
        self.image=self.imgloader.loadimage("inventoryframe", False)
        self.imgsize=self.image.get_size()
        self.font=pygame.font.SysFont("Sans", 14)
        self.imgoffset=(6,25)
        #
        self.ts=pygamefrontend.TILESIZE+4 # tilesize
        self.invsoffset=(0,0)
        self.invsize=(8, 4) # width, height
        self.invsizepix=(self.invsize[0]*self.ts,self.invsize[1]*self.ts)
        self.invpos=(320-self.imgsize[0]/2, 240-self.imgsize[1]/2)
        #
        self.visible=False
        self.inventory=None
        self.selected=0

    def setinventory(self, inventory):
        """Set inventory to display"""
        if inventory:
            self.inventory=inventory

    def getselected(self):
        """Get selected item id"""
        if self.inventory:
            slot=self.inventory.slots[self.selected]
            if slot:return slot[0]
        return 0

    def setselected(self,selecteditemid):
        """Set selected item"""
        self.selected=self.inventory.getslotid(selecteditemid)

    def update(self):
        pass

    def events(self, event):
        if not self.visible:return
        #left mouse button
        if pygame.mouse.get_pressed()[0]==1:
            #select block
            mx, my=pygame.mouse.get_pos()
            slotpos=self.getslotunderpoint((mx, my))
            if slotpos!=None and self.inventory:
                    slot=self.inventory.getslot(slotpos)
                    if slot!=None:self.selected=slotpos

    def getinvpos(self):
        """get position of the top left corner of area to display
        inventory items"""
        nx=self.invpos[0]+self.invsoffset[0]
        ny=self.invpos[1]+self.invsoffset[1]
        return (nx, ny)

    def isunder(self, (mx,my)):
        """Return True if point is under inventory"""
        if not self.visible:return False
        nx, ny=self.getinvpos()
        if mx>nx and mx<nx+self.invsizepix[0]:
            if my>ny and my<ny+self.invsizepix[1]:
                return True
        return False

    def getslotunderpoint(self, (mx, my)):
        """Return None if the point (mx, my) is not in
        inventory area, otherwise return index of slot"""
        nx, ny=self.getinvpos()
        if self.isunder((mx,my)):
            px=(mx-nx)/self.ts
            py=(my-ny)/self.ts
            return px+self.invsize[0]*py
        return None

    def redraw(self, screen):
        if not self.visible:return

        #pygame.draw.rect(screen, (128, 128, 128), \
        #    (self.invpos,self.invsizepix), 0)
        screen.blit(self.image,(self.invpos[0]-self.imgoffset[0],\
            self.invpos[1]-self.imgoffset[1]))
        xx=0 #current slot

        drawselected=True
        #Skip draw when there no inventory
        if not self.inventory:return
        for item in self.inventory.slots:
            if item!=None:
                img=self.imgloader.loadimage(item[0])
                nx=(xx%self.invsize[0])*self.ts+self.getinvpos()[0]
                ny=(xx/self.invsize[0])*self.ts+self.getinvpos()[1]
                screen.blit(img, (nx, ny))
                #draw count
                txt=self.font.render(str(item[1]), 1, (255, 255, 0))
                screen.blit(txt, (nx, ny))
                #draw selection
                if xx==self.selected and drawselected:
                    pygame.draw.rect(screen, (255, 255, 0), \
                        (nx-1, ny-1, self.ts-3, self.ts-3), 1)
                    drawselected=False
            xx+=1
