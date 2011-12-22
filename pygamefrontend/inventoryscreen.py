from pygamefrontend import imageloader
import Engine
import pygame
import time
import pygamefrontend

SW, SH=pygamefrontend.SW, pygamefrontend.SH

"""Inventory screen (show content of Inventory object)"""
class InventoryScreen:
    def __init__(self, image="inventoryframe"):
        self.imgloader=pygamefrontend.imgloader
        self.image=self.imgloader.loadimage(image, False)
        self.imgsize=self.image.get_size()
        self.font=pygame.font.SysFont("Sans", 12)
        self.imgoffset=(6, 27) #Dont touch
        #
        self.ts=pygamefrontend.TILESIZE+4 # tilesize
        #inventory offset (with image)
        self.invsoffset=(6, 190)
        self.invsize=(8, 4) # width, height
        self.invsizepix=(self.invsize[0]*self.ts, self.invsize[1]*self.ts)
        self.invpos=(SW/2-self.imgsize[0]/2, SH/2-self.imgsize[1]/2)
        #
        self.visible=False
        self.inventory=None
        self.selected=None
        self.lastslot=None # for tooltips
        self.tradeinventory=None # trade inventory

    def setinventory(self, inventory):
        """Set inventory to display"""
        if inventory:
            self.inventory=inventory

    def getselected(self):
        """Get selected item id"""
        if self.inventory:
            if self.selected is None:return None
            slot=self.inventory.slots[self.selected]
            if slot:return slot[0]
        return None

    def setselected(self, selecteditemid):
        """Set selected item"""
        self.selected=self.inventory.getslotid(selecteditemid)

    def update(self):
        pass

    def events(self, event):
        """Handle Inventory screen events"""
        #if not visible unselect slot
        if not self.visible:
            self.selected=None
            return

        #get slot under cursor
        mx, my=pygame.mouse.get_pos()
        slotpos=self.getslotunderpoint((mx, my))
        self.lastslot=slotpos # required for tooltips

        #left mouse button (select)
        if pygame.mouse.get_pressed()[0]==1:
            #select block
            nx,ny=self.getinvpos()

            #Hide inventory with Cross
            if mx>nx and mx<nx+10 and my>ny-20 and my<ny-5:
                self.visible=False

            #check slotpos
            if slotpos!=None and self.inventory:
                slot=self.inventory.getslot(slotpos)
                #If not selected. select one
                if slot!=None:
                    if self.selected is not None:
                        #replace items
                        data=self.inventory.getslot(slotpos)
                        tmp=self.inventory.getslot(self.selected)
                        self.inventory.slots[self.selected]=data
                        self.inventory.slots[slotpos]=tmp
                        self.selected=slotpos
                    else:
                        #Select one
                        self.selected=slotpos
                #rearrange slots
                else:
                    #only rearrange when slot is selected
                    if self.selected is not None:
                        data=self.inventory.getslot(self.selected)
                        if data is not None:
                            #Rearrange
                            self.inventory.slots[slotpos]=data
                            self.inventory.slots[self.selected]=None
                            self.selected=None

        #right mouse button (Trade)
        if pygame.mouse.get_pressed()[2]==1:
            if self.tradeinventory:
                mx, my=pygame.mouse.get_pos()
                slotpos=self.getslotunderpoint((mx, my))
                if slotpos!=None and self.inventory:
                    slot=self.inventory.getslot(slotpos)
                    if slot!=None:
                        err=self.tradeinventory.additem(slot[0])
                        #if adding success
                        if not err:
                            self.inventory.removeitem_fromslot(slotpos, slot[0])
                    else:self.selected=None

    def getinvpos(self):
        """get position of the top left corner of area to display
        inventory items"""
        nx=self.invpos[0]+self.invsoffset[0]
        ny=self.invpos[1]+self.invsoffset[1]
        return (nx, ny)

    def isunder(self, (mx, my)):
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
        if self.isunder((mx, my)):
            px=(mx-nx)/self.ts
            py=(my-ny)/self.ts
            return px+self.invsize[0]*py
        return None

    def setimage(self, imagename):
        """Set image for inventory background"""
        self.image=self.imgloader.loadfile(imagename)

    def redraw(self, screen, drawselected=True):
        if not self.visible:return

        #Draw inventory background
        screen.blit(self.image, (self.invpos[0]-\
            self.imgoffset[0]+self.invsoffset[0], \
            self.invpos[1]-self.imgoffset[1]+self.invsoffset[1]))
        xx=0 #current slot

        #Skip draw when there no inventory
        if not self.inventory:return
        for item in self.inventory.slots:
            if item!=None:
                img=self.imgloader.loadimage(item[0])
                nx=(xx%self.invsize[0])*self.ts+self.getinvpos()[0]
                ny=(xx/self.invsize[0])*self.ts+self.getinvpos()[1]
                screen.blit(img, (nx, ny))
                #Draw count
                txt=self.font.render(str(item[1]), 1, (255, 255, 0))
                screen.blit(txt, (nx, ny))
                #Draw selection
                if xx==self.selected and drawselected:
                    pygame.draw.rect(screen, (255, 255, 0), \
                        (nx-1, ny-1, self.ts-2, self.ts-2), 1)
                    drawselected=False
            #increase index
            xx+=1
        #Draw tooltip
        if self.lastslot!=None:
            slot=self.inventory.getslot(self.lastslot)
            if slot!=None:
                mx, my=pygame.mouse.get_pos()
                block=Engine.create_block(slot[0]) # create temp block
                #Draw tooltip background
                #pygame.draw.rect(screen, (64, 64, 64), \
                #   (mx, my, 128, 32), 0)
                #Draw item name
                color=(200, 200, 200)
                img=self.font.render(str(block.name), 1, color, (64, 64, 64))
                px,py=mx+(64-img.get_size()[0]/2),my
                screen.blit(img, (px, py))
