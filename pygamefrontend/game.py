from pygamefrontend import imageloader, mapviewer,ingamescreen
import Engine2d as engine
import pygame
import time
import math

"""Game """
class Game:
    def __init__(self, screen):
        self.screen=screen
        self.mapo=engine.map.Map()
        self.player=engine.player.Player("test", self.mapo)
        self.imageloader=imageloader.ImageLoader()
        self.mapviewer=mapviewer.MapViever()
        self.mapviewer.loadmapdata(self.mapo)
        #pages
        self.ingamescreen=ingamescreen.InGameScreen(self)
        #speeds
        self.movespeed=0.25
        self.mineticks=10 # number of ticks to mine
        self.minetick=0
        #times
        self.eventstime=time.time()
        self.eventdelay=0.025
        self.gametimer=pygame.time.Clock()
        #Action Distance
        self.actiondistance=4
        self.starttime=time.time()
        #Current selection
        self.currenttile=8

    def update(self):
        self.gametimer.tick()
        daydelta=time.time()-self.starttime
        if daydelta>1:
            self.starttime=time.time()
            self.mapviewer.updatedattime()
        #Grow
        if self.minetick%100==0:
            secp=self.mapo.convertposition(self.player.getposition())
            sector=self.mapo.getsector(secp[0])
            engine.map.randomgrow(sector)
        #update pages
        self.ingamescreen.update()

    def events(self):
        keys=pygame.key.get_pressed()
        event=pygame.event.poll()
        if event.type==pygame.QUIT:self.onexit()
        #events tick
        if time.time()>self.eventstime+self.eventdelay:
            self.eventstime=time.time()
            self.minetick+=1

            plpos=self.player.getposition()
            mx, my=pygame.mouse.get_pos()
            mtx, mty=self.mapviewer.getglobalfromscreen(plpos, (mx, my))

            #keys

            #time change
            if keys[pygame.K_F3]:
                self.mapviewer.daytime+=5
            if keys[pygame.K_F4]:
                self.mapviewer.daytime-=5
            #directions
            if keys[pygame.K_d]:
                self.player.move("e", self.movespeed)
            if keys[pygame.K_a]:
                self.player.move("w", self.movespeed)
            if keys[pygame.K_w]:
                self.player.move("n", self.movespeed)
            if keys[pygame.K_s]:
                self.player.move("s", self.movespeed)
            if keys[pygame.K_SPACE]:
                print "Position:", mtx, mty
                print "FPS:", self.gametimer.get_fps()
                print "Inventory:"
                for slot in self.player.inventory.slots:
                    if slot:print "Item ID=%s Count=%s" % (slot[0], slot[1])
            #Mouse events
            mousekeys=pygame.mouse.get_pressed()
            #mine block
            if mousekeys[0]==1:
                self.mineblock((mtx,mty))
            #get block under cursor
            if mousekeys[1]==1:
                block=self.mapo.getblock((mtx, mty))
                if block:self.currenttile=block.id
                else:self.currenttile=None
            #put block
            if mousekeys[2]==1:
                self.putblock((mtx,mty))
            #Send events to pages
            self.ingamescreen.events(event)

    def actioninrange(self,actionpos):
        plpos=self.player.getposition()
        if math.fabs(actionpos[0]-plpos[0])<=self.actiondistance and \
            math.fabs(actionpos[1]-plpos[1])<=self.actiondistance:
            return True
        else:return False

    def putblock(self,mousepos):
        #avoid putblock on player position
        if mousepos!=self.player.getposition():
            if self.actioninrange(mousepos):
                err=self.player.putblock(mousepos, self.currenttile)

    def mineblock(self,mousepos):
        plpos=self.player.getposition()
        if self.actioninrange(mousepos):
            if self.minetick%self.mineticks==0:
                err=self.player.mineblock(mousepos)

    def redraw(self):
        #clean the screen
        self.screen.fill((117,101,50))
        #render
        self.mapviewer.renderatplayer(self.screen, self.player, self.imageloader, self.mapo)
        #redraw pages
        self.ingamescreen.redraw(self.screen)
        pygame.display.update()

    def onexit(self):
        """On exit"""
        self.mapviewer.savemapdata(self.mapo)
        self.mapo.unloadsectors()
        self.player.unloadplayer()
        pygame.quit()
        exit()
