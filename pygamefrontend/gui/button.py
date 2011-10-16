import pygame
import pygamefrontend

class Button:
    def __init__(self,label, position):
        self.position=position #position of center
        #image
        self.image=pygamefrontend.imgloader.loadimage("button")
        self.size=self.image.get_size()
        self.font=pygame.font.SysFont("Sans",14)
        #label
        self.label=label
        self.labelcolor=(255,255,255)
        self.labelimg=self.font.render(self.label,1,self.labelcolor)
        #top-left corner of button
        self.posx=0
        self.posy=0
        #Callback
        self.clickcallback=None
        self.clickcallbackargs={}

    def connect(self,function,args={}):
        """Connect button callback on click to function."""
        self.clickcallback=function
        self.clickcallbackargs=args

    def setlabel(self, newlabel):
        """Set new label"""
        self.label=newlabel
        self.labelimg=self.font.render(self.label,1,self.labelcolor)

    def draw(self,surface):
        """Draw buttton on surface"""
        #recalculate top left corner
        self.posx=self.position[0]-self.size[0]/2
        self.posy=self.position[1]-self.size[1]/2
        #draw button image
        surface.blit(self.image,(self.posx, self.posy))
        #draw label
        posx=self.position[0]-self.labelimg.get_size()[0]/2
        posy=self.position[1]-self.labelimg.get_size()[1]/2
        surface.blit(self.labelimg, (posx, posy))

    def isunder(self, (mx,my)):
        """Return True when point is under button"""
        if mx>self.posx and mx< self.posx+self.size[0] and\
            my>self.posy and my < self.posy+self.size[1]:
            return True
        else:return False

    def events(self,event):
        """Handle button events"""
        if event.type==pygame.MOUSEBUTTONDOWN:
            #left mouse button
            if event.button==1:
                if self.isunder(event.pos):
                    if self.clickcallback:
                        self.clickcallback(*self.clickcallbackargs)
