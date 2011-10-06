from pygamefrontend import imageloader, mapviewer
from pygamefrontend import gamegui
import Engine2d as engine
import pygame
import time

"""Game """
class Game:
    def __init__(self, screen):
        self.screen=screen
        self.mapo=engine.map.Map()
        self.player=engine.player.Player("test", self.mapo)
        self.imageloader=imageloader.ImageLoader()
        self.mapviewer=mapviewer.MapViever()
        #speeds
        self.movespeed=0.25
        self.mineticks=10 # number of ticks to mine
        self.minetick=0
        #times
        self.eventstime=time.time()
        self.eventdelay=0.025
        #
        self.currenttile=0
        #GUI page
        self.guipage=gamegui.GameGUI(self.screen)

    def update(self):
        block=engine.map.Block(self.currenttile)
        self.guipage.labelposition.set_text(str(self.player.getposition()))
        self.guipage.labelselection.set_text(str(block.name))
        self.guipage.update()

    def events(self):
        keys=pygame.key.get_pressed()
        event=pygame.event.poll()
        #send event to pages
        self.guipage.events(event)
        if event.type==pygame.QUIT:exit()
        #events tick
        if time.time()>self.eventstime+self.eventdelay:
            self.eventstime=time.time()
            self.minetick+=1

            plpos=self.player.getposition()
            mx,my=pygame.mouse.get_pos()
            mtx,mty=self.mapviewer.getglobalfromscreen(plpos,(mx,my))

            #keys
            if keys[pygame.K_d]:
                self.player.move("e", self.movespeed)
            if keys[pygame.K_a]:
                self.player.move("w", self.movespeed)
            if keys[pygame.K_w]:
                self.player.move("n", self.movespeed)
            if keys[pygame.K_s]:
                self.player.move("s", self.movespeed)
            if keys[pygame.K_SPACE]:
                print mtx,mty
                print "Inventory",self.player.inventory.items
            #Mouse events
            mousekeys=pygame.mouse.get_pressed()
            #mine block
            if mousekeys[0]==1:
                if self.minetick%self.mineticks==0:
                    err=self.player.mineblock((mtx,mty))
            #get block under cursor
            if mousekeys[1]==1:
                block=self.mapo.getblock((mtx,mty))
                if block:self.currenttile=block.id
                else:self.currenttile=None
            #put block
            if mousekeys[2]==1:
                #avoid putblock on player position
                if (mtx,mty)!=self.player.getposition():
                    err=self.player.putblock((mtx,mty),self.currenttile)

    def redraw(self):
        self.mapviewer.renderatplayer(self.screen, self.player, self.imageloader, self.mapo)
        self.guipage.redraw()
        pygame.display.update()
