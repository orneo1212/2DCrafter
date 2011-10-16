import pygame
import pygamefrontend

class Actionbar:
    def __init__(self,inventory):
        self.image=pygamefrontend.imgloader.loadimage("slotsframe")
        self.inventory=inventory
        self.selected=None
        self.position=(400-148, 600-45)
        self.offset=(6,6)
        self.font=pygame.font.SysFont("Sans", 12)

    def redraw(self,screen):
        #draw actionbar
        screen.blit(self.image, self.position)
        #Draw first row from inventory
        slotid=0
        for slot in self.inventory.getfirstrow():
            if slot:
                img=pygamefrontend.imgloader.loadimage(slot[0])
                #calculate slotpos
                slotposx=self.position[0]+self.offset[0]+slotid*36
                slotposy=self.position[1]+self.offset[1]
                #draw slot item
                screen.blit(img, (slotposx, slotposy))
                #draw count
                txt=self.font.render(str(slot[1]), 1, (255, 255, 0))
                screen.blit(txt, (slotposx, slotposy))
                #Draw selected if any
                if self.selected!=None:
                    if self.selected==slotid:
                        pygame.draw.rect(screen,(255,255,0), \
                            (400-148+6+slotid*36-1, 600-45+6-1,34,34),1)
            slotid+=1

    def getselected(self):
        """Get selected item id"""
        if self.inventory:
            if self.selected is None:return None
            slot=self.inventory.slots[self.selected]
            if slot:return slot[0]
        return 0

    def isunder(self,(mx,my)):
        """Point is under actionbar?"""
        if mx>400-148+6 and mx< 400-148+self.image.get_size()[0] \
            and my>600-45+6 and my< 600-6:return True
        else:return False

    def events(self,event):
        mx,my=pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.isunder((mx,my)):
                #get slotid under cursor
                sx=(mx-(400-148+6))/(pygamefrontend.TILESIZE+4)
                #sy=(my-(600-45+6))/pygamefrontend.TILESIZE
                self.selected=sx
