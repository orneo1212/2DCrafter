from pygamefrontend import imageloader, mapviewer
import Engine2d as engine
import pygame
import time
import pygamefrontend

"""Inventory screen (show content of Inventory object)"""
class InventoryScreen:
    def __init__(self):
        self.imgloader=imageloader.ImageLoader("data/images.yaml")
        self.font=pygame.font.SysFont("Sans", 14)
        #
        self.ts=pygamefrontend.TILESIZE+2 # tilesize
        self.inventorypos=(640-4*self.ts, 480-5*self.ts)
        self.itemsoffset=(2, 2)
        self.invsize=(4*self.ts, 5*self.ts)
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
        nx=self.inventorypos[0]+self.itemsoffset[0]
        ny=self.inventorypos[1]+self.itemsoffset[1]
        return (nx, ny)

    def getslotunderpoint(self, (mx, my)):
        """Return None if the point (mx, my) is not in
        inventory area, otherwise return index of slot"""
        nx, ny=self.getinvpos()
        if mx>nx and mx<nx+self.invsize[0]:
            if my>ny and my<ny+self.invsize[1]:
                px=(mx-nx)/self.ts
                py=(my-ny)/self.ts
                return px+4*py
        return None

    def redraw(self, screen):
        if not self.visible:return

        pygame.draw.rect(screen, (128, 128, 128), \
            (self.inventorypos, self.invsize), 0)

        xx=0 #current slot

        drawselected=True
        #Skip draw when there no inventory
        if not self.inventory:return
        for item in self.inventory.slots:
            if item!=None:
                img=self.imgloader.loadimage(item[0])
                nx=xx%4*self.ts+self.getinvpos()[0]
                ny=xx/4*self.ts+self.getinvpos()[1]
                screen.blit(img, (nx, ny))
                #draw count
                txt=self.font.render(str(item[1]), 1, (255, 255, 0))
                screen.blit(txt, (nx, ny))
                #draw selection
                if xx==self.selected and drawselected:
                    pygame.draw.rect(screen, (255, 255, 0), \
                        (nx-1, ny-1, self.ts, self.ts), 1)
                    drawselected=False
            xx+=1
