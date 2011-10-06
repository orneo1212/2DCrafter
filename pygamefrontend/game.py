from pygamefrontend import imageloader, mapviewer
import Engine2d as engine
import pygame
import time

"""Game page"""
class Game:
    def __init__(self, screen):
        self.screen=screen
        self.mapo=engine.map.Map()
        self.player=engine.player.Player("test", self.mapo)
        self.imageloader=imageloader.ImageLoader()
        self.mapviewer=mapviewer.MapViever()
        #times
        self.eventstime=time.time()
        self.eventdelay=0.02
        #
        self.currenttile=0

    def update(self):
        pass

    def events(self):
        keys=pygame.key.get_pressed()
        event=pygame.event.poll()
        if event.type==pygame.QUIT:exit()
        #events tick
        if time.time()>self.eventstime+self.eventdelay:
            plpos=self.player.getposition()
            mx,my=pygame.mouse.get_pos()
            mtx,mty=self.mapviewer.getglobalfromscreen(plpos,(mx,my))
            self.eventstime=time.time()
            #keys
            if keys[pygame.K_d]:
                self.player.move("e", 0.25)
            if keys[pygame.K_a]:
                self.player.move("w", 0.25)
            if keys[pygame.K_w]:
                self.player.move("n", 0.25)
            if keys[pygame.K_s]:
                self.player.move("s", 0.25)
            if keys[pygame.K_SPACE]:
                print mtx,mty
            #Mouse events
            mousekeys=pygame.mouse.get_pressed()
            #mine block
            if mousekeys[0]==1:
                self.mapo.setblock((mtx,mty),None)
            #get block under cursor
            if mousekeys[1]==1:
                block=self.mapo.getblock((mtx,mty))
                if block:self.currenttile=block.id
                else:self.currenttile=None
            if mousekeys[2]==1:
                newblock=engine.map.Block(self.currenttile)
                self.mapo.setblock((mtx,mty),newblock)



    def redraw(self):
        self.mapviewer.renderatplayer(self.screen, self.player, self.imageloader, self.mapo)
        pygame.display.update()
